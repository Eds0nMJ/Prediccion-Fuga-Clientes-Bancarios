USE Portafolio_Bancario;
GO

-- 1. Limpieza de datos (Data Type Casting)
ALTER TABLE Clientes_Churn ALTER COLUMN Exited INT;
ALTER TABLE Clientes_Churn ALTER COLUMN Balance FLOAT;
GO

-- 2. Control de Calidad
SELECT COUNT(*) AS Total_Registros, COUNT(DISTINCT CustomerId) AS Clientes_Unicos
FROM Clientes_Churn;

-- 3. Tasa Global de Fuga (Churn Rate)
SELECT COUNT(*) AS Total_Clientes, 
       SUM(Exited) AS Clientes_Fugados, 
       COUNT(*) - SUM(Exited) AS Clientes_Retenidos, 
       ROUND(CAST(SUM(Exited) AS FLOAT) / COUNT(*) * 100, 2) AS Porcentaje_Churn
FROM Clientes_Churn;

-- 4. Fuga por País y Género
SELECT Geography AS Pais, 
       Gender AS Genero, 
       COUNT(*) AS Total_Clientes, 
       SUM(Exited) AS Cantidad_Fugados, 
       ROUND(CAST(SUM(Exited) AS FLOAT) / COUNT(*) * 100, 2) AS Porcentaje_Churn
FROM Clientes_Churn
GROUP BY Geography, Gender
ORDER BY Porcentaje_Churn DESC;

-- 5. Fuga por Rango de Edad
SELECT 
    CASE 
        WHEN Age < 30 THEN '1. Menor de 30'
        WHEN Age BETWEEN 30 AND 40 THEN '2. De 30 a 40'
        WHEN Age BETWEEN 41 AND 50 THEN '3. De 41 a 50'
        ELSE '4. Mayor de 50'
    END AS Rango_Edad,
    COUNT(*) AS Total_Clientes,
    SUM(Exited) AS Cantidad_Fugados,
    ROUND(CAST(SUM(Exited) AS FLOAT) / COUNT(*) * 100, 2) AS Porcentaje_Churn
FROM Clientes_Churn
GROUP BY 
    CASE 
        WHEN Age < 30 THEN '1. Menor de 30'
        WHEN Age BETWEEN 30 AND 40 THEN '2. De 30 a 40'
        WHEN Age BETWEEN 41 AND 50 THEN '3. De 41 a 50'
        ELSE '4. Mayor de 50'
    END
ORDER BY Rango_Edad;

-- 6. Impacto del Saldo (Balance)
SELECT 
    CASE 
        WHEN Balance = 0 THEN 'Sin Saldo (0)'
        ELSE 'Con Saldo en Cuenta'
    END AS Estado_Cuenta,
    COUNT(*) AS Total_Clientes,
    SUM(Exited) AS Cantidad_Fugados,
    ROUND(CAST(SUM(Exited) AS FLOAT) / COUNT(*) * 100, 2) AS Porcentaje_Churn
FROM Clientes_Churn
GROUP BY 
    CASE 
        WHEN Balance = 0 THEN 'Sin Saldo (0)'
        ELSE 'Con Saldo en Cuenta'
    END;