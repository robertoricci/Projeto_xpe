import streamlit as st
import pandas as pd
from datetime import date,datetime, timedelta
import yfinance as yf
from typing import Any, Dict



@st.cache_data(show_spinner="Carregando dados...", ttl=60*5)
def get_indice_bcb(cod_bcb):

    dataFinal = datetime.now()
    dataInicial = dataFinal - timedelta(days=70)

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



@st.cache_data(show_spinner="Carregando dados...", ttl=60*5)
def buscar_dados_tickers(tickers, df_info):
    count = 0
    for ticker in tickers:
        print(tickers)
        cotacoes = yf.download(ticker, period='5d')['Adj Close']
        variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
        df_info['Valor'][count] = round(cotacoes.iloc[-1], 2)
        df_info['%'][count] = round(variacao, 2)
        count += 1
    return df_info




def monta_item_filtro(
    df, coluna: str, label: str, widget: str, ajuda=None, formato=None
) -> Dict[str, Any]:
    if coluna not in df.columns:
        st.error(f"Coluna {coluna} não existe no DataFrame")
        st.stop()

    if widget is None:
        widget = "slider"

    if widget.lower() not in ["slider", "input_number"]:
        st.error(f"Widget {widget} não é slider ou input_number")
        st.stop()

    menor = float(df[coluna].min(numeric_only=True))
    maior = float(df[coluna].max(numeric_only=True))

    if widget == "slider":
        filtro_min, filtro_max = st.slider(
            label,
            menor,
            maior,
            (menor, maior),
            step=1.0,
            format=formato,
            help=ajuda,
            key=f"{coluna}{label}_slider",
        )

    else:
        col_min, col_max = st.columns(2)
        with col_min:
            filtro_min = st.number_input(
                f"{label} mínimo",
                min_value=menor,
                value=menor,
                step=1.0,
                key=f"{coluna}{label}_min",
            )
        with col_max:
            filtro_max = st.number_input(
                f"{label} máximo",
                max_value=maior,
                value=maior,
                step=1.0,
                help=ajuda,
                key=f"{coluna}{label}_max",
            )

    return {
        "minimo": filtro_min,
        "maximo": filtro_max,
    }