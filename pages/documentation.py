import streamlit as st
import os
from dotenv import load_dotenv
import base64
from fpdf import FPDF
import tempfile
import unicodedata
from pages.utils import load_from_db, get_available_tables

def remove_accents(text):
    """Elimina acentos y caracteres especiales del texto"""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text

def create_pdf():
    # Crear PDF con soporte UTF-8
    pdf = FPDF()
    pdf.add_page()
    
    # Configurar fuente
    pdf.set_font("helvetica", "B", 16)
    
    # Portada
    title = remove_accents("Documentacion del Proyecto de Analisis Predictivo")
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, "Desarrollado por:", ln=True, align='C')
    pdf.cell(0, 10, remove_accents("Santiago Ramirez Forero"), ln=True, align='C')
    pdf.cell(0, 10, remove_accents("Macjainer Molano Ramos"), ln=True, align='C')
    pdf.ln(20)
    
    # Contenido
    sections = [
        ("Introduccion", """
        Este proyecto es una aplicacion de analisis predictivo que permite:
        - Cargar y visualizar datos
        - Realizar analisis exploratorio
        - Entrenar modelos predictivos
        - Visualizar resultados
        
        Tecnologias Utilizadas:
        - Frontend: Streamlit
        - Backend: Python
        - Base de Datos: PostgreSQL
        - Modelos: Decision Tree, Random Forest, XGBoost, SVM, KNN, Regresion Logistica/Lineal
        """),
        
        ("Arquitectura del Sistema", """
        Estructura del Proyecto:
        proyecto/
        ├── app.py
        ├── requirements.txt
        ├── .env
        ├── README.md
        └── pages/
            ├── __init__.py
            ├── data_upload.py
            ├── dashboard.py
            ├── models.py
            ├── visualizations.py
            └── utils.py
            
        Componentes Principales:
        1. app.py: Punto de entrada de la aplicacion
        2. data_upload.py: Gestion de carga de datos
        3. dashboard.py: Visualizacion de datos
        4. models.py: Implementacion de modelos predictivos
        5. utils.py: Funciones de utilidad y conexion a BD
        """),
        
        ("Base de Datos", """
        ¿Por que PostgreSQL?
        - Confiabilidad: Sistema robusto y probado
        - Escalabilidad: Manejo eficiente de grandes volumenes de datos
        - Integracion: Excelente soporte para Python
        - Gratuito: Codigo abierto y sin costos de licencia
        
        Configuracion:
        1. Variables de Entorno (.env):
        DATABASE_URL=postgresql://usuario:contraseña@host:puerto/base_de_datos
        
        2. Conexion a la Base de Datos:
        import os
        from dotenv import load_dotenv
        import psycopg2
        from sqlalchemy import create_engine
        
        load_dotenv()
        DATABASE_URL = os.getenv('DATABASE_URL')
        engine = create_engine(DATABASE_URL)
        """),
        
        ("Desarrollo", """
        1. Carga de Datos:
        def show():
            st.title("Cargar Datos")
            upload_option = st.radio(
                "Selecciona el metodo de carga",
                ["Subir archivo", "Cargar desde base de datos"]
            )
            
        2. Modelos Predictivos:
        def get_model(model_name, model_type):
            if model_type == "Clasificacion":
                models = {
                    "Arbol de Decision": DecisionTreeClassifier(),
                    "Random Forest": RandomForestClassifier(),
                    "XGBoost": xgb.XGBClassifier(),
                    "Regresion Logistica": LogisticRegression(),
                    "SVM": SVC(),
                    "KNN": KNeighborsClassifier()
                }
            else:
                models = {
                    "Arbol de Decision": DecisionTreeRegressor(),
                    "Random Forest": RandomForestRegressor(),
                    "XGBoost": xgb.XGBRegressor(),
                    "Regresion Lineal": LinearRegression(),
                    "SVM": SVR(),
                    "KNN": KNeighborsRegressor()
                }
            return models.get(model_name)
        """),
        
        ("Metodologia CRISP-DM", """
        1. Comprension del Negocio:
        - Identificacion de objetivos
        - Requisitos del proyecto
        - Planificacion inicial
        
        2. Comprension de los Datos:
        - Recopilacion de datos
        - Descripcion de datos
        - Exploracion de datos
        - Verificacion de calidad
        
        3. Preparacion de los Datos:
        - Seleccion de datos
        - Limpieza de datos
        - Construccion de datos
        - Integracion de datos
        - Formato de datos
        
        4. Modelado:
        - Seleccion de tecnica de modelado
        - Diseno del test
        - Construccion del modelo
        - Evaluacion del modelo
        
        5. Evaluacion:
        - Evaluacion de resultados
        - Revision del proceso
        - Determinacion del siguiente paso
        
        6. Despliegue:
        - Planificacion del despliegue
        - Monitoreo y mantenimiento
        - Documentacion
        - Soporte tecnico
        """)
    ]
    
    for title, content in sections:
        pdf.add_page()
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, remove_accents(title), ln=True)
        pdf.set_font("helvetica", "", 12)
        # Dividir el contenido en líneas y procesar cada una
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, remove_accents(line))
    
    # Guardar PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name

