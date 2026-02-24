### 1. Diagrama de Casos de Uso
**Descrição:** Este diagrama mapeia as necessidades funcionais do sistema baseadas nos requisitos de reuso.
<img width="1024" height="236" alt="image" src="https://github.com/user-attachments/assets/5425d2db-34aa-476d-badc-26f2b98c10c1" />


### 1. UC 01: Buscar Produto nas Lojas
**Descrição:** Permite que o usuário localize ofertas de um produto específico através de integrações externas.

| Identificação | UC 01 |
| :--- | :--- |
| **Função** | Consultar as APIs das lojas parceiras para coletar dados de preços e produtos em tempo real. |
| **Atores** | Usuário |
| **Pré-condição** | 1) Conexão com a internet ativa para acessar APIs RESTful. <br> 2) Sistema disponível. |
| **Fluxo Principal** | 1) Usuário informa o nome do produto na barra de pesquisa. <br> 2) O sistema aciona os conectores de API fornecidos pelas próprias lojas. <br> 3) O sistema solicita os dados do produto em cada endpoint externo. <br> 4) O sistema recebe os dados brutos (JSON/XML). <br> 5) O sistema retorna a lista de resultados para processamento. |
| **Fluxo Secundário** | **A. Loja indisponível:** registrar erro de conexão e seguir para a próxima API. <br> **B. Produto não encontrado:** informar ao usuário que não há ofertas para o termo buscado. |

---

### 2. UC 02: Normalizar Resultados (Fuzzy Matching)
**Descrição:** Garante que variações de nomes do mesmo produto sejam tratadas como uma única entidade.

| Identificação | UC 02 |
| :--- | :--- |
| **Função** | Utilizar algoritmos de comparação de strings para identificar e unificar produtos idênticos com descrições diferentes [cite: 6]. |
| **Atores** | Sistema (Processo Interno) |
| **Pré-condição** | 1) Lista de produtos brutos obtida no UC 01. <br> 2) Biblioteca Fuzzy String Matching carregada. |
| **Fluxo Principal** | 1) O sistema percorre a lista de produtos recebidos das APIs. <br> 2) O sistema aplica o algoritmo de **Fuzzy Matching** entre os nomes. <br> 3) O sistema identifica que variações (ex: "Preto" vs "Black") referem-se ao mesmo item. <br> 4) O sistema agrupa os preços sob um único cabeçalho de produto. <br> 5) O sistema ordena as ofertas do menor para o maior preço. |
| **Fluxo Secundário** | **A. Baixa similaridade:** manter os produtos como itens distintos na lista de resultados. |

---

### 3. UC 03: Gerar Gráfico de Histórico de Preços
**Descrição:** Fornece inteligência de dados ao usuário sobre a variação de valor do produto ao longo do tempo.

| Identificação | UC 03 |
| :--- | :--- |
| **Função** | Processar dados históricos de preços para gerar visualizações estatísticas de tendências. |
| **Atores** | Usuário |
| **Pré-condição** | 1) Produto selecionado pelo usuário. <br> 2) Existência de dados históricos no banco de dados. <br> 3) Bibliotecas **Pandas e NumPy** operacionais. |
| **Fluxo Principal** | 1) Usuário solicita a visualização do histórico de 30 dias. <br> 2) O sistema recupera os registros de preços temporais. <br> 3) O sistema utiliza o **NumPy** para cálculos estatísticos. <br> 4) O sistema utiliza o **Pandas** para organizar e tratar as séries temporais. <br> 5) O sistema renderiza o gráfico de variação de preço na interface. |
| **Fluxo Secundário** | **A. Dados insuficientes:** informar ao usuário que ainda não há histórico acumulado para gerar o gráfico. |

---

### 4. UC 04: Configurar Alerta de Preço
**Descrição:** Permite o monitoramento automático de valores para futuras notificações através de Webhooks.

| Identificação | UC 04 |
| :--- | :--- |
| **Função** | Registrar o interesse do usuário em um valor alvo para um produto específico para monitoramento contínuo. |
| **Atores** | Usuário |
| **Pré-condição** | 1) Usuário identificado no sistema. <br> 2) Produto válido selecionado. |
| **Fluxo Principal** | 1) Usuário informa o preço desejado (valor alvo). <br> 2) Usuário fornece o e-mail para contato. <br> 3) O sistema registra o alerta e o vincula à rotina de monitoramento via APIs ou Webhooks. <br> 4) O sistema confirma o agendamento do alerta para o usuário. |
| **Fluxo Secundário** | **A. Valor alvo inválido:** sistema solicita que o usuário insira um valor numérico positivo. |

