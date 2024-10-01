import streamlit as st
import pandas as pd
from streamlit_extras.card import card

import util.util as util

import altair as alt



# Criação da tabela de IR
tabela_ir = pd.DataFrame({
    "Período de Aplicação": ["Até 180 dias", "De 181 a 360 dias", "De 361 a 720 dias", "Acima de 720 dias"],
    "Alíquota IR": [22.5, 20, 17.5, 15]
})



def calcular_rentabilidade_cdb(tempo_meses, taxa_anual, capital_inicial, tabela_ir):

    # Converter taxa anual para mensal
    taxa_anual = taxa_anual/100
    taxa_mensal = (1 + taxa_anual)**(1/12) - 1
    print(f"Taxa anual: {taxa_anual*100:.2f}%")
    print(f"Taxa mensal: {taxa_mensal*100:.2f}%")

    # Calcular o valor final bruto diretamente com o tempo em meses
    valor_final_bruto = capital_inicial * (1 + taxa_mensal) ** tempo_meses
    print(f"Valor final bruto: R$ {valor_final_bruto:.2f}")

    # Determinar a alíquota de IR com base no tempo em meses
    if tempo_meses <= 6:
        aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'Até 180 dias', 'Alíquota IR'].iloc[0]
    elif tempo_meses <= 12:
        aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'De 181 a 360 dias', 'Alíquota IR'].iloc[0]
    elif tempo_meses <= 24:
        aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'De 361 a 720 dias', 'Alíquota IR'].iloc[0]
    else:
        aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'Acima de 720 dias', 'Alíquota IR'].iloc[0]
    print(f"Alíquota de IR aplicável: {aliquota_ir}%")

    # Calcular o IR sobre o rendimento
    rendimento_bruto = valor_final_bruto - capital_inicial
    imposto_devido = rendimento_bruto * (aliquota_ir / 100)
    print(f"Imposto devido sobre o rendimento: R$ {imposto_devido:.2f}")

    # Calcular o valor final líquido
    valor_final_liquido = valor_final_bruto - imposto_devido

    return rendimento_bruto,valor_final_bruto,valor_final_liquido,imposto_devido,aliquota_ir



def validar_parametros(meses,taxa_anual,capital_inicial,mensagens):
    if not meses:
        mensagens.error("meses não informado.", icon="🚨")
        st.stop()
    if taxa_anual < 0:
        mensagens.error("Taxa invalida.", icon="🚨")
        st.stop()
    if not capital_inicial:
        mensagens.error("Capital inicial não informado.", icon="🚨")
        st.stop()


def roundster (x):
     return "{:.2f}".format(x)


def format_brl(x):
            return f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

