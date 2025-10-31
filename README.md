# Análise do Funil de Vendas + Teste A/A/B

> Projeto do curso TripleTen — Análise de comportamento de usuários no app de venda de produtos alimentícios.

---

## Visão geral

Neste projeto estudamos o comportamento dos usuários do aplicativo e avaliamos um experimento A/A/B que testa um novo estilo de fontes que os designers desenvolveram e desejam implementar no app. O objetivo principal é:

* Entender o funil de eventos (da abertura do app até o pagamento);
* Identificar onde perdemos mais usuários ao longo do funil;
* Avaliar se a mudança de fontes (grupo 248) afeta o comportamento comparado aos dois grupos de controle (246 e 247).

---

## Dados

**Arquivo:** `datasets/logs_exp_us.csv` - Este é o arquivo bruto que é processado pelo ETL
**Colunas relevantes:**

* `EventName` — nome do evento
* `DeviceIDHash` — identificador único do usuário
* `EventTimestamp` — timestamp do evento
* `ExpId` — id do experimento (246, 247 = controles; 248 = teste)

> Observação: o notebook `analise_funil_aab.ipynb` contém o ETL e toda a análise exploratória.

---

## ETL e preparação

Passos realizados (resumo):

1. Leitura do CSV e renomeação das colunas para nomes legíveis.
2. Conversão do `EventTimestamp` para `datetime` e criação de colunas auxiliares: `date` e `hour`.
3. Verificação e tratamento de valores ausentes e tipos incorretos.
4. Filtragem de registros antigos até o ponto em que os dados ficam consistentes - definida uma data de corte.
5. Mapeamento de grupos
6. Identificação de usuários que estão em mais de um grupo e os contaminados.

> Para reproduzir: execute o notebook `analise_funil_aab.ipynb` (célula ETL). Ele contém o código com as verificações e transformações.

## Saídas possíveis do ETL

Atualmente, este ETL gera um arquivo `.csv` no diretório local `data/processed/`.  
No entanto, o pipeline pode ser facilmente configurado para enviar os dados para outros destinos, como:

- Armazenamento em nuvem (S3, GCS, Azure)
- Bancos de dados SQL e NoSQL
- APIs externas ou dashboards analíticos
- Sistemas de mensageria e orquestração (Airflow, Kafka, Prefect)
- Data Warehouses e Data Lakes (BigQuery, Snowflake, Redshift)

---

## Análise exploratória (resumo)

**Número total de eventos:** *241298*
**Número total de usuários únicos:** *7534*
**Período dos dados (min → max):** *de 2019-08-01 00:07:28 até 2019-08-07 21:15:17*
**Média de eventos por usuário:** *34471*

> *Observação*: foram excluídos da análise registros anteriores à data de 01-08-2019, pois é a partir deste momento que os dados começam a ficar significantes. No total, foram excluídos 2828 eventos (1,16%) e 17 usuários(0.26%).

---

## Funil de eventos

### Etapas consideradas (exemplo)

1. MainScreenAppear - O app é iniciado e o usuário vê a tela principal. Ponto de entrada lógico.
2. OffersScreenAppear - O usuário navega pelas promoções ou produtos disponíveis.
3. CartScreenAppear - Após escolher produtos, ele acessa o carrinho para revisar a compra.
4. PaymentScreenSuccessful - O usuário finaliza a compra com sucesso.
5. Tutorial - Geralmente aparece apenas para novos usuários ou na primeira vez que o app é aberto.


### Métricas a reportar

* Usuários que fizeram cada evento (n e % do total de usuários):
                            *Usuário*   *Percentual*            
    MainScreenAppear	    7419	    98.47
    OffersScreenAppear	    4593	    60.96
    CartScreenAppear	    3734	    49.56
    PaymentScreenSuccessful	3539	    46.97
    Tutorial	            840	        11.15 
* Conversão entre etapas (porcentagem que vai de A→B, B→C, ...):
    Main → Offers: 61.91%
    Offers → Cart: 81.30%
    Cart → Payment: 94.78%
* Etapa com maior perda de usuários (gargalo do funil): Entre Main → Offers a taxa de perda é de 38%
* Proporção de usuários que completam o funil até `purchase`: 3429 usuários / 46.22%

---

## Análise do experimento A/A/B

### 1) Tamanho das amostras

* Usuários em ExpId 246 (controle A1): *2484*
* Usuários em ExpId 247 (controle A2): *2513*
* Usuários em ExpId 248 (teste - fonte nova): *2537*

### 2) Verificação A/A (246 vs 247)

* Teste realizado: comparação de proporções para os eventos mais populares (ex.: `Main`, `Offers`, `Payment`).
* Nível de significância usado inicialmente: **0.05**
* Resultados (exemplo de linha a preencher):

  * `MainScreenAppear`: p-valor = 0.7571, diferença significativa? *não*
  * `OffersScreenAppear`: p-valor = 0.2481, diferença significativa? *não*
  * `CartScreenAppearse`: p-valor = 0.2288, diferença significativa? *não*
  * `PaymentScreenSuccessful`: p-valor = 0.1146, diferença significativa? *não*

