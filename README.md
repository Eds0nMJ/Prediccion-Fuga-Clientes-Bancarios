# 🏦 Predicción de Churn (Fuga de Clientes) en el Sector Bancario

## 🎯 Objetivo del Proyecto
Identificar los factores críticos que impulsan el abandono de clientes en una entidad bancaria y desarrollar un modelo predictivo de Machine Learning para clasificar clientes en riesgo de fuga, optimizando las estrategias de retención.

## 🛠️ Stack Tecnológico
* **SQL Server (T-SQL):** Extracción, limpieza de datos (Data Type Casting) y Análisis Exploratorio de Datos (EDA).
* **Python (Pandas, Scikit-Learn):** Conexión ODBC, preprocesamiento matricial (One-Hot Encoding, StandardScaler) y modelado predictivo.
* **Power BI:** Visualización gerencial y comunicación de hallazgos.

## 📊 Hallazgos de Negocio (EDA en SQL & Power BI)
Mediante consultas SQL sobre una cartera de 10,000 registros, se detectó una tasa de fuga global del **20.37%**. Los principales focos de riesgo descubiertos fueron:
1. **Perfil Demográfico:** Las mujeres en Alemania presentan una tasa de abandono crítica por encima del 37%.
2. **Riesgo por Edad:** La probabilidad de fuga se dispara en clientes mayores de 50 años.
3. **Paradoja del Saldo:** Contraintuitivamente, los clientes *con saldo en sus cuentas* presentan casi el doble de fuga frente a las cuentas en cero, sugiriendo que la competencia está capturando cuentas activas y rentables.

![Dashboard Power BI](Dashboard_PowerBI.png)

## 🤖 Rendimiento del Modelo Predictivo (Machine Learning)
Se entrenó un algoritmo **Random Forest Classifier** optimizado para lidiar con el desbalance de clases nativo del sector bancario (`class_weight='balanced'`).

* **Recall (Sensibilidad) - Clase 1:** Se logró un **60%**, permitiendo al banco identificar proactivamente a más de la mitad de los clientes en riesgo real antes de que cierren su cuenta.
* **Accuracy General:** 84%.
* **Feature Importance:** El modelo confirmó algorítmicamente que la Edad (`Age`) y el Saldo (`Balance`) son los predictores matemáticos más fuertes del comportamiento de fuga, validando con exactitud la hipótesis del análisis exploratorio visual.
