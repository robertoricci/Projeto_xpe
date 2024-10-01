import streamlit as st
import pandas as pd
import logging
import yfinance as yf
import pandas as pd
from datetime import date,datetime, timedelta
import plotly.express as px
import util.util as util



dict_tickers = {
    "Bovespa": {'ticker': "^BVSP", 'texto_pos': ' ptos', 'descricao': "O índice Bovespa, também conhecido como Ibovespa, é o principal índice de ações da bolsa de valores brasileira, a B3 (Brasil, Bolsa, Balcão). A unidade de medida do Ibovespa é em pontos. Ele é calculado a partir do desempenho das ações mais negociadas na B3, ponderado pelo valor de mercado das empresas. O Ibovespa é uma referência importante para o mercado financeiro brasileiro e é utilizado como indicador do desempenho médio das ações negociadas na bolsa."},
    #"IFIX": {'ticker': "^IFIX", 'texto_pos': ' pontos', 'descricao': "IFIX é um índice de desempenho que representa o desempenho médio dos fundos imobiliários negociados na bolsa de valores brasileira, a B3. O nome \"IFIX\" é uma sigla que significa \"Índice de Fundos Imobiliários\". O índice é calculado pela própria B3 e é composto por uma carteira teórica de fundos imobiliários listados na bolsa."},
    "NASDAQ": {'ticker': "^IXIC", 'texto_pos': ' ptos', 'descricao': "A NASDAQ é uma bolsa de valores eletrônica dos Estados Unidos, onde são negociadas ações de empresas de tecnologia e outras indústrias relacionadas. A NASDAQ também possui vários índices de ações, o mais conhecido dos quais é o NASDAQ Composite, que inclui todas as empresas listadas na bolsa. A unidade de medida do NASDAQ Composite é em pontos, calculados com base no valor de mercado de todas as ações incluídas no índice. Além do NASDAQ Composite, a NASDAQ também possui outros índices, como o NASDAQ 100, que inclui as 100 maiores empresas não financeiras listadas na bolsa."},
    "DAX": {'ticker': "^GDAXI", 'texto_pos': ' ptos', 'descricao': "O DAX é o principal índice de ações da bolsa de valores da Alemanha, a Frankfurt Stock Exchange (FSE). A unidade de medida do DAX é em pontos. Ele é calculado com base no desempenho das 30 maiores empresas listadas na FSE, ponderadas pelo valor de mercado das empresas. O DAX é um dos principais indicadores do mercado financeiro europeu e é frequentemente utilizado como uma referência para o desempenho das ações alemãs. O índice é considerado um barômetro importante para a economia alemã e é acompanhado de perto por investidores em todo o mundo."},
    "Nikkei 225": {'ticker': "^N225", 'texto_pos': ' ptos', 'descricao': "A Nikkei 225 é o principal índice de ações da bolsa de valores do Japão, a Tokyo Stock Exchange (TSE). A unidade de medida da Nikkei 225 é em pontos. Ele é calculado com base no desempenho das 225 empresas listadas na TSE, ponderadas pelo preço de suas ações. A Nikkei 225 é considerada um dos principais indicadores do mercado financeiro japonês e é amplamente acompanhada por investidores em todo o mundo. A composição do índice inclui empresas de diversos setores da economia, como eletrônicos, automóveis, finanças e telecomunicações, entre outros."},
    "FTSE 100": {'ticker': "^FTSE", 'texto_pos': ' ptos', 'descricao': "A FTSE 100 é o principal índice de ações da bolsa de valores do Reino Unido, a London Stock Exchange (LSE). A unidade de medida da FTSE 100 é em pontos. Ele é calculado com base no desempenho das 100 maiores empresas listadas na LSE, ponderadas pelo valor de mercado das empresas. A FTSE 100 é frequentemente considerada como um indicador do desempenho da economia britânica e é amplamente acompanhada por investidores em todo o mundo. A composição do índice inclui empresas de diversos setores, como finanças, energia, mineração, farmacêutico, entre outros. O FTSE 100 é um dos principais índices de ações europeus e é considerado um dos principais índices de referência para investidores que desejam acompanhar o mercado de ações do Reino Unido."},
    "PETRÓLEO CRU": {'ticker': "CL=F", 'texto_pos': ' USD/BBL', 'descricao': "O Petróleo Cru, também conhecido como WTI (West Texas Intermediate) ou Brent, é uma commodity negociada nos mercados financeiros internacionais. A unidade de medida do Petróleo Cru é em dólares americanos por barril (bbl). O preço do petróleo é influenciado por diversos fatores, como a oferta e a demanda global, a produção de petróleo dos países produtores, a política dos países exportadores, as condições climáticas, entre outros. O preço do petróleo é um dos indicadores mais importantes da economia global, já que o petróleo é uma das commodities mais amplamente utilizadas em todo o mundo, seja para a produção de energia, combustíveis, plásticos, entre outros produtos."},
    "OURO": {'ticker': "GC=F", 'texto_pos': ' ', 'descricao': "O ouro é uma commodity negociada nos mercados financeiros internacionais, e a unidade de medida padrão do ouro é a onça troy (oz t), que equivale a cerca de 31,1 gramas. O preço do ouro é influenciado por diversos fatores, como a demanda global por joias, a estabilidade política e econômica dos países, as condições do mercado financeiro global, a inflação, entre outros. O ouro é considerado uma reserva de valor, sendo muitas vezes utilizado como uma forma de proteger o patrimônio em tempos de instabilidade econômica ou política. O preço do ouro é um dos indicadores mais importantes dos mercados financeiros globais, e é amplamente acompanhado por investidores em todo o mundo."},
    "Bitcoin USD": {'ticker': "BTC-USD", 'texto_pos': ' USD', 'descricao': "O Bitcoin é uma criptomoeda negociada nos mercados financeiros internacionais e a unidade de medida padrão do preço do Bitcoin é em dólares americanos (USD) por unidade. O preço do Bitcoin é altamente volátil e é influenciado por diversos fatores, como a oferta e a demanda dos investidores, a adoção global da criptomoeda, as regulamentações governamentais, a confiança do mercado, entre outros. O Bitcoin é uma forma de ativo digital que permite transações financeiras sem a necessidade de intermediários, como bancos ou governos, e é considerado por muitos como uma alternativa ao sistema financeiro tradicional."},
    "Ethereum USD": {'ticker': "ETH-USD", 'texto_pos': ' USD', 'descricao': "O Ethereum é uma criptomoeda negociada nos mercados financeiros internacionais, e a unidade de medida padrão do preço do Ethereum é em dólares americanos (USD) por unidade. O preço do Ethereum é altamente volátil e é influenciado por diversos fatores, como a oferta e a demanda dos investidores, a adoção global da criptomoeda, as regulamentações governamentais, a confiança do mercado, entre outros. O Ethereum é uma plataforma blockchain descentralizada que permite a criação de aplicativos descentralizados e contratos inteligentes. A criptomoeda é utilizada para pagar pelos serviços na rede Ethereum, incluindo taxas de transação e remuneração para os mineradores. "},
    "Binance USD": {'ticker': "BNB-USD", 'texto_pos': ' USD', 'descricao': "BNB-USD é o par de negociação que representa a taxa de câmbio entre a criptomoeda Binance Coin (BNB) e o dólar americano (USD). O Binance Coin é uma criptomoeda desenvolvida pela exchange de criptomoedas Binance, que pode ser usada para pagar taxas de negociação na plataforma e para participar de campanhas e projetos lançados pela exchange."},
    "EURO/R$": {'ticker': "EURBRL=X", 'texto_pos': ' R$', 'descricao': "Euro/R$ é o par de moedas que representa a taxa de câmbio entre o euro e o real brasileiro. A unidade de medida padrão para o par de moedas Euro/R$ é o valor do euro em reais. Ou seja, se a taxa de câmbio do Euro/R$ for 6,00, significa que um euro vale 6 reais. "},
    "USD/R$": {'ticker': "USDBRL=X", 'texto_pos': ' R$', 'descricao': "USD/R$ é o par de moedas que representa a taxa de câmbio entre o dólar americano e o real brasileiro. A unidade de medida padrão para o par de moedas USD/R$ é o valor do dólar em reais. Ou seja, se a taxa de câmbio do USD/R$ for 5,00, significa que um dólar vale 5 reais."},
    "CAD/R$": {'ticker': "CADBRL=X", 'texto_pos': ' R$', 'descricao': "CAD/R$ é o par de moedas que representa a taxa de câmbio entre o dólar canadense e o real brasileiro. A unidade de medida padrão para o par de moedas CAD/R$ é o valor do dólar canadense em reais. Ou seja, se a taxa de câmbio do CAD/R$ for 4,00, significa que um dólar canadense vale 4 reais."},
    "S&P500": {'ticker': "^GSPC", 'texto_pos': ' ptos', 'descricao': "O S&P 500 é um índice de ações das 500 maiores empresas negociadas nas bolsas de valores dos Estados Unidos, selecionadas com base em sua capitalização de mercado, liquidez e representatividade setorial. A unidade de medida do S&P 500 é em pontos. O índice é calculado com base na soma dos valores de mercado das ações das 500 empresas componentes, ponderados pelo seu peso relativo no índice. O S&P 500 é um dos principais indicadores do mercado financeiro dos Estados Unidos e é amplamente utilizado como referência para o desempenho do mercado de ações americano."},
}


