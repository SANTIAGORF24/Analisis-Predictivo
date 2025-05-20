import streamlit as st
import pandas as pd
from pages.utils import upload_to_db, get_available_tables, load_from_db, delete_table
import time

def show():
    try:
        st.title("📤 Carga de Datos")
        st.markdown("---")
        
        # Crear dos columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Subir Nuevo Archivo")
            st.markdown("### Selecciona un archivo CSV o Excel para cargar")
            uploaded_file = st.file_uploader("", type=['csv', 'xlsx', 'xls'])
            
            if uploaded_file is not None:
                try:
                    # Determinar el tipo de archivo y leerlo
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:  # Excel
                        df = pd.read_excel(uploaded_file)
                    
                    st.success("Archivo cargado exitosamente!")
                    
                    # Mostrar información del archivo
                    st.write(f"**Nombre del archivo:** {uploaded_file.name}")
                    st.write(f"**Tamaño del archivo:** {uploaded_file.size / 1024:.2f} KB")
                    
                    # Opciones de visualización
                    st.write("### Vista previa de los datos")
                    rows_to_show = st.slider("Número de filas a mostrar", 5, 100, 10)
                    st.dataframe(df.head(rows_to_show), use_container_width=True)
                    
                    # Opción para ver más datos
                    if st.checkbox("Ver más datos"):
                        st.dataframe(df, use_container_width=True, height=400)
                    
                    table_name = st.text_input("Nombre de la tabla", "datos_analisis")
                    
                    if st.button("Cargar a Base de Datos", key="upload_to_db"):
                        # Crear una barra de progreso
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # Mostrar información de carga
                            total_rows = len(df)
                            status_text.text(f"Preparando carga de {total_rows} registros...")
                            
                            # Cargar datos a la base de datos
                            upload_to_db(df, table_name)
                            
                            # Actualizar la barra de progreso al 100%
                            progress_bar.progress(100)
                            status_text.text("¡Carga completada!")
                            
                            # Guardar el DataFrame en la sesión
                            st.session_state['df'] = df
                            
                            # Mostrar mensaje de éxito
                            st.success(f"✅ Datos cargados exitosamente a la base de datos")
                            st.info(f"Total de registros cargados: {total_rows}")
                            
                            # Mostrar vista previa de los datos cargados
                            st.write("### Vista previa de los datos cargados")
                            st.dataframe(df.head(), use_container_width=True)
                            
                        except Exception as e:
                            st.error(f"❌ Error al cargar los datos: {str(e)}")
                            progress_bar.empty()
                            status_text.empty()
                except Exception as e:
                    st.error(f"Error al leer el archivo: {str(e)}")
        
        with col2:
            st.header("Cargar desde Base de Datos")
            st.markdown("### Selecciona una tabla existente")
            
            try:
                available_tables = get_available_tables()
                
                if available_tables:
                    selected_table = st.selectbox(
                        "Selecciona una tabla",
                        available_tables
                    )
                    
                    # Opción para eliminar tabla
                    if st.button("🗑️ Eliminar Tabla", key="delete_table"):
                        if st.warning(f"¿Estás seguro de que deseas eliminar la tabla '{selected_table}'?"):
                            delete_table(selected_table)
                            st.success(f"Tabla '{selected_table}' eliminada exitosamente")
                            st.experimental_rerun()
                    
                    if st.button("Cargar Datos", key="load_from_db"):
                        # Crear una barra de progreso
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Simular progreso mientras se cargan los datos
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            status_text.text(f"Cargando datos... {i + 1}%")
                            time.sleep(0.01)  # Pequeña pausa para mostrar el progreso
                        
                        # Cargar datos desde la base de datos
                        df = load_from_db(selected_table)
                        if df is not None:
                            st.session_state['df'] = df
                            
                            # Actualizar la barra de progreso al 100%
                            progress_bar.progress(100)
                            status_text.text("¡Carga completada!")
                            st.success("Datos cargados exitosamente")
                            
                            # Opciones de visualización
                            st.write("### Vista previa de los datos")
                            rows_to_show = st.slider("Número de filas a mostrar", 5, 100, 10, key="db_rows")
                            st.dataframe(df.head(rows_to_show), use_container_width=True)
                            
                            # Opción para ver más datos
                            if st.checkbox("Ver más datos", key="db_more"):
                                st.dataframe(df, use_container_width=True, height=400)
                else:
                    st.info("No hay tablas disponibles en la base de datos")
            except Exception as e:
                st.error(f"Error al cargar desde la base de datos: {str(e)}")
        
        # Mostrar información sobre los datos cargados
        if 'df' in st.session_state:
            st.markdown("---")
            st.header("📊 Información de los Datos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Número de Filas", len(st.session_state['df']))
            
            with col2:
                st.metric("Número de Columnas", len(st.session_state['df'].columns))
            
            with col3:
                st.metric("Memoria Usada", f"{st.session_state['df'].memory_usage().sum() / 1024:.2f} KB")
            
            # Mostrar información de tipos de datos
            st.subheader("Tipos de Datos")
            type_info = pd.DataFrame({
                'Columna': st.session_state['df'].columns,
                'Tipo': st.session_state['df'].dtypes,
                'Valores Únicos': st.session_state['df'].nunique()
            })
            st.dataframe(type_info, use_container_width=True)
            
            # Mostrar estadísticas descriptivas
            st.subheader("Estadísticas Descriptivas")
            st.dataframe(st.session_state['df'].describe(), use_container_width=True)
    
    except Exception as e:
        st.error(f"Error en la página de carga de datos: {str(e)}")
        st.error("Por favor, intenta recargar la página") 