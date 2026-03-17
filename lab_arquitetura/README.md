# Lab de Arquitetura - Componentes e Interfaces (BuscaTotal)

Este projeto implementa os três componentes do sistema arquitetural, focando na comunicação exclusiva por meio de interfaces (fornecidas e requeridas) e injeção de dependência, seguindo os contratos definidos nos Casos de Uso UC01 a UC07.

---

## 🚀 Como Executar o Projeto (Guia Passo a Passo no VSCode)

### Passo 1: Abrir o projeto no VSCode
1. Abra o **Visual Studio Code**.
2. Vá em `File > Open Folder...` e selecione a pasta **`lab_arquitetura`**.

### Passo 2: Abrir o Terminal do VSCode
1. No menu superior, clique em **`Terminal > New Terminal`**.
2. Certifique-se de que o caminho no terminal aponta para a pasta `lab_arquitetura`.

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar o Sistema
```bash
python app.py
```
*(Se não funcionar, tente `python3 app.py` ou `py app.py`)*

### Passo 5: Acessar a Interface
Quando aparecer `* Running on http://127.0.0.1:5001`, segure `Ctrl` e clique no link (ou cole no navegador).

---

## 1. Descrição dos Componentes Implementados

O sistema é composto por **três componentes** com responsabilidades distintas, baseados no Diagrama de Componentes definido no Lab 03:

### 1. Busca e Inteligência
- **Interface Realizada:** `BuscaService`
- **Responsabilidade:** Realizar a consulta às APIs das lojas parceiras e aplicar o algoritmo de *Fuzzy String Matching* (`difflib.SequenceMatcher`) para normalizar e agrupar ofertas de produtos idênticos com descrições diferentes (ex: "iPhone 15 Preto" ≡ "iPhone 15 Black"). É o **componente provedor central** que alimenta os demais com dados limpos e normalizados.

### 2. Analista Estatístico
- **Interface Realizada:** `AnaliseService`
- **Responsabilidade:** Processar o banco de dados histórico de preços utilizando **Pandas** e **NumPy**. Encapsula toda a lógica matemática para calcular tendências percentuais e determinar se uma promoção é real ou artificial. Gera os dados necessários para a renderização dos gráficos de variação de preço dos últimos 30 dias.

### 3. Mensageiro de Ofertas
- **Interface Realizada:** `AlertaService`
- **Responsabilidade:** Gerenciar a persistência dos alertas de preço, validar os valores-alvo informados pelos usuários e automatizar o disparo de e-mails via **Smtplib** quando o gatilho de preço é atingido.

---

## 2. Interfaces Fornecidas e Requeridas

A comunicação entre os componentes é estritamente definida por contratos de interface (utilizando o módulo `abc` do Python).

### Interfaces Fornecidas

| Interface | Componente Provedor | Operações |
| :--- | :--- | :--- |
| `BuscaService` | Busca e Inteligência | `consultarAPIsLojas(termoBusca)`, `normalizarProdutos(listaOfertas)`, `exibirListaOrdenada(listaOfertas)` |
| `AnaliseService` | Analista Estatístico | `gerarEstatisticasPreco(idProduto)`, `calcularTendencia(idProduto)` |
| `AlertaService` | Mensageiro de Ofertas | `configurarAlerta(email, idProduto, precoAlvo)`, `validarPrecoAlvo(precoAlvo, precoAtual)`, `notificarBaixaDePreco(idAlerta)` |

### Interfaces Requeridas

| Componente | Interface Requerida | Motivo |
| :--- | :--- | :--- |
| Analista Estatístico | `BuscaService` | Para analisar o histórico, precisa do nome padronizado do produto após o Fuzzy Matching. |
| Mensageiro de Ofertas | `BuscaService` | Para verificar se o preço caiu, precisa consultar o preço atualizado ao componente de busca. |

---

## 3. Contratos das Operações (Pré e Pós-condições)

### Componente: Busca e Inteligência

**`consultarAPIsLojas(termoBusca)`**
- **Pré-condição:** O `termoBusca` não pode ser nulo ou vazio; deve haver ao menos uma loja parceira ativa.
- **Pós-condição:** Lista de ofertas brutas retornada, contendo obrigatoriamente nome do produto, preço e loja de origem.