> Objetivo: Não houve diferença estatisticamente significativa em nenhum dos eventos entre os grupos de controle.
Isso confirma que a divisão dos grupos foi feita corretamente e que o experimento está equilibrado.

### 3) Comparação do grupo teste (248) vs controle (246+247)

* Procedimento: comparar proporções por evento entre 248 e cada controle isoladamente e também contra os controles combinados.
* Recomendações de interpretação:

  * Se 248 difere de ambos os controles em várias métricas e com p-valores baixos, há indícios de que a nova fonte altera o comportamento.
  * Se 248 difere de um controle mas não do outro, reavalie a aleatoriedade / tamanho das amostras.

Resultado resumido do teste:
                            Grupo A  Grupo B Grupo A(%) Grupo B(%)  p_valor  Diferença Significativa
CartScreenAppear                246      248      50.97      48.48   0.0784  False 
CartScreenAppear           controle      248      50.11      48.48   0.1818  False  
CartScreenAppear                247      248      49.26      48.48   0.5786  False  
MainScreenAppear           controle      248      98.58      98.27   0.2942  False  
MainScreenAppear                246      248      98.63      98.27   0.2950  False  
MainScreenAppear                247      248      98.53      98.27   0.4587  False  
OffersScreenAppear              246      248      62.08      60.35   0.2084  False  
OffersScreenAppear         controle      248      61.28      60.35   0.4343  False  
OffersScreenAppear              247      248      60.49      60.35   0.9198  False  
PaymentScreenSuccessful         246      248      48.31      46.55   0.2123  False  
PaymentScreenSuccessful    controle      248      47.19      46.55   0.6004  False  
PaymentScreenSuccessful         247      248      46.08      46.55   0.7373  False  
Tutorial                   controle      248      11.23      11.00   0.7649  False  
Tutorial                        247      248      11.26      11.00   0.7653  False  
Tutorial                        246      248      11.19      11.00   0.8264  False  

**Resultados resumidos:**

* Eventos em que 248 apresenta melhoria estatisticamente significativa: Nenhum evento apresentou diferença significativa.
* Eventos em que 248 apresenta piora estatisticamente significativa: Nenhum evento apresentou diferença significativa.
* Eventos sem diferença significativa: Todos os eventos testados (CartScreenAppear, MainScreenAppear, OffersScreenAppear, PaymentScreenSuccessful, Tutorial).

### 4) Correção para múltiplos testes

* Número de testes realizados: 15
* Com nível α = 0.05, nenhuma diferença atingiu significância.
* Correção Bonferroni (α corrigido ≈ 0.0033) confirmaria os mesmos resultados — sem diferenças significativas.

---

## Visualizações disponíveis

No notebook há células que geram os seguintes gráficos:

* Histograma de eventos por data/hora;
* Gráfico de barras com eventos por dia;
* Gráfico de barras com usuários por dia;
* Diagrama do funil com taxas de conversão entre etapas;

---

## Conclusões (exemplo de estrutura — preencha com os achados concretos)

1. A maior perda de usuários ocorre entre a tela principal (MainScreenAppear) e a tela de ofertas (OffersScreenAppear). Aproximadamente 38% dos usuários não avançam além da tela inicial, o que sugere que pode haver barreiras ou falta de incentivo para explorar os produtos.
2. Quase metade dos usuários (48%) que abrem o app completam toda a jornada até a compra, o que é uma taxa de conversão excelente!
3. Não houve diferença estatisticamente significativa em nenhum dos eventos entre os grupos de controle. Isso confirma que a divisão dos grupos foi feita corretamente e que o experimento está equilibrado.
4. O grupo 248 (nova fonte) *não alterou* a métrica `purchase` (p-valor = 0.6094).
5. Recomendação: Não houve evidência estatística de que a alteração das fontes do app tenha impactado o comportamento dos usuários, fica a cargo dos gestores diciderem pela implementação da nova interface ou não.

---

## Como reproduzir (instruções rápidas)

1. Abra `analise_funil_aab.ipynb`.
2. Execute as células na ordem (ETL → EDA → Funil → Experimento).
3. Ajuste `alpha` e método de correção para múltiplos testes conforme preferir.

---

## Estrutura de arquivos

---

analise_funil_vendas/
├── .venv/ # Ambiente virtual
├── analise/
│ └── analise_funil_aab.ipynb # Notebook principal de análise
├── data/
│ ├── processed/
│ │ └── logs_exp_us_processado.csv # Arquivo criado após o ETL
│ └── raw/
│ └── logs_exp_us.csv # Dataset bruto utilizado no extract
├── src/
│ ├── extract.py # Script responsável pela extração dos dados
│ ├── transform.py # Limpeza e transformação dos dados
│ ├── load.py # Carregamento e salvamento dos dados processados
│ └── main.py # Pipeline principal (executa o ETL completo)
├── requirements.txt
└── README.md

---

## Contato

Gustavo Savi — Analista de Dados (projeto TripleTen).
LinkedIn — [www.linkedin.com/in/gustavo-savi](http://www.linkedin.com/in/gustavo-savi)

---