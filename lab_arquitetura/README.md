# Lab de Arquitetura - Componentes e Interfaces (Web Migration)

Este projeto implementa dois componentes do sistema arquitetural modelado no Lab 3, focando na comunicação exclusiva por meio de interfaces (fornecidas e requeridas) e injeção de dependência.

Para tornar a experiência real e visual, a aplicação foi migrada para **Web (Flask)** e está totalmente integrada com a **API Pública do Mercado Livre**, utilizando o algoritmo *Fuzzy Matching* via `difflib` para classificar os itens buscados.

---

## 🚀 Como Executar o Projeto (Guia Passo a Passo no VSCode)

Este guia foi feito para ser executado de forma simples e direta utilizando o **Visual Studio Code (VSCode)**. Nenhuma configuração complexa de ambiente é necessária.

### Passo 1: Abrir o projeto no VSCode
1. Abra o **Visual Studio Code**.
2. Vá em `File > Open Folder...` (Arquivo > Abrir Pasta...).
3. Selecione a pasta **`lab_arquitetura`**.

### Passo 2: Abrir o Terminal do VSCode
1. No menu superior do VSCode, clique em **`Terminal > New Terminal`** (Terminal > Novo Terminal).
2. Uma janela preta vai aparecer na parte inferior da tela. Certifique-se de que o caminho na tela preta termine na pasta `lab_arquitetura`.

### Passo 3: Instalar as Bibliotecas
Este projeto utiliza recursos da Web para buscar dados reais (Flask para o servidor e BeautifulSoup4 para ler os sites parceiros). 

Na tela preta do terminal, copie e cole o comando abaixo e aperte **ENTER**:
```bash
pip install -r requirements.txt
```
*(Aguarde alguns segundos até que todas as barrinhas de download terminem).*

### Passo 4: Ligar o Sistema
Para ligar o nosso servidor inteligente de injeção de dependências, copie e cole o código abaixo no terminal e aperte **ENTER**:
```bash
python app.py
```
*(Se no seu computador o comando acima não funcionar, tente digitar `python3 app.py` ou `py app.py`)*.

### Passo 5: Acessar a Interface Gráfica Premium
Quando você ver a mensagem `* Running on http://127.0.0.1:5001` no terminal, significa que a arquitetura está rodando!

Para abrir o site:
1. Posicione o mouse em cima do link azul **http://127.0.0.1:5001** no terminal.
2. Segure a tecla **`Ctrl`** no seu teclado e **clique** no link (ou simplesmente copie o link e cole no seu Google Chrome).

Pronto! Ao buscar um produto no site, volte ao VSCode e repare na tela preta: você verá "ao vivo" as provas de que os componentes estão se comunicando via interface para aprovar (ou reprovar) a similaridade de cada item!

---

## 1. Descrição dos Componentes Implementados

Foram selecionados dois componentes que possuem dependência entre si, baseados nos Casos de Uso 01 e 02 do projeto "BuscaTotal", responsáveis pela busca externa e normalização dos dados:

1. **IntelligenceProcessor (Processador de Inteligência):**
   - **Descrição:** Componente responsável por processar e validar regras de negócio inteligentes. Agora, ele utiliza a biblioteca avançada nativa `difflib.SequenceMatcher` para normalização de strings e *Fuzzy Matching*. Ele recebe o termo buscado e o título vindo do Mercado Livre, retornando `True` se a similaridade for maior que `60%`.

2. **StoreSearch (Busca em Lojas):**
   - **Descrição:** Componente que agora realiza de fato uma requisição HTTP via biblioteca `requests` para o REST Endpoint do Mercado Livre. Recebe milhares de dados sujos JSON, e depende estritamente das regras de similaridade do componente 1 para filtrar as informações formatadas antes de mandá-las de volta para a Web.

---

## 2. Interfaces Fornecidas e Requeridas

A comunicação entre o sistema foi estritamente definida através da declaração de abstrações (interfaces do `abc` module no Python):

### **Interfaces Fornecidas**
- **`IIntelligenceProcessor`**: Fornecida pelo componente `IntelligenceProcessor`.
  - **Serviço:** `validar_similaridade(string_a: str, string_b: str) -> bool`
- **`IStoreSearch`**: Fornecida pelo componente `StoreSearch`.
  - **Serviço:** `buscar_produtos(termo_busca: str) -> list`

### **Interfaces Requeridas**
- O componente `StoreSearch` possui uma **Interface Requerida**: `IIntelligenceProcessor`. Ele *precisa* dessa interface para funcionar corretamente, pois depende do mecanismo de validação para montar os resultados da busca final.

---

## 3. Comunicação entre os Componentes

A comunicação ocorre estritamente pelas assinaturas das interfaces orquestradas pelo Entrypoint:
1. O Front-end Web faz um GET no endpoint `/api/search?q=TERMO` rodando em `app.py`.
2. O servidor aciona o componente `StoreSearch` através da sua interface fornecida `IStoreSearch.buscar_produtos()`.
3. Para cada item da grande lista recebida ao consumir a API pública do Mercado Livre, o `StoreSearch` invoca o método da sua **interface requerida**: `self._processor.validar_similaridade(termo, produto)`.
4. O `IntelligenceProcessor`, através da sua implementação da interface `IIntelligenceProcessor`, processa o pedido e devolve para o `StoreSearch` o valor lógico (se bate ou não). O Item é então filtrado.
5. Em nenhum momento o componente `StoreSearch` instancia ou chama diretamente um objeto da classe concreta `IntelligenceProcessor`. Tudo é resolvido por injeção na rota da aplicação central.

---

## 4. Justificativa: Evitando o Acoplamento Direto

O acoplamento direto foi evitado utilizando o **Mecanismo de Injeção de Dependência** via construtor.

Ao analisar o script central (`app.py`), a instanciação é feita ali e "injetada" em `StoreSearch` no construtor:

```python
# Em app.py
processor = IntelligenceProcessor()
store_search = StoreSearch(processor)
```

No construtor do `StoreSearch` (em `components/store_search.py`), observamos que ele sequer sabe quem é o `processor` instanciado, pois seu contrato visualiza apenas um objeto do tipo abstrato `IIntelligenceProcessor`:

```python
def __init__(self, processor: IIntelligenceProcessor):
    self._processor = processor
```

**Por que isso evita o acoplamento?**
- O `StoreSearch` não conhece como o algoritmo matemático em `difflib` está implementado iteramente.
- Poderíamos criar outras implementações como `RegexAIProcessor` ou alterar as taxas de similaridade e passar para o `StoreSearch` desde que elas respeitem a Interface `IIntelligenceProcessor`. O buscador continuaria funcionando sem precisar alterar uma linha do seu código interno.
- Cumpre-se formalmente com o Princípio de Inversão de Dependência (DIP - *Dependency Inversion Principle*).
