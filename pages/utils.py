import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def get_db_connection():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {str(e)}")
        return None

def clean_column_name(col_name):
    """Limpia el nombre de la columna para que sea válido en PostgreSQL"""
    # Reemplazar espacios y caracteres especiales con guiones bajos
    clean_name = col_name.lower().replace(' ', '_')
    # Eliminar caracteres no alfanuméricos excepto guiones bajos
    clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '_')
    return clean_name

def get_postgres_type(dtype):
    """Convierte el tipo de dato de pandas a PostgreSQL"""
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'DOUBLE PRECISION'
    elif pd.api.types.is_datetime64_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def upload_to_db(df, table_name):
    """Carga un DataFrame a la base de datos PostgreSQL"""
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Limpiar nombres de columnas
            df.columns = [clean_column_name(col) for col in df.columns]
            
            # Crear tabla si no existe
            columns = []
            for col in df.columns:
                col_type = get_postgres_type(df[col].dtype)
                columns.append(f'"{col}" {col_type}')
            
            # Eliminar la tabla si existe
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            
            # Crear la tabla nueva
            create_table_query = f'CREATE TABLE "{table_name}" ({", ".join(columns)})'
            cursor.execute(create_table_query)
            
            # Preparar los datos para inserción en lotes
            batch_size = 1000
            total_rows = len(df)
            
            for i in range(0, total_rows, batch_size):
                batch_df = df.iloc[i:i + batch_size]
                values_list = []
                
                for _, row in batch_df.iterrows():
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append('NULL')
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            # Escapar comillas simples en strings
                            val_str = str(val).replace("'", "''")
                            values.append(f"'{val_str}'")
                    values_list.append(f"({', '.join(values)})")
                
                if values_list:
                    insert_query = f'INSERT INTO "{table_name}" VALUES {", ".join(values_list)}'
                    cursor.execute(insert_query)
                    conn.commit()
            
            st.success(f"Datos cargados exitosamente a la base de datos. Total de registros: {total_rows}")
        except Exception as e:
            st.error(f"Error al cargar datos: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

def load_from_db(table_name):
    """Carga datos desde la base de datos PostgreSQL"""
    conn = get_db_connection()
    if conn is not None:
        try:
            df = pd.read_sql(f'SELECT * FROM "{table_name}"', conn)
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {str(e)}")
            return None
        finally:
            conn.close()
    return None

def get_available_tables():
    """Obtiene la lista de tablas disponibles en la base de datos"""
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = [table[0] for table in cursor.fetchall()]
            return tables
        except Exception as e:
            st.error(f"Error al obtener tablas: {str(e)}")
            return []
        finally:
            conn.close()
    return []

def delete_table(table_name):
    """Elimina una tabla de la base de datos"""
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Error al eliminar la tabla: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()
    return False 