**`normalizarProdutos(listaOfertas)`**
- **Pré-condição:** A lista de ofertas brutas não pode ser nula; cada oferta deve conter nome e preço.
- **Pós-condição:** Produtos com nomes similares agrupados sob um ID único; retorna lista estruturada e normalizada.

### Componente: Analista Estatístico

**`gerarEstatisticasPreco(idProduto)`**
- **Pré-condição:** O `idProduto` deve ser válido e existente no banco; devem existir dados históricos de pelo menos 7 dias.
- **Pós-condição:** Retorna objeto Pandas DataFrame processado para plotagem, com tendência calculada em percentual.

### Componente: Mensageiro de Ofertas

**`configurarAlerta(email, idProduto, precoAlvo)`**
- **Pré-condição:** E-mail com formato sintático válido; `precoAlvo` numérico positivo e inferior ao preço atual do produto.
- **Pós-condição:** Alerta persistido no banco com status `Pendente`; e-mail de confirmação disparado ao usuário.

---

## 4. Comunicação entre os Componentes

A orquestração segue estritamente as assinaturas das interfaces, sem chamadas diretas entre implementações concretas:

1. O Front-end Web realiza um GET em `/api/search?q=TERMO` no servidor `app.py`.
2. O servidor aciona o componente **Busca e Inteligência** via `BuscaService.consultarAPIsLojas()`.
3. A lista bruta retornada é processada via `BuscaService.normalizarProdutos()` e ordenada via `BuscaService.exibirListaOrdenada()`.
4. Quando o usuário solicita um gráfico, o servidor aciona o **Analista Estatístico** via `AnaliseService.gerarEstatisticasPreco()`. Este componente, internamente, injeta a **interface requerida** `BuscaService` para obter o nome padronizado do produto antes da consulta histórica.
5. Quando um alerta de preço é configurado, o **Mensageiro de Ofertas** é acionado via `AlertaService.configurarAlerta()`. Para verificar o preço atual, ele utiliza sua **interface requerida** `BuscaService`, sem nunca instanciar diretamente o componente de busca.
6. O Sistema Cron/Webhook aciona `AlertaService.notificarBaixaDePreco()` periodicamente; se o gatilho é atingido, o e-mail é disparado via Smtplib.

---

## 5. Justificativa: Evitando o Acoplamento Direto

O acoplamento direto é evitado pelo **Mecanismo de Injeção de Dependência via construtor**, operacionalizado em `app.py`:

```python
# Em app.py — Entrypoint e Composição Root
busca_service = BuscaInteligencia()
analise_service = AnalistaEstatistico(busca_service)       # injeta BuscaService requerida
mensageiro = MensageiroDeOfertas(busca_service)            # injeta BuscaService requerida
```

No construtor do **Analista Estatístico**, por exemplo, nenhuma referência à classe concreta `BuscaInteligencia` existe — apenas ao contrato abstrato:

```python
def __init__(self, busca: IBuscaService):
    self._busca = busca
```

**Por que isso evita o acoplamento?**

- O **Analista Estatístico** e o **Mensageiro de Ofertas** desconhecem completamente como o Fuzzy Matching ou a consulta à API do Mercado Livre são implementados internamente.
- Qualquer outra implementação de `IBuscaService` (ex: um conector para Amazon, um mock de testes) pode ser injetada sem alterar uma linha dos componentes dependentes.
- Cumpre-se formalmente o **Princípio de Inversão de Dependência (DIP)** e o **Princípio de Segregação de Interfaces (ISP)**, conforme modelado no Diagrama de Componentes do Lab 03.

---

## 6. Casos de Uso Suportados

| Caso de Uso | Componente Responsável | Interface Utilizada |
| :--- | :--- | :--- |
| UC01 — Consultar APIs de Lojas | Busca e Inteligência | `BuscaService` |
| UC02 — Normalizar Produtos (Fuzzy Matching) | Busca e Inteligência | `BuscaService` |
| UC03 — Gerar Estatísticas de Preço | Analista Estatístico | `AnaliseService` |
| UC04 — Configurar Alerta de Preço | Mensageiro de Ofertas | `AlertaService` |
| UC05 — Notificar Baixa de Preço | Mensageiro de Ofertas | `AlertaService` |
| UC06 — Validar Preço Alvo | Mensageiro de Ofertas | `AlertaService` |
| UC07 — Exibir Lista Ordenada de Ofertas | Busca e Inteligência | `BuscaService` |

---
