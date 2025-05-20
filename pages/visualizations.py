import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils import load_from_db, get_available_tables

def show():
    st.title("📈 Visualizaciones Avanzadas")
    
    try:
        # Obtener lista de tablas disponibles
        tables = get_available_tables()
        
        if not tables:
            st.warning("Por favor, carga los datos en la sección 'Cargar Datos'")
            return
            
        # Seleccionar tabla
        selected_table = st.selectbox(
            "Selecciona la tabla a visualizar",
            tables
        )
        
        # Cargar datos
        df = load_from_db(selected_table)
        
        if df is None or df.empty:
            st.error("No se pudieron cargar los datos. Por favor, verifica la conexión a la base de datos.")
            return
            
        st.success(f"Datos cargados correctamente: {len(df)} filas, {len(df.columns)} columnas")
        
        # Mostrar información básica
        st.subheader("📊 Información del Dataset")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Número de Filas", len(df))
            st.metric("Número de Columnas", len(df.columns))
        
        with col2:
            st.metric("Memoria Usada", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            st.metric("Valores Nulos", df.isnull().sum().sum())
        
        # Visualizaciones
        st.subheader("📈 Visualizaciones")
        
        # 1. Distribución de Variables Numéricas
        st.write("### Distribución de Variables Numéricas")
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 0:
            selected_numeric = st.selectbox("Selecciona una variable numérica", numeric_cols)
            
            # Histograma
            fig_hist = px.histogram(
                df, 
                x=selected_numeric,
                title=f"Distribución de {selected_numeric}",
                nbins=30
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Box Plot
            fig_box = px.box(
                df,
                y=selected_numeric,
                title=f"Box Plot de {selected_numeric}"
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # 2. Correlación entre Variables Numéricas
        if len(numeric_cols) > 1:
            st.write("### Matriz de Correlación")
            corr_matrix = df[numeric_cols].corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))
            
            fig_corr.update_layout(
                title="Matriz de Correlación",
                height=600
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # 3. Visualización de Variables Categóricas
        st.write("### Variables Categóricas")
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) > 0:
            selected_cat = st.selectbox("Selecciona una variable categórica", categorical_cols)
            
            # Gráfico de barras
            fig_bar = px.bar(
                df[selected_cat].value_counts().reset_index(),
                x='index',
                y=selected_cat,
                title=f"Distribución de {selected_cat}"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Gráfico de pastel
            fig_pie = px.pie(
                df,
                names=selected_cat,
                title=f"Proporción de {selected_cat}"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # 4. Relación entre Variables
        st.write("### Relación entre Variables")
        col1, col2 = st.columns(2)
        
        with col1:
            x_var = st.selectbox("Variable X", df.columns)
        with col2:
            y_var = st.selectbox("Variable Y", df.columns)
        
        if x_var and y_var:
            # Scatter plot
            fig_scatter = px.scatter(
                df,
                x=x_var,
                y=y_var,
                title=f"Relación entre {x_var} y {y_var}"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 5. Vista previa de los datos
        st.subheader("📋 Vista Previa de los Datos")
        st.dataframe(df.head(10))
        
    except Exception as e:
        st.error(f"Error al cargar o procesar los datos: {str(e)}")
        st.info("Por favor, verifica que los datos estén correctamente cargados en la base de datos.") 