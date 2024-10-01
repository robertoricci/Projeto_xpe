import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

#esconder botões do streamlit
def hidden_menu_and_footer():
    hide_menu = '''
    <style>
    #MainMenu {
        visibility:hidden;
    }
    footer{
        visibility:hidden;
    }
    </style>
    '''
    st.markdown(hide_menu, unsafe_allow_html=True)

#linha no cabeçalho branca desing
def headerstyle():
    st.markdown(
    f"""
    <nav class="navbar fixed-top navbar-light bg-white" style="color: #ffffff; padding: 0.8rem 1rem;">
        <span class="navbar-brand mb-0 h1" " >  </span>
    </nav>
    """, unsafe_allow_html=True
    )


#espaço entre plots
def space(tamanho):
    if tamanho == 1:
        st.title('')
    if tamanho == 2:
        st.header('') 
    if tamanho == 3:
        st.write('') 

def sidebarwidth():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 250px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 250px;
            margin-left: -500px;
        }
        .st-c9:hover {
         color: rgb(14, 121, 228);
        }
       
        </style>
        """,
        unsafe_allow_html=True,
        )    

def font_google():
    st.markdown(
            """
            <style>
    @font-face {
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    src: url(https://fonts.gstatic.com/s/tangerine/v12/IurY6Y5j_oScZZow4VOxCZZM.woff2) format('woff2');
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
        html, body, [class*="css"]  {
        font-family: 'Roboto';
        font-size: 48px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
    
def button():
    butttom = '''
    <style>
    .stButton > button{
        color: #ffffff;
        background-color: rgb(74, 113, 152);
    }
   .stButton > button:hover{
        color: #ffffff;
        background-color: rgb(14, 121, 228);
        border-color: rgb(85, 115, 146);
    }
    .svg:hover {
        fill: rgb(14, 121, 228);;
    }
    </style>
    '''
    st.markdown(butttom, unsafe_allow_html=True)



#esconder botões do streamlit
def hidden_menu_deploy():
    hide_menu = '''
    <style>
        [data-testid="stToolbar"]{
        display: none;
        visibility: hidden;
    }
    </style>
    '''
    st.markdown(hide_menu, unsafe_allow_html=True)