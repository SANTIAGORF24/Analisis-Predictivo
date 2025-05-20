import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.utils import load_from_db, get_available_tables

def show():
    st.title("📊 Dashboard")
    
    try:
        # Obtener lista de tablas disponibles
        available_tables = get_available_tables()
        
        if not available_tables:
            st.warning("No hay datos disponibles. Por favor, carga datos en la sección 'Cargar Datos'.")
            return
        
        # Seleccionar tabla
        selected_table = st.selectbox(
            "Selecciona la tabla a analizar",
            available_tables
        )
        
        # Cargar datos
        df = load_from_db(selected_table)
        
        if df is None or df.empty:
            st.error("No se pudieron cargar los datos. Por favor, intenta nuevamente.")
            return
        
        # Mostrar información general
        st.header("📈 Información General")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Número de Registros", len(df))
        with col2:
            st.metric("Número de Columnas", len(df.columns))
        with col3:
            st.metric("Memoria Usada", f"{df.memory_usage().sum() / 1024:.2f} KB")
        
        # Análisis de columnas numéricas
        st.header("📊 Análisis de Variables Numéricas")
        
        # Seleccionar columna numérica
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) > 0:
            selected_column = st.selectbox(
                "Selecciona una variable numérica",
                numeric_columns
            )
            
            # Crear histograma
            fig_hist = px.histogram(
                df,
                x=selected_column,
                title=f"Distribución de {selected_column}",
                nbins=30
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Estadísticas descriptivas
            st.subheader("Estadísticas Descriptivas")
            st.dataframe(df[selected_column].describe(), use_container_width=True)
        
        # Análisis de columnas categóricas
        st.header("📊 Análisis de Variables Categóricas")
        
        # Seleccionar columna categórica
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_columns) > 0:
            selected_cat_column = st.selectbox(
                "Selecciona una variable categórica",
                categorical_columns
            )
            
            # Crear gráfico de barras
            value_counts = df[selected_cat_column].value_counts().reset_index()
            value_counts.columns = ['Categoría', 'Cantidad']
            
            fig_bar = px.bar(
                value_counts,
                x='Categoría',
                y='Cantidad',
                title=f"Distribución de {selected_cat_column}"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Mostrar conteos
            st.subheader("Conteo por Categoría")
            st.dataframe(value_counts, use_container_width=True)
        
        # Correlaciones (si hay suficientes columnas numéricas)
        if len(numeric_columns) > 1:
            st.header("📊 Matriz de Correlaciones")
            
            # Calcular correlaciones
            corr_matrix = df[numeric_columns].corr()
            
            # Crear mapa de calor
            fig_corr = px.imshow(
                corr_matrix,
                title="Matriz de Correlaciones",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Vista previa de los datos
        st.header("📋 Vista Previa de los Datos")
        st.dataframe(df.head(10), use_container_width=True)
        
    except Exception as e:
        st.error(f"Error en el dashboard: {str(e)}")
        st.error("Por favor, intenta recargar la página o verifica que los datos estén cargados correctamente.") 