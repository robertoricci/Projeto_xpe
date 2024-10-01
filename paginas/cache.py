import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from bd.postgree import RDSPostgreSQLManager


def busca_dados_acoes():

    df = buscar_acoes_bd()
    st.session_state["lista_acoes"] = df
    return df


@st.cache_data(show_spinner="Buscando dados dos tickers", ttl=3600)
def buscar_acoes_bd():
   
    query = """ select  
         null  AS IMAGE
         ,ticker as "TICKER"
        ,companyname as "NOME"
        ,COALESCE (dy,NULL,0,dy) AS "DY"
        ,COALESCE (price,NULL,0,price) as "PRICE"
        ,COALESCE (p_l,NULL,0,p_l) as "P/L"
        ,COALESCE (p_vp,NULL,0,p_vp) as "P/VP"
        ,COALESCE (p_ebit,NULL,p_ebit) as "P/EBIT"
        ,COALESCE (p_ativo,NULL,p_ativo) as "P/ATIVOS"
        ,COALESCE (ev_ebit,NULL,0,ev_ebit) as "EV/EBIT"
        ,COALESCE (margembruta,NULL,0,margembruta) AS "Marg. Bruta"
        ,COALESCE (margemebit,NULL,0,margemebit) AS "Marg. EBIT"
        ,COALESCE (margemliquida,NULL,0,margemliquida) AS "Marg. Liquida"
        ,COALESCE (p_sr,NULL,0,p_sr)            AS "P/SR"
        ,COALESCE (p_capitalgiro,NULL,0,p_capitalgiro) AS "P/Cap Giro"
        ,COALESCE (p_ativocirculante,NULL,0,p_ativocirculante) AS "Preço sobre Ativo"
        ,COALESCE (giroativos,NULL,0,giroativos) AS "Giro ativos"
        ,COALESCE (roe,NULL,0,roe) AS "ROE"
        ,COALESCE (roa,NULL,0,roa) AS "ROA"
        ,COALESCE (roic,NULL,0,roic) AS "ROIC"
        ,COALESCE (dividaliquidapatrimonioliquido,NULL,0,dividaliquidapatrimonioliquido) AS "DIV. Liquida/Patrimomio"
        ,COALESCE (dividaliquidaebit,NULL,0,dividaliquidaebit) AS "Div. liquida/EBIT"
        ,COALESCE (pl_ativo,NULL,0,pl_ativo) AS "PL/Ativo"
        ,COALESCE (passivo_ativo,NULL,0,passivo_ativo) AS "Passivo/Ativo"
        ,COALESCE (liquidezcorrente,NULL,0,liquidezcorrente) AS "Liq. Corrente"
        ,COALESCE (peg_ratio,NULL,0,peg_ratio) AS "PEG Ratio"
        ,COALESCE (receitas_cagr5,NULL,0,receitas_cagr5) AS "CAGR Receitas 5 Anos"
        ,COALESCE (liquidezmediadiaria,NULL,0,liquidezmediadiaria) AS "Liquidez Diaria"
        ,COALESCE (vpa,NULL,0,vpa) AS "VPA"
        ,COALESCE (lpa,NULL,0,lpa) AS "LPA"
        ,COALESCE (valormercado,NULL,0,valormercado) AS "Valor Mercado"
        ,COALESCE (lucros_cagr5,NULL,0,lucros_cagr5) AS "CAGR Lucros 5 Anos"
        ,COALESCE(sectorid,NULL,0,sectorid) AS "ID Setor"
        ,COALESCE(sectorname,NULL,'OUTROS',sectorname) AS "SETOR"
        from public.acao_stinv """
    
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)

    return df

def busca_dados_setores():
    query = """
        select
        distinct
         cast(COALESCE(sectorid,null,0,sectorid) AS INTEGER) as id
        ,COALESCE(sectorname,NULL,'OUTROS',sectorname) as nome
        from public.acao_stinv """
    

    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df


def busca_dados_setores_fii():

    query = """
        select
        distinct
        cast(COALESCE(segmentid,null,0,segmentid) AS INTEGER) as id
        ,COALESCE(segment,NULL,'OUTROS',segment) as nome
        from public.fii_stinv """
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df

def busca_df_acoes_do_cache():
    if "lista_acoes" not in st.session_state:
        df = busca_dados_acoes()
        #df = df.ffill(0)
        ##df = df.ffill(value=np.nan)
        #df = df.replace({None: 0})
        st.session_state["lista_acoes"] = df
    else:
        df = st.session_state["lista_acoes"]
    return df



def busca_df_setores_do_cache():
    if "lista_setores" not in st.session_state:
        df = busca_dados_setores()
        st.session_state["lista_setores"] = df
    else:
        df = st.session_state["lista_setores"]
    return df



def busca_df_setores_fii_do_cache():
    if "lista_setores_fii" not in st.session_state:
        df = busca_dados_setores_fii()
        st.session_state["lista_setores_fii"] = df
    else:
        df = st.session_state["lista_setores_fii"]
    return df


@st.cache_data(show_spinner="Buscando dados dos setores", ttl=3600)
def buscar_df_setores_dy():
    query = """select 
         ticker as ticker
        ,'https://raw.githubusercontent.com/robertoricci/icon-b3/main/icon/'||ticker||'.png' as image
        ,companyname as "nome"
         ,sectorname AS "Setor"
        ,subsectorname AS "SubSetor"
        ,dy         AS "DY"
    from public.acao_stinv
    where dy is not null"""
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df
    return df


@st.cache_data(show_spinner="Buscando dados dos FIIS", ttl=3600)
def buscar_fii_bd():
   
    query = """select 
       ticker as "Ticker"
    ,companyname as "Nome"
    ,COALESCE(price,null,0,price)  as "Preco"
    ,CASE gestao
     WHEN 1 then 'Passiva'
     ELSE 'Ativa'
     END  as "Gestao"
    ,COALESCE(dy,null,0,dy )     as "DY"
    ,COALESCE(p_vp,null,0,p_vp)    AS "P/VP"
    ,COALESCE(valorpatrimonialcota,null,0,valorpatrimonialcota)  AS "Vlr Patr/Cot"
    ,COALESCE(liquidezmediadiaria,null,0,liquidezmediadiaria)  AS "Liq. Media Diaria"
    ,COALESCE(percentualcaixa,null,0,percentualcaixa)     AS "Perc do Caixa"
    ,COALESCE(dividend_cagr,null,0,dividend_cagr )      AS "DY CAGR 3 Anos"
    ,COALESCE(cota_cagr ,null,0,cota_cagr)         AS "Vlr CAGR 3 Anos"
    ,COALESCE(numerocotistas,null,0,numerocotistas)    AS "Nº Cotistas"
    ,COALESCE(numerocotas,null,0,numerocotas )       AS "Nº de Cotas"   
    ,COALESCE(patrimonio ,null,0,patrimonio )       AS "Patrimonio"    
    ,COALESCE(lastdividend,null,0,lastdividend)      AS "Ultimo Rendimento"
    ,segment                                          AS "Segmento"
    from public.fii_stinv"""
    
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return  df


def busca_df_fii_do_cache():
    if "lista_fii" not in st.session_state:
        df = buscar_fii_bd()
        #df = df.ffill(0)
        ##df = df.ffill(value=np.nan)
        #df = df.replace({None: 0})
        st.session_state["lista_fii"] = df
    else:
        df = st.session_state["lista_fii"]
    return df

