import streamlit as st
import base64



def home():
    st.html('<h3 class="title">Bem Vindo ao desafio final XPE - Simulador Financeiro</h3>')

    st.html("<iframe src='https://robertoricci.github.io/pbisolutions.github.io/' width='700' height='600'></iframe>")

    """Cria a página"""
    st.markdown("#### Sobre o Bootcamp - Ciências de Dados para o Mercado Financeiro DA XPE")
    c1, c2 = st.columns(2)
    c1.markdown(
        "[Desafio Final do BOOTCAMP - Ciências de Dados para o Mercado Financeiro DA XPE - Educação] (https://www.xpeducacao.com.br/bootcamp-pass/ciencia-de-dados-para-o-mercado-financeiro)"
    )
    # c2.markdown(
    #     "[Link Bootcamp](https://www.xpeducacao.com.br/bootcamp-pass/ciencia-de-dados-para-o-mercado-financeiro)"
    # )
    
    st.markdown("### Funcionalidades da aplicação:")


    st.markdown("""#### 1. Indices
- Acompanhe, em tempo real, as cotações de diversas bolsas internacionais, incluindo Brasil, EUA, Argentina, entre outras.
- Monitore índices econômicos importantes, como CDI, SELIC, IPCA e PIB, de forma automática.
- Consulte cotações de índices do mercado financeiro, como Bovespa, Petróleo Bruto, Ouro, entre outros, de forma dinâmica e atualizada.""")

    st.markdown("""#### 2. Renda Fixa
- Cálculo de Rentabilidade: Simule e calcule a rentabilidade de diversos títulos de renda fixa, como CDB, LCI e LCA.
- Suporte para títulos **pré-fixados** (com taxa de juros fixa) e **pós-fixados** (atrelados a indicadores como CDI, IPCA, entre outros).
- Acompanhe a **evolução do investimento** com gráficos interativos que mostram o desempenho ao longo do tempo.
- Simule investimentos com possibilidade de inserir o período do investimento e realizar aportes periódicos.
- Exibição de gráficos com projeções de crescimento e rentabilidade.""")

    st.markdown("""#### 4. Renda Variável
- **Screener de Ações**: Ferramenta de filtragem que permite selecionar ações com base em múltiplos critérios (como setor, P/L, dividend yield, etc.) para ajudar o investidor a escolher o melhor ativo.
- **Screener de Fundos Imobiliários**: Selecione fundos imobiliários (FIIs) com base em filtros como liquidez, dividend yield, tipo de imóvel, localização, e mais..""")

    st.markdown("""
        #### 5. Dividendos por Setor
- Gráficos interativos que mostram a distribuição de dividendos por setor, permitindo visualizar quais setores pagam os melhores dividendos.
- Comparação interativa entre setores para facilitar a tomada de decisão do investidor, de acordo com o DY""")

    st.markdown("""#### Fonte de dados
- Coleta dos dados fundamentalista em sites, e armazenamento em banco de dados.
- Cotações coletada através do yfinance.
- Indices econômicos coletado através do api do banco central.""")

    st.markdown("#### Livros recomendados:")
    col1, col2 , col3, col4 = st.columns(4)
    st.markdown("""
        <style>
        .rounded-image {
        border-radius: 30px; 
        height: 350px;
        padding: 3px 3px 3px 3px ;
        }
        </style> """, unsafe_allow_html=True)

    col1.markdown(
    """<a href="https://amzn.to/4cPKHTN">
        <img src="https://m.media-amazon.com/images/I/61skg9Wk8jL._SY522_.jpg" alt=Python e Mercado Financeiro: Programação Para Estudantes, Investidores e Analistas width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )

    col2.markdown(
    """<a href="https://amzn.to/3Wr3bUZ">
        <img src="https://m.media-amazon.com/images/I/71T8JKcwBXL._SY522_.jpg" alt="Python Aplicado: Bolsa de Valores - Um guia para construção de análises e indicadores" width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )
    
    col3.markdown(
    """<a href="https://amzn.to/4ds8RDp">
        <img src="https://m.media-amazon.com/images/I/81+RQr2khqL._SY466_.jpg" alt="Python Para Análise de Dados: Tratamento de Dados com Pandas, NumPy & Jupyter" width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )

    col4.markdown(
    """<a href="https://amzn.to/4d5d93F">
        <img src="https://m.media-amazon.com/images/I/616szDf9V2L._SY522_.jpg" alt="Faça Fortuna com Ações, Antes que seja Tarde " width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    col1.markdown(
    """<a href="https://amzn.to/3WsNaho">
        <img src="https://m.media-amazon.com/images/I/71XhGdYgoTL._SY522_.jpg" alt="O investidor inteligente " width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )

    col2.markdown(
    """<a href="https://amzn.to/4eObH6R">
        <img src="https://m.media-amazon.com/images/I/61LOilcY53L._SY466_.jpg" alt=Análise Técnica do Mercado Financeiro: um Guia Abrangente de Aplicações e Métodos de Negociação width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )


    col3.markdown(
    """<a href="https://amzn.to/47WbSL1">
        <img src="https://m.media-amazon.com/images/I/81ViUjhTWAL._SY466_.jpg" alt=Análise Técnica do Mercado Financeiro: um Guia Abrangente de Aplicações e Métodos de Negociação width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )


    col4.markdown(
    """<a href="https://amzn.to/4gMnUdW">
        <img src="https://m.media-amazon.com/images/I/91twOXkfEXL._SY466_.jpg" alt=Dominando o Ciclo de Mercado: Aprenda a Reconhecer Padrões Para Investir com Segurança width="300" class="rounded-image">
        </a>""",
    unsafe_allow_html=True,
    )

    st.write("")
    st.markdown(
         "[Link Github Projeto](https://https://github.com/robertoricci/Projeto_xpe)"
     )
    
    st.write("")
    st.markdown(
         "[Link Github da Minha caminhada no BOOTCAMP](https://github.com/robertoricci/XPE-Bootcamp-Cientista-de-Dados-com--nfase-em-Mercado-Financeiro)"
     )


    st.markdown("# Disclaimer:")
    st.markdown("""O conteúdo apresentado neste aplicação é destinada exclusivamente para fins educacionais e de estudo no mercado financeiro. 
                Ele não deve ser interpretado como recomendação de investimento, consultoria financeira ou qualquer forma de aconselhamento profissional. 
                As informações fornecidas podem não estar completas, precisas ou atualizadas. O uso do conteúdo é de inteira responsabilidade do usuário, 
                e qualquer decisão de investimento deve ser tomada com base em análise própria ou com a ajuda de um consultor financeiro licenciado.""")


