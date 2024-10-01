import streamlit as st
import paginas.home as app_home
import paginas.indices as app_indices
import paginas.rendafixa as app_rendafixa
import paginas.rendavariavel as app_rendavariavel
import paginas.setores_ibov as app_setores_ibov
import html_css.style as style

from streamlit_option_menu import option_menu


st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title="SFin",  # String or None. Strings get appended with "• Streamlit". 
    page_icon= 'QAF.png',  # String, anything supported by st.image, or None.
)
 #esconder botão de menu e marca dágua no rodapé
style.hidden_menu_and_footer()
 #cabeçalho detalhe superior da página 
style.headerstyle()
style.hidden_menu_deploy()

st.html("styles.html")

def main():

      
    pages= {
         "Home":page_home,
         "Indices":page_indices,
         "Renda Fixa":page_rendafixa,
         "Renda Variável":page_rendavariavel,
         "DY Por Setores":page_setores_ibov
    }

    with st.sidebar:
        style.sidebarwidth() 
        page = option_menu('Menu',['Home','Indices','Renda Fixa','Renda Variável','DY Por Setores'],
        icons=['house','bar-chart','book','pen','cash-coin'],
        default_index=0, menu_icon='app-indicator',
        styles={
                "container": {"padding": "2!important", "background-color": "#ffffff","margin": "0px" },
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"}, #,"position": "relative","display": "inline"},
                "nav-link-selected": {"background-color": "#4a7198"},
        }
    )

    pages[page]()
    with st.sidebar.expander('Sobre'):
        # Mostrar versões das bibliotecas
        #st.write(os.popen(f'python --version').read())
        #st.write('Streamlit:', st.__version__)
        #st.write('Pandas:', pd.__version__)
        #st.write('yfinance:', yf.__version__)
        #st.write('plotly:', plotly.__version__)
        #st.write('Fundamentus:', fundamentus.__version__)
        st.write('Feito com Carinho ')
        st.markdown("- Roberto Carlos Ricci")
        st.markdown("- <a href='mailto:roberto.rricci@gmail.com' target='_blank'><img src='https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white' target='_blank'> </a> ", unsafe_allow_html=True)
        st.markdown("- [![Linkedin Badge](https://img.shields.io/badge/-%40robertoricci-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://bit.ly/lirobertocarlosricci)](https://bit.ly/lirobertocarlosricci)")


def page_home():
     app_home.home()

def page_indices():
    app_indices.main()

def page_indices():
    app_indices.main()


def page_rendafixa():
    app_rendafixa.main()

def page_rendavariavel():
    app_rendavariavel.main()


def page_setores_ibov():
    app_setores_ibov.main()


if __name__ == "__main__":
   main()