def get_download_link(file_path, link_text):
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes)
        return f'<a href="data:application/pdf;base64,{b64.decode()}" download="documentacion.pdf">{link_text}</a>'

def show():
    st.title("📚 Documentación del Proyecto")
    
    # Botón para descargar PDF
    pdf_path = create_pdf()
    st.markdown(get_download_link(pdf_path, "📥 Descargar Documentación en PDF"), unsafe_allow_html=True)
    
    # Índice
    st.markdown("## Índice")
    st.markdown("""
    1. [Introducción](#introducción)
    2. [Objetivos](#objetivos)
    3. [Análisis del Sistema](#análisis)
    4. [Arquitectura del Sistema](#arquitectura)
    5. [Base de Datos](#base-de-datos)
    6. [Desarrollo](#desarrollo)
    7. [Modelos Predictivos](#modelos)
    8. [Visualizaciones](#visualizaciones)
    9. [Metodología CRISP-DM](#metodología)
    """)
    
    # Introducción
    st.markdown("## Introducción")
    st.markdown("""
    Este proyecto es una aplicación de análisis predictivo que permite:
    - Cargar y visualizar datos
    - Realizar análisis exploratorio
    - Entrenar modelos predictivos
    - Visualizar resultados
    """)
    
    st.markdown("### Tecnologías Utilizadas")
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: Python
    - **Base de Datos**: PostgreSQL
    - **Modelos**: Decision Tree, Random Forest, XGBoost, SVM, KNN, Regresión Logística/Lineal
    """)
    
    st.markdown("### Integrantes")
    st.markdown("""
    - Santiago Ramirez Forero
    - Macjainer Molano Ramos
    """)
    
    # Objetivos
    st.markdown("## Objetivos")
    st.markdown("""
    ### Objetivo General
    Desarrollar una aplicación web que permita realizar análisis predictivo de datos utilizando diferentes modelos de machine learning.
    
    ### Objetivos Específicos
    1. Implementar una interfaz intuitiva para la carga y visualización de datos
    2. Desarrollar un sistema de almacenamiento eficiente en base de datos
    3. Integrar múltiples modelos predictivos para análisis
    4. Generar visualizaciones interactivas de los resultados
    5. Documentar el proceso y resultados del proyecto
    """)
    
    # Análisis del Sistema
    st.markdown("## Análisis del Sistema")
    st.markdown("""
    ### Requisitos Funcionales
    1. **Gestión de Datos**
       - Carga de archivos CSV y Excel
       - Almacenamiento en base de datos
       - Visualización de datos
       
    2. **Análisis Predictivo**
       - Selección de variables objetivo
       - Entrenamiento de modelos
       - Evaluación de resultados
       
    3. **Visualización**
       - Gráficos interactivos
       - Matrices de confusión
       - Curvas ROC
       
    ### Requisitos No Funcionales
    1. **Usabilidad**
       - Interfaz intuitiva
       - Documentación clara
       - Mensajes de error descriptivos
       
    2. **Rendimiento**
       - Tiempo de respuesta < 3 segundos
       - Soporte para archivos grandes
       - Optimización de consultas
    """)
    
    # Arquitectura
    st.markdown("## Arquitectura del Sistema")
    st.markdown("### Estructura del Proyecto")
    st.code("""
    proyecto/
    ├── app.py
    ├── requirements.txt
    ├── .env
    ├── README.md
    └── pages/
        ├── __init__.py
        ├── data_upload.py
        ├── dashboard.py
        ├── models.py
        ├── visualizations.py
        └── utils.py
    """)
    
    st.markdown("### Componentes Principales")
    st.markdown("""
    1. **app.py**: Punto de entrada de la aplicación
    2. **data_upload.py**: Gestión de carga de datos
    3. **dashboard.py**: Visualización de datos
    4. **models.py**: Implementación de modelos predictivos
    5. **utils.py**: Funciones de utilidad y conexión a BD
    """)
    
    # Base de Datos
    st.markdown("## Base de Datos")
    st.markdown("### ¿Por qué PostgreSQL?")
    st.markdown("""
    - **Confiabilidad**: Sistema robusto y probado
    - **Escalabilidad**: Manejo eficiente de grandes volúmenes de datos
    - **Integración**: Excelente soporte para Python
    - **Gratuito**: Código abierto y sin costos de licencia
    """)
    
    st.markdown("### Configuración")
    st.markdown("#### 1. Variables de Entorno")
    st.code("""
    # .env
    DATABASE_URL=postgresql://usuario:contraseña@host:puerto/base_de_datos
    """)
    
    st.markdown("#### 2. Conexión a la Base de Datos")
    st.code("""
    import os
    from dotenv import load_dotenv
    import psycopg2
    from sqlalchemy import create_engine
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener URL de la base de datos
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Crear conexión
    engine = create_engine(DATABASE_URL)
    """)
    
    st.markdown("#### 3. Funciones de Utilidad")
    st.code('''
def upload_to_db(df, table_name):
    """Sube un DataFrame a la base de datos"""
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        return True
    except Exception as e:
        print(f"Error al subir datos: {str(e)}")
        return False

def load_from_db(table_name):
    """Carga datos de la base de datos"""
    try:
        return pd.read_sql(f"SELECT * FROM {table_name}", engine)
    except Exception as e:
        print(f"Error al cargar datos: {str(e)}")
        return None
''')
    
    # Desarrollo
    st.markdown("## Desarrollo")
    st.markdown("### 1. Carga de Datos")
    st.code("""
    def show():
        st.title("Cargar Datos")
        
        # Opciones de carga
        upload_option = st.radio(
            "Selecciona el metodo de carga",
            ["Subir archivo", "Cargar desde base de datos"]
        )
        
        if upload_option == "Subir archivo":
            uploaded_file = st.file_uploader(
                "Sube tu archivo CSV o Excel",
                type=['csv', 'xlsx']
            )
    """)
    
    # Modelos Predictivos
    st.markdown("## Modelos Predictivos")
    st.markdown("### Tipos de Modelos")
    st.markdown("""
    #### 1. Árbol de Decisión
    - **Clasificación**: DecisionTreeClassifier
    - **Regresión**: DecisionTreeRegressor
    - **Ventajas**: Fácil interpretación, manejo de datos no lineales
    - **Desventajas**: Puede sobreajustar
    
    #### 2. Random Forest
    - **Clasificación**: RandomForestClassifier
    - **Regresión**: RandomForestRegressor
    - **Ventajas**: Reduce sobreajuste, manejo de outliers
    - **Desventajas**: Mayor complejidad computacional
    
    #### 3. XGBoost
    - **Clasificación**: XGBClassifier
    - **Regresión**: XGBRegressor
    - **Ventajas**: Alto rendimiento, manejo de datos faltantes
    - **Desventajas**: Requiere ajuste de hiperparámetros
    
    #### 4. SVM (Support Vector Machine)
    - **Clasificación**: SVC
    - **Regresión**: SVR
    - **Ventajas**: Efectivo en espacios de alta dimensión
    - **Desventajas**: Sensible a la escala de los datos
    
    #### 5. KNN (K-Nearest Neighbors)
    - **Clasificación**: KNeighborsClassifier
    - **Regresión**: KNeighborsRegressor
    - **Ventajas**: Simple, no requiere entrenamiento
    - **Desventajas**: Costoso computacionalmente
    
    #### 6. Regresión
    - **Clasificación**: LogisticRegression
    - **Regresión**: LinearRegression
    - **Ventajas**: Interpretable, rápido
    - **Desventajas**: Asume relaciones lineales
    """)
    
    st.markdown("### Implementación")
    st.code("""
    def get_model(model_name, model_type):
        if model_type == "Clasificacion":
            models = {
                "Arbol de Decision": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "XGBoost": xgb.XGBClassifier(),
                "Regresion Logistica": LogisticRegression(),
                "SVM": SVC(),
                "KNN": KNeighborsClassifier()
            }
        else:
            models = {
                "Arbol de Decision": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "XGBoost": xgb.XGBRegressor(),
                "Regresion Lineal": LinearRegression(),
                "SVM": SVR(),
                "KNN": KNeighborsRegressor()
            }
        return models.get(model_name)
    """)
    
    # Visualizaciones
    st.markdown("## Visualizaciones")
    st.markdown("### Tipos de Gráficos")
    st.markdown("""
    #### 1. Matriz de Confusión
    - Muestra verdaderos/falsos positivos/negativos
    - Útil para evaluar clasificadores
    
    #### 2. Curva ROC
    - Muestra relación entre sensibilidad y especificidad
    - Área bajo la curva (AUC) indica rendimiento
    
    #### 3. Gráficos de Importancia de Características
    - Muestra importancia de variables
    - Útil para interpretación del modelo
    """)
    
    st.markdown("### Implementación")
    st.code("""
    def plot_confusion_matrix(y_true, y_pred, model_name):
        cm = confusion_matrix(y_true, y_pred)
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicción Negativa', 'Predicción Positiva'],
            y=['Real Negativo', 'Real Positivo'],
            colorscale='Blues'
        ))
        return fig
    """)
    
    # Metodología CRISP-DM
    st.markdown("## Metodología CRISP-DM")
    st.markdown("### 1. Comprensión del Negocio")
    st.markdown("""
    - Identificación de objetivos
    - Requisitos del proyecto
    - Planificación inicial
    """)
    
    st.markdown("### 2. Comprensión de los Datos")
    st.markdown("""
    - Recopilación de datos
    - Descripción de datos
    - Exploración de datos
    - Verificación de calidad
    """)
    
    st.markdown("### 3. Preparación de los Datos")
    st.markdown("""
    - Selección de datos
    - Limpieza de datos
    - Construcción de datos
    - Integración de datos
    - Formato de datos
    """)
    
    st.markdown("### 4. Modelado")
    st.markdown("""
    - Selección de técnica de modelado
    - Diseño del test
    - Construcción del modelo
    - Evaluación del modelo
    """)
    
    st.markdown("### 5. Evaluación")
    st.markdown("""
    - Evaluación de resultados
    - Revisión del proceso
    - Determinación del siguiente paso
    """)
    
    st.markdown("### 6. Despliegue")
    st.markdown("""
    - Planificación del despliegue
    - Monitoreo y mantenimiento
    - Documentación
    - Soporte técnico
    """)
    
    # Footer
    st.markdown("---")