dict_indices = {
    "CDI": {'cod_bcb':1178,'texto_pre':" ",'texto_pos':" % ",'descricao':'O índice CDI (Certificado de Depósito Interbancário) é uma taxa que serve de referência para diversas aplicações financeiras no Brasil. Ele representa a média das taxas de juros praticadas em empréstimos entre os bancos, com prazo diário, e é calculado diariamente pela CETIP (Câmara de Custódia e Liquidação)'},
    "SELIC": {'cod_bcb':432,'texto_pre':" ",'texto_pos':" % ",'descricao':'O índice SELIC (Sistema Especial de Liquidação e de Custódia) é a taxa básica de juros da economia brasileira. Ele é determinado pelo Comitê de Política Monetária (COPOM) do Banco Central do Brasil e serve como referência para diversas operações financeiras no país'},
    "IPCA": {'cod_bcb':13522,'texto_pre':" ",'texto_pos':" %",'descricao':'O Índice de Preços ao Consumidor Amplo (IPCA) é o indicador oficial de inflação no Brasil, utilizado pelo Instituto Brasileiro de Geografia e Estatística (IBGE). Ele mede a variação média dos preços de um conjunto específico de produtos e serviços consumidos pelas famílias brasileiras que possuem renda entre 1 e 40 salários mínimos'},
    "PIB": {'cod_bcb':24364,'texto_pre':" R$",'texto_pos':" Trilhão",'descricao':'O Produto Interno Bruto (PIB) é uma medida que quantifica a atividade econômica de um país em um determinado período de tempo, geralmente anualmente ou trimestralmente. Ele representa o valor total de todos os bens e serviços finais produzidos dentro do território econômico de um país durante um período específico'},
}

