import streamlit as st
import pandas as pd
import util.util as util
from .cache import busca_dados_acoes,busca_df_acoes_do_cache,busca_df_setores_do_cache,busca_df_fii_do_cache,busca_df_setores_fii_do_cache
from util.util import monta_item_filtro
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def  mostrar_filtros_acoes(filtros, itens_col1, itens_col2, itens_col3):
  
   df_tickers = busca_df_acoes_do_cache().copy()
   col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

   with col1:

      for item in itens_col1:
         coluna = item.get("coluna")
         label = item.get("label")
         help = item.get("help")

         filtros[coluna] = monta_item_filtro(
               df_tickers, coluna, label, "input_number", ajuda=help, formato=None
         )

      setores = busca_df_setores_do_cache()
     
      filtros["setores"] = st.multiselect(
              "Setor(es):", sorted(setores['nome']),[], key='setores'
          )
      
      filtros["ticker"] = st.multiselect(
              "Ticker:", sorted(df_tickers['TICKER']),[], key='ticker'
          )
      
   with col2:
        for item in itens_col2:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = monta_item_filtro(
                df_tickers, coluna, label, "input_number", ajuda=help, formato=None
            )
        st.write('')
        st.write('')
        filtros["Apenas com liquidez media acima de 1 milhão"] = st.checkbox(
         "Apenas com liquidez media acima de 1 milhão",
         False,
         help="Apenas com liquidez media acima de 1 milhão",
      )
   with col3:
        for item in itens_col3:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = monta_item_filtro(
                df_tickers, coluna, label, "input_number", ajuda=help, formato=None
            )



def filtrar_df_acoes(filtros, itens_col1, itens_col2, itens_col3):
         """Filtrar as ações de acordo com os filtros informados."""
         df_tickers = busca_df_acoes_do_cache().copy()
         
         if filtros["Apenas com liquidez media acima de 1 milhão"]:
            df_tickers = df_tickers.loc[df_tickers["Liquidez Diaria"] > 100000]

         #filtrar por setores
         if filtros["setores"] != []:
             df_tickers = df_tickers.loc[df_tickers["SETOR"].isin(filtros["setores"])]


               #filtrar por setores
         if filtros["ticker"] != []:
             df_tickers = df_tickers.loc[df_tickers["TICKER"].isin(filtros["ticker"])]


         for item in itens_col1 + itens_col2 + itens_col3:
            coluna = item.get("coluna")
            minimo = float(filtros[coluna].get("minimo"))
            maximo = float(filtros[coluna].get("maximo"))
      
            if minimo > maximo:
               frase = f"Para o campo {coluna} o valor mínimo está maior que o valor máximo! Corrija o seu filtro!"
               print(frase)
               st.info(
                     frase,
                     icon="⚠️",
               )
               st.stop()

            df_tickers = df_tickers[df_tickers[coluna].between(minimo, maximo)]

         df_tickers.set_index("TICKER", drop=True, inplace=True)
         return df_tickers

def habilita_tab_graf(df, titulo, graficos, numero_colunas, numero_linhas):
      fig = make_subplots(
         rows=numero_linhas, cols=numero_colunas, subplot_titles=graficos
      )

      col_atual = 1
      row_atual = 1

      for g in graficos:
         fig.add_trace(
               go.Bar(x=df.index, y=df[g], name=g),
               row=row_atual,
               col=col_atual,
         )
         fig.add_hline(
               y=df[g].mean(),
               line_dash="dot",
               annotation_text="Média",
               annotation_position="bottom right",
               row=row_atual,
               col=col_atual,
         )

         if col_atual == numero_colunas:
               row_atual += 1
               col_atual = 1
         else:
               col_atual += 1

      fig.update_layout(
            height=800,
            width=1200,
            title_text=titulo,
      )

      st.plotly_chart(fig)


