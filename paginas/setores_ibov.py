import streamlit as st
from .cache import buscar_df_setores_dy
import plotly.express as px
import plotly.graph_objects as go


def main():
    st.html('<h3 class="title">Análise de DY por Setor/SubSetor</h3>')

    df_ticker_ibov = buscar_df_setores_dy()


    col1,col2 = st.columns([12,1]) 
          
    with col1:  
        df_ticker_ibov['ticker_dy'] = df_ticker_ibov.apply(lambda x:  (x['ticker']+' - '+str(x['DY'])+'%' ), axis=1)
        st.markdown("<h2 style='text-align: center; color: grey;'>DY - Por Setor/SubSetor</h2>", unsafe_allow_html=True)

        fig = px.sunburst(df_ticker_ibov, path=['Setor', 'SubSetor', 'ticker_dy'], values='DY', height=900,width=1300)

        fig.update_traces(textfont_color='white',
        textfont_size=14,
        ##hovertemplate='<b>%{label}:</b> %{value:.2f}%')
        hovertemplate='<b>%{label}:</b>')

        st.plotly_chart(fig)

        # st.markdown("<h1 style='text-align: center; color: grey;'>Participação do IBOV</h1>", unsafe_allow_html=True)

        # fig = px.treemap(df_ibov, path=['Setor', 'SubSetor', 'ticker'], values='part', height=900,width=1300)

        # fig.update_traces(textfont_color='white',
        # textfont_size=14,
        # hovertemplate='<b>%{label}:</b> %{value:.2f}%')
        # st.plotly_chart(fig)

        st.write('Análise de DY por Setor/SubSetor - Tabela')
        c1,c2 = st.columns(2) 
        df_ticker_ibov.drop(columns=['ticker_dy'],inplace=True)
        with c1:
            setores = st.multiselect(
                "Setor(es):", sorted(df_ticker_ibov['Setor'].unique()),[], key='setores')
        with c2:
            if setores != []:
                df_ticker_ibov = df_ticker_ibov.loc[df_ticker_ibov["Setor"].isin(setores)]
        
            subsetores = st.multiselect(
                "SubSetor(es):", sorted(df_ticker_ibov['SubSetor'].unique()),[], key='subsetores')

        if setores != []:
             df_ticker_ibov = df_ticker_ibov.loc[df_ticker_ibov["Setor"].isin(setores)]


        if subsetores != []:
             df_ticker_ibov = df_ticker_ibov.loc[df_ticker_ibov["SubSetor"].isin(subsetores)]
        
        st.dataframe(df_ticker_ibov,
                     hide_index=True,
                     use_container_width=False,
                       column_config={"image": st.column_config.ImageColumn(help='IMag')}
                    )
        st.write("#### " + str(df_ticker_ibov.shape[0]) + " registros selecionados")

        
