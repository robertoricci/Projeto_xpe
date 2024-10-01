
#### Objetivo
Este projeto foi desenvolvido como parte do Desafio Final do Bootcamp de Ciências de Dados para o Mercado Financeiro promovido pela XPE. 
O objetivo é demonstrar as habilidades adquiridas durante o programa, 
aplicando técnicas avançadas de ciência de dados, conhecimento sobre mercado financiero para montar um simulador financeiro.


### Funcionalidades da aplicação:


 #### 1. Indices
- Acompanhe, em tempo real, as cotações de diversas bolsas internacionais, incluindo Brasil, EUA, Argentina, entre outras.
- Monitore índices econômicos importantes, como CDI, SELIC, IPCA e PIB, de forma automática.
- Consulte cotações de índices do mercado financeiro, como Bovespa, Petróleo Bruto, Ouro, entre outros, de forma dinâmica e atualizada.""")

#### 2. Renda Fixa
- Cálculo de Rentabilidade: Simule e calcule a rentabilidade de diversos títulos de renda fixa, como CDB, LCI e LCA.
- Suporte para títulos **pré-fixados** (com taxa de juros fixa) e **pós-fixados** (atrelados a indicadores como CDI, IPCA, entre outros).
- Acompanhe a **evolução do investimento** com gráficos interativos que mostram o desempenho ao longo do tempo.
- Simule investimentos com possibilidade de inserir o período do investimento e realizar aportes periódicos.
- Exibição de gráficos com projeções de crescimento e rentabilidade.""")

  #### 4. Renda Variável
- **Screener de Ações**: Ferramenta de filtragem que permite selecionar ações com base em múltiplos critérios (como setor, P/L, dividend yield, etc.) para ajudar o investidor a escolher o melhor ativo.
- **Screener de Fundos Imobiliários**: Selecione fundos imobiliários (FIIs) com base em filtros como liquidez, dividend yield, tipo de imóvel, localização, e mais..


#### 5. Dividendos por Setor
- Gráficos interativos que mostram a distribuição de dividendos por setor, permitindo visualizar quais setores pagam os melhores dividendos.
- Comparação interativa entre setores para facilitar a tomada de decisão do investidor, de acordo com o DY

#### Fonte de dados
- Coleta dos dados fundamentalista em sites, e armazenamento em banco de dados.
- Cotações coletada através do yfinance.
- Indices econômicos coletado através do api do banco central.



#### Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Python**: Linguagem principal para processamento e automação.
- **pandas**: Para manipulação e estruturação dos dados extraídos.
- **yfinance**: Para dowloados da cotação atualizado dos tickers.                
- **plotly**: para montagens dos gráficos.   
- **poetry**: para gerenciamentos das depedências 
- **Banco de Dados**:  PostgreSQL para armazenamento dos dados processados .
- **Interface Gráfica**: Desenvolvimento de uma interface gráfica usando o streamlit, para que usuários possam carregar os PDFs e visualizar os dados.


O projeto foi desenvolvido utilizando **3.10.0** e as seguintes bibliotecas:

```toml
[tool.poetry.dependencies]
python = "^3.10.0"
pandas = "^2.2.2"
streamlit = "^1.35.0"
taskipy = "^1.12.2"
plotly = "^5.22.0"
openpyxl = "^3.1.3"
streamlit-option-menu = "^0.3.13"
yfinance = "^0.2.40"
streamlit-extras = "^0.4.3"
sqlalchemy = "^2.0.31"
psycopg2 = "^2.9.9"
python-dotenv = "^1.0.1"
```

## Variáveis de Ambiente

O projeto requer as seguintes variáveis de ambiente para configurar o acesso ao banco de dados PostgreSQL:

- `DB_NAME`: Nome do banco de dados
- `DB_USER`: Nome de usuário do banco de dados
- `DB_PASSWORD`: Senha do banco de dados
- `DB_HOST`: Host do banco de dados (ex.: `localhost` ou IP do servidor)


## Configuração do Ambiente

para selecionar a versão do python com pyenv
```bash
   pyenv local 3.10.0
   ```

1. Clone o repositório:
   ```bash
   git clone https://github.com/robertoricci/Projeto_xpe.git
   cd Projeto_xpe
   ```

2. Instale as dependências usando Poetry:
   ```bash
   poetry install
   ```

3. Defina as variáveis de ambiente. Você pode criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo, podendo utilizar o exemplo do arquivo '`.env_exemplo`:
   ```env
   DB_NAME=seu_nome_de_banco_de_dados
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=seu_host
   ```

4. Execute o projeto:
   ```bash
   streamlit run app.py
   ou poetry run streamlit run app.py
   ```


## Link do Projeto ON line
[Projeto Hospedado do RENDER](https://xpe-simuladorfinanceiro.onrender.com//)


## Link da minha Jornada no BOOTCAMP
[Minha Jornada](https://github.com/robertoricci/XPE-Bootcamp-Cientista-de-Dados-com--nfase-em-Mercado-Financeiro)