def habilitar_tab_acoes():

    itens_col1 = [
        {"coluna": "PRICE", "label": "Preço (R$)", "help": "Valor em R$"},
        {"coluna": "DY", "label": "Div. Yield (%)", "help": "Valor %"},
        {"coluna": "P/VP", "label": "P/VP Ação", "help": ""},
        {"coluna": "P/ATIVOS", "label": "P/Ativo", "help": ""},
        {"coluna": "Marg. EBIT", "label": "Mrg Ebit (%)", "help": "Valor %"},
        {"coluna": "Marg. Bruta", "label": "Mrg Bruta (%)", "help": "Valor %"},
        {"coluna": "ROIC", "label": "ROIC (%)", "help": "Valor %"},
    ]

    itens_col2 = [
        {"coluna": "Valor Mercado", "label": "Vlr de Mercado", "help": ""},
        {"coluna": "P/SR", "label": "PSR", "help": ""},
        {"coluna": "P/Cap Giro", "label": "P/Cap. Giro", "help": ""},
        {"coluna": "EV/EBIT", "label": "EV/EBIT", "help": ""},
        {"coluna": "Marg. Liquida", "label": "Margem Líq.", "help": "Valor %"},
        {"coluna": "ROE", "label": "ROE (%)", "help": "Valor %"},
        {"coluna": "DIV. Liquida/Patrimomio", "label": "Dív. liquida/Patrim.", "help": ""},
    ]

    itens_col3 = [
        {"coluna": "P/L", "label": "P/L", "help": ""},
        {"coluna": "Preço sobre Ativo", "label": "P/Ativ Circ. Liq.", "help": ""},
        {"coluna": "P/EBIT", "label": "P/EBIT", "help": ""},
        {"coluna": "Passivo/Ativo", "label": "PASSIVOS / ATIVOS", "help": ""},
        {"coluna": "Div. liquida/EBIT", "label": "Div. Liquida", "help": ""},
        {"coluna": "Liq. Corrente", "label": "Liq. 2 meses", "help": ""},
        {"coluna": "Liquidez Diaria",      "label": "Liq. Med. Diária",    "help": "",   },
    ]
    st.write("## Ações")

    filtros = {}

    with st.form("form_acoes"):
        mostrar_filtros_acoes(filtros, itens_col1, itens_col2, itens_col3)

        filtrar_acoes = st.form_submit_button("Filtrar")
        if filtrar_acoes:
            
            tab_resul, tab_graf = st.tabs(
               [
                  ":memo: Resultados",
                  ":bar_chart: Gráficos",
               ]
            )
            
            with tab_resul:
                st.write('Resultados')
                df = filtrar_df_acoes(filtros, itens_col1, itens_col2, itens_col3)
                
                total_registro =  df.shape[0]##df.count().unique()[1]
                df['image'] = 'https://raw.githubusercontent.com/robertoricci/icon-b3/main/icon/'+df.index+'.png'
                st.dataframe(df,hide_index= False, column_config={"image": st.column_config.ImageColumn(help='IMag'), 
                                                'Valor Mercado': st.column_config.NumberColumn( "Valor Mercado",help="Valor Mercado",format="%f")}
                             ,use_container_width=True)
                st.write("#### " + str(total_registro) + " registros selecionados")

            with tab_graf:
               st.write('graficos')
               titulo = "Gráficos sobre os Tickers selecionados"
               graficos = [
                     "PRICE",
                     "P/L",
                     "P/VP",
                     "DY",
                     "ROIC",
                     "ROE",
                     "Liq. Corrente",
                     "P/ATIVOS"
               ]

               habilita_tab_graf(df, titulo, graficos, 3, 3)


def buscar_lista_acoes():
   df_tickers = pd.read_csv("tickers_ibra.csv",sep=',',skiprows=1,index_col=False)
   df_tickers.rename(columns={'Unnamed: 0': 'Index', '0': 'Ticker'}, inplace=True)
   return df_tickers


def filtrar_df_fii(filtros, itens_col1, itens_col2, itens_col3):
         """Filtrar as fundos de acordo com os filtros informados."""
         df_tickers = busca_df_fii_do_cache().copy()


           #filtrar por setores
         if filtros["gestao"] != []:
             df_tickers = df_tickers.loc[df_tickers["Gestao"].isin(filtros["gestao"])]
         

         #filtrar por setores
         if filtros["setores"] != []:
             df_tickers = df_tickers.loc[df_tickers["Segmento"].isin(filtros["setores"])]


               #filtrar por setores
         if filtros["ticker"] != []:
             df_tickers = df_tickers.loc[df_tickers["Ticker"].isin(filtros["ticker"])]


         for item in itens_col1 + itens_col2 + itens_col3:
            coluna = item.get("coluna")
            minimo = float(filtros[coluna].get("minimo"))
            maximo = float(filtros[coluna].get("maximo"))
      
            if minimo > maximo:
               frase = f"Para o campo {coluna} o valor mínimo está maior que o valor máximo! Corrija o seu filtro!"
               print(frase)
               st.info(
                     frase,
                     icon="⚠️",
               )
               st.stop()

            df_tickers = df_tickers[df_tickers[coluna].between(minimo, maximo)]

         df_tickers.set_index("Ticker", drop=True, inplace=True)
         return df_tickers

