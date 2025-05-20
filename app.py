import streamlit as st
import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages import data_upload, dashboard, models, visualizations, documentation
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Análisis Predictivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        max-width: 100%;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #3498db;
        color: white;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #262730;
        color: white;
        text-align: center;
        padding: 1rem;
        font-size: 0.8rem;
    }
    .stPlotlyChart {
        width: 100%;
    }
    .stDataFrame {
        width: 100%;
    }
    .stMetric {
        width: 100%;
    }
    .stRadio > div {
        width: 100%;
    }
    .stSelectbox > div {
        width: 100%;
    }
    .stMultiselect > div {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Menú lateral
with st.sidebar:
    st.title("📊 Análisis Predictivo")
    st.markdown("---")
    
    # Navegación
    page = st.radio(
        "Navegación",
        ["Inicio", "Cargar Datos", "Dashboard", "Modelos", "Visualizaciones", "Documentación"]
    )
    
    st.markdown("---")
    st.markdown("### Desarrollado por:")
    st.markdown("""
    - Santiago Ramirez Forero
    - Macjainer Molano Ramos
    """)

# Contenido principal
if page == "Inicio":
    st.title("Bienvenido al Sistema de Análisis Predictivo")
    st.markdown("""
    Este sistema te permite:
    - Cargar y visualizar datos
    - Realizar análisis exploratorio
    - Entrenar modelos predictivos
    - Visualizar resultados
    
    Para comenzar, selecciona una opción en el menú lateral.
    """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        Desarrollado por Santiago Ramirez Forero y Macjainer Molano Ramos
    </div>
    """, unsafe_allow_html=True)
    
elif page == "Cargar Datos":
    data_upload.show()
elif page == "Dashboard":
    dashboard.show()
elif page == "Modelos":
    models.show()
elif page == "Visualizaciones":
    visualizations.show()
elif page == "Documentación":
    documentation.show()