@st.cache_data(show_spinner="Carregando dados...", ttl=60*5)
def buscar_mercado(tickers, df_info):
    count = 0
    for ticker in tickers:
        cotacoes = yf.download(ticker, period='5d')['Adj Close']
        variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
        df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1], 2)
        df_info['%'][count] = round(variacao, 2)
        count += 1
    return df_info


@st.cache_data(show_spinner="Carregando dados ticker...", ttl=60*50)
def buscar_mercado_unico(ticker):
        cotacoes = yf.download(ticker, period='5d')['Adj Close']
        variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1) * 100
        return variacao


# @st.cache_data(show_spinner="Carregando dados...", ttl=60*5)
# def buscar_dados_intraday(dict_tickers, indice):
#     logging.log(logging.DEBUG, "Buscando dados intraday...")
#     ticker_diario = yf.download(dict_tickers.get(
#         indice)['ticker'], period='1d', interval='5m')
#     return ticker_diario

def gerar_descricao(dict_tickers, df_info, numero_item):
    hint = dict_tickers.get(df_info['Ativo'][numero_item])[
        'descricao']
    nome = df_info['Ativo'][numero_item].replace("$", "\$")
    codigo_yf = dict_tickers.get(df_info['Ativo'][numero_item])['ticker']

    return "**[" + nome + "]" + \
        f"(https://br.financas.yahoo.com/quote/{codigo_yf}?p={codigo_yf}, \"" + \
        hint + "\")**"


