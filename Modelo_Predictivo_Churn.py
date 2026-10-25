import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# FASE 1: EXTRACCIÓN DESDE SQL SERVER
# ============================================================
try:
    cadena_conexion = r'mssql+pyodbc://localhost\SQLEXPRESS/Portafolio_Bancario?driver=SQL+Server&Trusted_Connection=yes'
    motor_sql = create_engine(cadena_conexion)
    print("Conectando a SQL Server...")
    
    query = "SELECT * FROM Clientes_Churn"
    df_clientes = pd.read_sql(query, motor_sql)
    print("¡Extracción exitosa!")

except Exception as e:
    print("Ocurrió un error en la conexión. Detalle:")
    print(e)
    exit()

# ============================================================
# FASE 2: PREPROCESAMIENTO Y TRANSFORMACIÓN
# ============================================================
print("\nIniciando limpieza y transformación...")
# Eliminamos columnas basura (IDs y Apellidos)
columnas_basura = ['RowNumber', 'CustomerId', 'Surname']
df_limpio = df_clientes.drop(columns=columnas_basura)

# Convertimos texto (País, Género) a binario (One-Hot Encoding)
df_matriz = pd.get_dummies(df_limpio, columns=['Geography', 'Gender'], drop_first=True)

# Separamos variables predictoras (X) y variable objetivo (y)
X = df_matriz.drop(columns=['Exited'])
y = df_matriz['Exited']

# ============================================================
# FASE 3: MACHINE LEARNING - RANDOM FOREST
# ============================================================
# División 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

# Escalado Matemático
COLS_CONTINUAS = ['CreditScore', 'Age', 'Tenure', 'Balance', 'EstimatedSalary']
scaler = StandardScaler()
X_train = X_train.copy()
X_test  = X_test.copy()
X_train[COLS_CONTINUAS] = scaler.fit_transform(X_train[COLS_CONTINUAS])
X_test[COLS_CONTINUAS]  = scaler.transform(X_test[COLS_CONTINUAS])

# Entrenamiento del Modelo
print("\nEntrenando algoritmo...")
modelo_rf = RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42, n_jobs=-1)
modelo_rf.fit(X_train, y_train)

# ============================================================
# FASE 4: EVALUACIÓN DE NEGOCIO
# ============================================================
y_pred = modelo_rf.predict(X_test)

print("\n" + "="*55)
print("REPORTE DE CLASIFICACIÓN")
print("="*55)
print(classification_report(y_test, y_pred, target_names=['Retenido (0)', 'Fugado (1)']))

# Extraer Top 5 de Variables Más Importantes
importancias = pd.Series(modelo_rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
print("\nTop 5 predictores del Churn:")
print(importancias.head(5).to_string())

# Mostrar Gráficos (El código se pausa hasta que cierres estas ventanas)
# 1. Matriz de confusión
fig, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Retenido', 'Fugado'])
disp.plot(cmap='Blues', ax=ax, colorbar=False)
ax.set_title('Matriz de Confusión — Churn Bancario')
plt.show()

# 2. Gráfico de Importancia
top5 = importancias.head(5).sort_values(ascending=True)
fig2, ax2 = plt.subplots(figsize=(8, 4))
top5.plot(kind='barh', ax=ax2, color=sns.color_palette("Blues_r", n_colors=5))
ax2.set_title('Top 5 Variables — Feature Importance (Random Forest)')
plt.show()