def main():

   
    st.html('<h3 class="title">Renda Fixa</h3>')

    im, im1,im3 = st.columns(3)

    im.image('./img/iof.png',width=400, caption='Tabela Progressiva de IOF sobre retirada')
    im1.image('./img/ir.png',width=500, caption='Tabela Progressiva de IR Sobre o lucro')

    with  st.container(border=True):

        st.text('Calculando rentabilidade de um CDB - já descontando o IR - conforme tabela de aliquotas')
        st.text('Aplicação retiradas antes de 30 dias, incide IOF')

        pre_pos = st.radio(
            "É PRÉ fixado ou PÓS fixado? 👇",
            ["PRE", "CDI", "IPCA"],
            key="visibility",
            ##label_visibility=st.session_state.visibility,
            horizontal=True)
        
        tipo = st.radio(
            "Tipo de investimento 👇",
            ["LCI/LCA", "CDB/LC"],
            key="2",
            ##label_visibility=st.session_state.visibility,
            horizontal=True)

        col1, col2 = st.columns(2)
        mensagens = st.container()
    
        
        st.write("You selected:", pre_pos)

        taxa = 10.0
        if pre_pos == "CDI":
            taxa = util.get_indice_bcb(1178)
        elif pre_pos == "IPCA":
            taxa = util.get_indice_bcb(13522)


        valor_inicio    = col1.number_input('Valor Inicial', min_value = 0, value = 1000)
        valor_aportes   = col2.number_input('Aporte Mensal', min_value = 0, value = 100)
        taxa_anual      = col1.number_input(label='Juros Anual % ' + pre_pos + f'({taxa})',step=1.,format="%.2f", value = taxa)
        periodo         = col2.number_input('Período em meses', min_value = 0, max_value=500, value = 12)
        #periodo mensal
        ###periodo = int(periodo * 12)
        st.text(periodo)
        taxa_anual = taxa_anual/100
        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1


        df = pd.DataFrame(0, range(periodo+1), columns = ['Juros', 'Total Investido', 'Total Juros','Total Acumulado'])


        #Ajustando o valor inicial para o valor informado
        df.index.name = 'Mês'
        df.reset_index(inplace=True)

        df.at[0, 'Total Investido'] = float(valor_inicio)
        df.at[0, 'Total Acumulado'] = float(valor_inicio)
       
   
        for i in range(1, periodo + 1):
            df['Juros'][i] = float(roundster(df['Total Acumulado'][i-1] * taxa_mensal))
            df['Total Investido'][i] = float(valor_inicio + (i * valor_aportes))
            df['Total Juros'][i] = float(df['Juros'][i]) + float(df['Total Juros'][i-1])
            df['Total Acumulado'][i] = df['Total Investido'][i] + df['Total Juros'][i]
      
        if tipo != "LCI/LCA":
                if periodo <= 6:
                    aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'Até 180 dias', 'Alíquota IR'].iloc[0]
                elif periodo <= 12:
                    aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'De 181 a 360 dias', 'Alíquota IR'].iloc[0]
                elif periodo <= 24:
                    aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'De 361 a 720 dias', 'Alíquota IR'].iloc[0]
                else:
                    aliquota_ir = tabela_ir.loc[tabela_ir['Período de Aplicação'] == 'Acima de 720 dias', 'Alíquota IR'].iloc[0]
                print(f"Alíquota de IR aplicável: {aliquota_ir}%")

                # Calcular o IR sobre o rendimento
                total_juros = df.at[periodo, 'Total Juros']
                imposto_devido = total_juros * (aliquota_ir / 100)
                # Calcular o valor final líquido
                valor_final_liquido = df.at[periodo, 'Total Acumulado'] - imposto_devido
        else:
            # Não tem imposto
            total_juros = df.at[periodo, 'Total Juros']
            imposto_devido = 0
            # Calcular o valor final líquido
            valor_final_liquido = df.at[periodo, 'Total Acumulado'] - imposto_devido
            aliquota_ir = 0

     

        c1, c2, c3 = st.columns(3)
        #st.html('<span class="blue_metric_value"></span>')
        with c1:
            st.html('<span class="blue_metric_value"></span>')
            st.metric('Valor Total Bruto', format_brl(df.at[periodo, 'Total Acumulado']))
        with c2:
            st.metric('Valor investido', format_brl(df.at[periodo, 'Total Investido']))
        with c3:
            st.metric('Valor em juros', format_brl(total_juros))


        c1, c2, c3 = st.columns(3)

        with c1:
            #st.html('<span class="green_metric_value"></span>')
            st.metric("IR sobre rentabilidade", f"Alíquota de IR : {aliquota_ir} %")

        with c2:
        
            st.metric("Valor pago IR", format_brl(imposto_devido))

        with c3:
            st.html('<span class="green_metric_value"></span>')
            st.metric("Valor Total Liquido", format_brl(valor_final_liquido))

  
        tab1, tab2 = st.tabs(["🗃 Tabela", "📈 Grafico"])

        with tab1:
            st.subheader('Tabela de dados')
            st.dataframe(df, height=500, hide_index=True)

      

        with tab2:
            df_melted = df.melt(id_vars='Mês', value_vars=['Total Investido', 'Total Juros'], 
                        var_name='Tipo', value_name='Valor')

            # Create the stacked bar chart with custom order for the stack
            bar_chart = alt.Chart(df_melted).mark_bar().encode(
                x=alt.X('Mês:O', title='Mês'),
                y=alt.Y('Valor:Q', title='Valor (R$)', stack='zero'),
                color=alt.Color('Tipo:N', title='Tipo', sort=['Total Investido', 'Total Juros']),
                order=alt.Order('key:N',sort='descending'),
                tooltip=['Mês', 'Tipo', 'Valor']
            ).properties(
                title='Evolução Patrimonial - Total Investido vs Total Juros',
                width=800,
                height=400
            )

                    # Create DataFrame for pie chart
            pie_data = pd.DataFrame({
                'Tipo': ['Total Juros', 'Total Investido'],
                'Valor': [roundster(df.at[periodo, 'Total Juros']), df.at[periodo, 'Total Investido']]
            })
            # Create the pie chart
            pie_chart = alt.Chart(pie_data).mark_arc().encode(
                theta = 'Valor',
                color = 'Tipo'
            ).properties(
                title='Evolução Patrimonial - Total Investido vs Total Juros',
                width=500,
                height=300
            )


            # Display the charts in Streamlit

            st.altair_chart(pie_chart, use_container_width=True)
            st.altair_chart(bar_chart, use_container_width=True)



if __name__ == "__main__":
   main()