def  mostrar_filtros_fii(filtros, itens_col1, itens_col2, itens_col3):
   
    df_tickers = busca_df_fii_do_cache().copy()
   
    col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

    with col1:

        for item in itens_col1:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = monta_item_filtro(
                df_tickers, coluna, label, "input_number", ajuda=help, formato=None
            )

        filtros["gestao"] = st.multiselect(
                "Gestão:", ['Ativa','Passiva'],[], key='gestao'
            )
        
    
        filtros["setores"] = st.multiselect(
                "Segmentos:", sorted(df_tickers['Segmento'].unique()),[], key='setoresfi'
            )
    
        filtros["ticker"] = st.multiselect(
                "Ticker:", sorted(df_tickers['Ticker']),[], key='tickerfi'
            )
        
    with col2:
        for item in itens_col2:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = monta_item_filtro(
                df_tickers, coluna, label, "input_number", ajuda=help, formato=None
            )
        st.write('')
        st.write('')
    with col3:
        for item in itens_col3:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = monta_item_filtro(
                df_tickers, coluna, label, "input_number", ajuda=help, formato=None
            )



def habilitar_tab_fii():
     
        itens_col1 = [
            {"coluna": "Preco", "label": "Preço (R$) ", "help": "Valor em R$"},
            {"coluna": "DY", "label": "Div. Yield (%) ", "help": "Valor %"},
           ## {"coluna": "Gestao", "label": "Gestão ", "help": ""},
            {"coluna": "P/VP", "label": "P/VP ", "help": ""}
        ]

        itens_col2 = [
            {"coluna": "Vlr Patr/Cot", "label": "Vlr Patr/Cot", "help": ""},
            {"coluna": "Liq. Media Diaria", "label": "Liq. Media Diaria", "help": ""},
            {"coluna": "Perc do Caixa", "label": "Perc do Caixa", "help": ""},
            {"coluna": "DY CAGR 3 Anos", "label": "DY CAGR 3 Anos", "help": ""},
        ]

        itens_col3 = [
            {"coluna": "Nº Cotistas", "label": "Nº Cotistas", "help": ""},
            {"coluna": "Patrimonio", "label": "P/Ativ Circ. Liq.", "help": ""},
            {"coluna": "Nº de Cotas", "label": "Nº de Cotas", "help": ""},
            {"coluna": "Ultimo Rendimento", "label": "Ultimo Rendimento", "help": ""},
        ]
        st.write("## FII")

        filtros = {}

        with st.form("form_fii"):
            mostrar_filtros_fii(filtros, itens_col1, itens_col2, itens_col3)

            filtrar_fii = st.form_submit_button("Filtrar")

            if filtrar_fii:
                ##st.write('Resultados')
                df = filtrar_df_fii(filtros, itens_col1, itens_col2, itens_col3)

                st.dataframe(df)
                total_registro =  df.shape[0]##df.count().unique()[1]
                st.write("#### " + str(total_registro) + " registros selecionados")

            ##tickers = busca_df_fii_do_cache()
            ##st.dataframe(tickers)
            ##df = filtrar_df_fii(filtros, itens_col1, itens_col2, itens_col3)
            ##st.dataframe(df)

def mostrar_tab_acoes():
   habilitar_tab_acoes()
   ##tickers = busca_dados_acoes()
   ##st.dataframe(tickers)

def mostrar_tab_fiis():
    habilitar_tab_fii()
   



def main():
   st.html('<h3 class="title">Renda Variavel</h3>')

   # c1,c2 = st.columns(2)
   # st.divider()
   # tickers = buscar_lista_acoes()
   # tickers[:0]

   # # tickers = [t+".SA" for t in tickers]

   # # df_info = pd.DataFrame({'Ticker': tickers,'Valor':'','%':''})
            
   # # df_info = util.buscar_dados_tickers(tickers,df_info)

   # #calcular % 

   # with c1:
   #    st.text('Maiores Altas')
   #    st.dataframe(tickers)

   # with c2:
   #    st.text('Maiores baixas')
   #    st.dataframe(tickers)


   tab_acoes, tab_fiis = st.tabs(["Ações", "FIIs"])
   with tab_acoes:
            mostrar_tab_acoes()

   with tab_fiis:
            mostrar_tab_fiis()
           




if __name__ == "__main__":
   main()