---

### 5. UC 05: Notificar Baixa de Preço
**Descrição:** Executa o envio da mensagem de alerta utilizando plataformas que garantem a entrega sem spam.

| Identificação | UC 05 |
| :--- | :--- |
| **Função** | Disparar notificações via e-mail utilizando a biblioteca **Smtplib** e serviços de mensageria. |
| **Atores** | Sistema (Processo Automático) |
| **Pré-condição** | 1) Gatilho de preço atingido (Preço Atual <= Preço Alvo). <br> 2) Servidor de mensageria e biblioteca **Smtplib** configurados. |
| **Fluxo Principal** | 1) O sistema detecta a queda de preço através de varredura ou Webhook. <br> 2) O sistema localiza os usuários com alertas ativos para aquele produto e valor. <br> 3) O sistema formata a mensagem de alerta. <br> 4) O sistema utiliza a biblioteca **Smtplib** para realizar o envio do e-mail. <br> 5) O sistema registra o log de notificação enviada com sucesso. |
| **Fluxo Secundário** | **A. Falha no envio:** o sistema registra a falha e agenda uma nova tentativa de disparo após um intervalo definido. |

---

### Interface do Sistema:

| Operação (Assinatura) | Descrição do Serviço | Artefato de Reuso Relacionado |
| :--- | :--- | :--- |
| `buscarProdutos(termoBusca)` | Realiza a varredura em múltiplas APIs externas e retorna uma lista agregada de ofertas. |Conectores de API / APIs RESTful |
| `obterAnaliseHistorica(idProduto)` | Fornece dados estatísticos, médias e séries temporais para a geração de gráficos de tendência. |Pandas / NumPy |
| `cadastrarAlerta(email, precoAlvo, idProduto)` | Registra o interesse de monitoramento de um usuário para envio de notificações automáticas. |Serviços de Mensageria / Webhooks |
| `validarSimilaridade(stringA, stringB)` | Expõe o serviço de normalização de produtos, identificando se descrições diferentes referem-se ao mesmo item. |Fuzzy String Matching |

---

### Descrição Técnica dos Serviços

1. **Serviço de Busca Agregada**: Focado na **Interoperabilidade**, permite que o sistema se comunique com múltiplos endpoints externos via APIs, evitando motores de busca proprietários.
2. **Serviço de Inteligência de Dados**: Utiliza bibliotecas de estatística para gerar a lógica de "o preço subiu ou desceu nos últimos 30 dias".
3. **Serviço de Notificação**: Garante que alertas sejam enviados via e-mail sem que caiam no spam, utilizando protocolos de rede estáveis.
4. **Serviço de Normalização**: Aplica algoritmos matemáticos para entender que variações textuais (ex: "Preto" vs "Black") são o mesmo produto.

---

### Agrupamento de Operações em Interfaces

| Interface | Operações Agrupadas | Justificativa de Agrupamento |
| :--- | :--- | :--- |
| **IStoreSearch** | `buscarProdutos(termoBusca)` | Focada na integração externa e coleta de dados brutos de APIs e lojas. |
| **IIntelligenceProcessor** | `validarSimilaridade(stringA, stringB)`, `obterAnaliseHistorica(idProduto)` | Reúne a lógica de processamento inteligente, incluindo normalização de textos e cálculos estatísticos. |
| **INotificationManager** | `cadastrarAlerta(email, precoAlvo, idProduto)` | Responsável pela gestão de saída de dados, interação com o usuário e agendamento de avisos. |

---

### Princípios de Design Utilizados

* **Coesão Funcional**: Cada interface possui uma responsabilidade única e bem definida dentro do domínio do problema.
* **Simplicidade de Interface**: Ao separar a busca da análise, permitimos que cada parte do sistema evolua de forma independente.
* **Preparação para Componentização**: Este agrupamento facilita a identificação de quais partes do código podem ser transformadas em componentes reutilizáveis.