def gerar_descricao_ind(ind, hint):
    ##hint = dict_tickers.get(df_info['Ativo'][numero_item])['descricao']
    ##nome = df_info['Ativo'][numero_item].replace("$", "\$")

    return "**[" + ind + "]" + \
        f"(https://www.bcb.gov.br/estatisticas/indecoreestruturacao, \"" + \
        hint + "\")**"


def gerar_valor(dict_tickers, df_info, numero_item):
    valor = df_info['Ult. Valor'][numero_item]
    valor_br = str(valor).replace(',', '').replace('.', ',')

    return str(valor_br) + \
        dict_tickers.get(df_info['Ativo'][numero_item])['texto_pos']

@st.cache_data(show_spinner="Carregando dados...", ttl=timedelta(days=1))
def get_indice_bcb_tab(cod_bcb,dt_ini,dt_fim):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'
    """
    Parameters
    ----------
    url :
        The URL string to Brazilian Central Bank data api.
        The default is 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'
        where '11' is the code to CDI (Interbank Deposit Certificate) table.
    cod_bcb : integer
        The code of the desired table (see https://www.bcb.gov.br/estatisticas/indecoreestruturacao
        for a complete list.)
    dt_ini format dd/mm/yyyy
    """
    url = url.format(cod_bcb,dt_ini,dt_fim)
    cod_bcb = str(cod_bcb)
    try:
        tabela = pd.read_json(url)
        tabela['data'] = pd.to_datetime(tabela['data'], dayfirst=True)
        tabela.set_index('data', inplace=True)
    except:
        print(f"Tabela codigo {cod_bcb} não encontrada.")
        return
    
    ##valor = tabela.iloc[0]['valor']
    return tabela
    ##return valor


@st.cache_data(show_spinner="Carregando dados...", ttl=timedelta(days=1))
def get_indice_bcb(cod_bcb):

    dataFinal = datetime.now()
    dataInicial = dataFinal - timedelta(days=10)

    dataInicial = dataInicial.strftime('%d/%m/%Y')
    dataFinal = dataFinal.strftime('%d/%m/%Y')  

    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'
    """
    Parameters
    ----------
    url :
        The URL string to Brazilian Central Bank data api.
        The default is 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'
        where '11' is the code to CDI (Interbank Deposit Certificate) table.
    cod_bcb : integer
        The code of the desired table (see https://www.bcb.gov.br/estatisticas/indecoreestruturacao
        for a complete list.)
    dt_ini format dd/mm/yyyy
    """
    url = url.format(cod_bcb,dataInicial,dataFinal)
    cod_bcb = str(cod_bcb)
    try:
        tabela = pd.read_json(url)
        ##tabela['data'] = pd.to_datetime(tabela['data'], dayfirst=True)
        ##tabela.set_index('data', inplace=True)
        vlr = tabela.tail(1)['valor'].values[0]
    except:
        print(f"Tabela codigo {cod_bcb} não encontrada.")
        return
    return float(vlr)


