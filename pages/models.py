import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, classification_report, confusion_matrix, roc_curve, auc
import xgboost as xgb
import plotly.express as px
import plotly.graph_objects as go
from pages.utils import load_from_db, get_available_tables

def plot_confusion_matrix(y_true, y_pred, model_name):
    """Genera y muestra la matriz de confusión"""
    cm = confusion_matrix(y_true, y_pred)
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicción Negativa', 'Predicción Positiva'],
        y=['Real Negativo', 'Real Positivo'],
        colorscale='Blues',
        showscale=True
    ))
    fig.update_layout(
        title=f'Matriz de Confusión - {model_name}',
        xaxis_title='Predicción',
        yaxis_title='Valor Real'
    )
    return fig

def plot_roc_curve(y_true, y_pred_proba, model_name):
    """Genera y muestra la curva ROC"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        name=f'ROC (AUC = {roc_auc:.2f})',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        name='Línea Base',
        line=dict(color='red', dash='dash')
    ))
    fig.update_layout(
        title=f'Curva ROC - {model_name}',
        xaxis_title='Tasa de Falsos Positivos',
        yaxis_title='Tasa de Verdaderos Positivos',
        showlegend=True
    )
    return fig

def plot_regression_results(y_true, y_pred, model_name):
    """Genera y muestra gráfica de resultados de regresión"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_true, y=y_pred,
        mode='markers',
        name='Predicciones',
        marker=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=[min(y_true), max(y_true)],
        y=[min(y_true), max(y_true)],
        mode='lines',
        name='Línea Perfecta',
        line=dict(color='red', dash='dash')
    ))
    fig.update_layout(
        title=f'Predicciones vs Valores Reales - {model_name}',
        xaxis_title='Valores Reales',
        yaxis_title='Predicciones',
        showlegend=True
    )
    return fig

def plot_feature_importance(importance_df, model_name):
    """Genera y muestra gráfica de importancia de características"""
    fig = px.bar(
        importance_df,
        x='Importancia',
        y='Característica',
        orientation='h',
        title=f'Importancia de Características - {model_name}'
    )
    fig.update_layout(
        xaxis_title='Importancia',
        yaxis_title='Característica',
        showlegend=False
    )
    return fig

def get_model(model_name, model_type):
    """Retorna el modelo seleccionado según el tipo"""
    if model_type == "Clasificación":
        models = {
            "Árbol de Decisión": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
            "XGBoost": xgb.XGBClassifier(random_state=42),
            "Regresión Logística": LogisticRegression(random_state=42),
            "SVM": SVC(random_state=42, probability=True),
            "KNN": KNeighborsClassifier()
        }
    else:  # Regresión
        models = {
            "Árbol de Decisión": DecisionTreeRegressor(random_state=42),
            "Random Forest": RandomForestRegressor(random_state=42),
            "XGBoost": xgb.XGBRegressor(random_state=42),
            "Regresión Lineal": LinearRegression(),
            "SVM": SVR(),
            "KNN": KNeighborsRegressor()
        }
    return models.get(model_name)

