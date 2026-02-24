Membros:

Gustavo Bertoluzzi Cardoso: 22.123.016-2  

Isabella Vieira Silva Rossetto: 22.222.036-0 

Henrique Hodel Babler: 22.125.084-8 

Matheus Ferreira de Freitas: 22.125.085-5 

# BuscaTotal 🏷️

O **BuscaTotal** é uma plataforma de agregação de ofertas e inteligência de mercado voltada para o E-commerce. O sistema resolve o problema da fragmentação de preços em lojas online, oferecendo transparência, histórico de valores e automação de monitoramento para consumidores estratégicos.

Este projeto é desenvolvido como parte da disciplina de **Engenharia de Software Avançada**, focando na criação de um software evolutivo e escalável.

---

## 🚀 Sobre o Projeto

### O Problema
Com a proliferação de lojas online, um mesmo produto apresenta variações drásticas de preço, frete e disponibilidade. O consumidor perde tempo consultando diversos sites e muitas vezes não consegue validar se um desconto é real ou se o preço foi inflado recentemente ("metade do dobro").

### A Solução
O BuscaTotal elimina a necessidade de consulta manual, centralizando dados de múltiplas fontes, normalizando as informações e oferecendo ferramentas de análise de preço e notificações automáticas.

---

## 🧠 Domínio e Público-alvo

* **Domínio:** Agregação de Ofertas e Inteligência de Mercado.
* **Público-alvo:** Consumidores digitais que buscam otimizar o orçamento doméstico ou pessoal (desde compradores ocasionais até entusiastas de tecnologia).

---

## 🛠️ Processos de Negócio Identificados

O sistema opera sobre três processos fundamentais:

1.  **Consulta Unificada de Preços:** Realiza a busca em múltiplas APIs e fontes de varejo simultaneamente.
2.  **Padronização e Atualização de Dados:** Processo de limpeza e normalização (ETL) que organiza nomes, converte moedas e prepara os dados para comparação.
3.  **Alerta de Preço Desejado (Wishlist):** Serviço de monitoramento que rastreia produtos e notifica o usuário via múltiplos canais quando o preço alvo é atingido.

---

## 📊 Fluxograma do Processo

```mermaid
graph LR
    A[Usuário: Busca Produto] --> B(Sistema: Consulta Lojas)
    B --> C(Processo: Normalizar Dados)
    C --> D{Preço Ideal?}
    
    D -- Sim --> E[Ir para Loja]
    D -- Não --> F(Monitorar Preço)
    
    F --> G{Preço Caiu?}
    G -- Sim --> H[Notificar Usuário]
    G -- Não --> F
    H --> E