def main():

    st.html('<h3 class="title">Indices</h3>')

    with  st.container(border=True):
        st.text('Indices econômicos')
        n = 0
        colunas = [c1, c2, c3, c4] = st.columns(4)
        keys = list(dict_indices.keys())
        
        for c in colunas:
                with c: 
                    st.html('<span class="Medio_indicator"></span>')
                    item = dict_indices[keys[n]]
                    descricao = gerar_descricao_ind(keys[n],item['descricao'])##keys[n]

                    # print(item['descricao'])
                    ind = util.get_indice_bcb(item['cod_bcb'])
                    ##st.metric(keys[n], item['texto_pre'] + f" {ind:.2f} "+item['texto_pos'])
                    st.metric(descricao, item['texto_pre'] + f" {ind} "+item['texto_pos'])

                n = n+1
                    

    with  st.container(border=True):
            st.text('Indices financeiros')
            ativos = dict_tickers.keys()

            tickers = list(map(lambda item: item['ticker'], dict_tickers.values()))
            df_info = pd.DataFrame({'Ativo': ativos,
                            'Ticker': tickers})
            df_info['Ult. Valor'] = ''
            df_info['%'] = ''
            df_info = buscar_mercado(tickers, df_info)
            colunas = [col1, col2, col3, col4] = st.columns(4)
            numero_item = 0
            for c in colunas:
                with c:
                    for linha in [0, 1, 2, 3]:
                        if (numero_item < len(tickers)):
                            descricao = gerar_descricao(dict_tickers, df_info, numero_item)
                            valor = gerar_valor(dict_tickers, df_info, numero_item)
                            variacao = str(df_info['%'][numero_item]) + '%'
                            ##st.html('<span class="Medio_indicator"></span>')
                            st.metric(descricao, valor, delta=variacao)
                            numero_item += 1
    with  st.container(border=True):
            ##st.text('Bolsas Mundiais')
            with st.spinner('Carregando bolsas Mundiais....'):
                bolsas_mundiais()

@st.cache_data(ttl=timedelta(days=1))
def busca_arquivo_paises():
     return pd.read_csv('https://raw.githubusercontent.com/robertoricci/arquivos_projetos/main/lista_paises_iso.csv')

def bolsas_mundiais():
    df = busca_arquivo_paises()

    for i, row in df.iterrows():
        try:
            variacao = buscar_mercado_unico(row['Symbol'])
            df.at[i,'Variação %'] = round(variacao,2)
            # Avisar se houve algum erro na obtenção dos dados. Se sim, não será exibido no mapa
            if pd.isna(df.at[i,'Variação %']):
                print('---->   erro em',row['Symbol'],':', df.at[i,'Variação %'],'(Não será exibido no mapa)')
        except:
            print('Erro ' + row['Symbol'])
    plotar_grafico(df)

     

def plotar_grafico(df):
    # definindo a fonte dos dados e coloração da escala
    fig = px.choropleth(df, 
                        locations="ISO-code",    # identificação das regiões (países)
                        color="Variação %",      # coluna do df para popular os valores 
                        hover_name="Country",
                        labels='Symbol',
                        range_color=[-5,5],      # limite de cores da escala. valores além deste numero terão a mesma cor do limite
                        color_continuous_scale = ["maroon","red","lightcoral","white","#96C9F4","#3FA2F6","#0F67B1"], 
                        color_continuous_midpoint=0)

    # configurações de layout, título e fontes
    fig.update_layout(
        width=1200,
        height=700,
        geo=dict(
            showframe=True,
            showcoastlines=True,
            landcolor = 'white',
            showocean=True, 
            oceancolor="azure",
            showlakes=True, 
            lakecolor="azure",
            projection_type='equirectangular'
        ),
        title={
            'text': 'Bolsas Mundiais',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        title_font_color='#525252',
        title_font_size=22,
            showlegend=True,
        font=dict(
            family='Sans-serif', 
            size=15, 
            color='#525252'
        ),
        annotations = [dict(
            x=0.5,
            y=0.25,
            xref='paper',
            yref='paper',
            text='Python para finanças',
            showarrow = False
        )]
    )

    # para mais customizações veja documentação: https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html

    st.plotly_chart(fig,use_container_width=True)
                
if __name__ == "__main__":
   main()