def show():
    st.title("🤖 Modelos de Machine Learning")
    
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
        
        # Seleccionar tipo de modelo
        model_type = st.radio(
            "Selecciona el tipo de modelo",
            ["Clasificación", "Regresión"]
        )
        
        # Seleccionar modelos a entrenar
        available_models = {
            "Clasificación": [
                "Árbol de Decisión",
                "Random Forest",
                "XGBoost",
                "Regresión Logística",
                "SVM",
                "KNN"
            ],
            "Regresión": [
                "Árbol de Decisión",
                "Random Forest",
                "XGBoost",
                "Regresión Lineal",
                "SVM",
                "KNN"
            ]
        }
        
        selected_models = st.multiselect(
            "Selecciona los modelos a entrenar",
            available_models[model_type],
            default=["Árbol de Decisión", "XGBoost"]
        )
        
        # Seleccionar variable objetivo
        target_column = st.selectbox(
            "Selecciona la variable objetivo",
            df.columns
        )
        
        # Seleccionar variables predictoras
        feature_columns = st.multiselect(
            "Selecciona las variables predictoras",
            [col for col in df.columns if col != target_column]
        )
        
        if not feature_columns:
            st.warning("Por favor, selecciona al menos una variable predictora.")
            return
        
        # Preparar datos
        X = df[feature_columns]
        y = df[target_column]
        
        # Dividir datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Entrenar modelos
        if st.button("Entrenar Modelos"):
            with st.spinner("Entrenando modelos..."):
                results = {}
                models = {}
                
                for model_name in selected_models:
                    model = get_model(model_name, model_type)
                    model.fit(X_train, y_train)
                    pred = model.predict(X_test)
                    
                    if model_type == "Clasificación":
                        score = accuracy_score(y_test, pred)
                        report = classification_report(y_test, pred)
                        # Obtener probabilidades para la curva ROC
                        if hasattr(model, 'predict_proba'):
                            pred_proba = model.predict_proba(X_test)[:, 1]
                        else:
                            pred_proba = pred
                    else:
                        score = r2_score(y_test, pred)
                        mse = mean_squared_error(y_test, pred)
                        report = f"MSE: {mse:.4f}"
                    
                    results[model_name] = {
                        'score': score,
                        'report': report,
                        'predictions': pred,
                        'pred_proba': pred_proba if model_type == "Clasificación" else None
                    }
                    models[model_name] = model
                
                # Mostrar resultados
                st.header("📊 Resultados de los Modelos")
                
                # Crear columnas para los resultados
                cols = st.columns(len(selected_models))
                
                for i, model_name in enumerate(selected_models):
                    with cols[i]:
                        st.subheader(model_name)
                        if model_type == "Clasificación":
                            st.metric("Precisión", f"{results[model_name]['score']:.4f}")
                        else:
                            st.metric("R²", f"{results[model_name]['score']:.4f}")
                            st.metric("MSE", f"{mean_squared_error(y_test, results[model_name]['predictions']):.4f}")
                        st.text("Reporte:")
                        st.text(results[model_name]['report'])
                
                # Gráficas específicas según el tipo de modelo
                st.header("📈 Visualizaciones")
                
                for model_name in selected_models:
                    st.subheader(f"Gráficas - {model_name}")
                    
                    if model_type == "Clasificación":
                        # Matriz de confusión
                        st.plotly_chart(plot_confusion_matrix(y_test, results[model_name]['predictions'], model_name))
                        
                        # Curva ROC
                        st.plotly_chart(plot_roc_curve(y_test, results[model_name]['pred_proba'], model_name))
                    else:
                        # Gráfica de predicciones vs valores reales
                        st.plotly_chart(plot_regression_results(y_test, results[model_name]['predictions'], model_name))
                
                # Importancia de características
                st.header("📊 Importancia de Características")
                
                importance_models = [m for m in selected_models if m in ["Árbol de Decisión", "Random Forest", "XGBoost"]]
                if importance_models:
                    cols = st.columns(len(importance_models))
                    
                    for i, model_name in enumerate(importance_models):
                        with cols[i]:
                            importance = pd.DataFrame({
                                'Característica': feature_columns,
                                'Importancia': models[model_name].feature_importances_
                            }).sort_values('Importancia', ascending=False)
                            
                            # Mostrar gráfica de importancia
                            st.plotly_chart(plot_feature_importance(importance, model_name))
                            
                            # Mostrar tabla de importancia
                            st.dataframe(importance, use_container_width=True)
                
                # Guardar modelos en la sesión
                st.session_state['models'] = models
                st.session_state['feature_columns'] = feature_columns
                st.session_state['results'] = results
    
    except Exception as e:
        st.error(f"Error en los modelos: {str(e)}")
        st.error("Por favor, verifica que los datos sean apropiados para el tipo de modelo seleccionado.") 