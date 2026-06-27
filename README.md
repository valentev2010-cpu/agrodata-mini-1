# AgroData Mini - Analizador de datos semanales

Mini proyecto en Python orientado a ciencia de datos básica aplicada al contexto rural.
Permite cargar una base de datos semanal, analizar producción, clasificar resultados y exportar un reporte.

## ¿Qué incluye?
- Base de datos CSV amplia con **416 registros**.
- Script principal para analizar datos semanales.
- Menú interactivo en consola.
- Reporte exportable en TXT.
- Estructura lista para abrir en **Visual Studio Code**.

## Estructura del proyecto
```bash
agrodata-mini/
|-- data/
|   `-- agrodata_semanal.csv
|-- docs/
|-- reports/
|-- src/
|   `-- agrodata_mini.py
`-- README.md
```

## Datos incluidos
La base contiene información semanal de 8 fincas durante 52 semanas.
Columnas principales:
- finca
- municipio
- semana
- fecha_inicio
- litros_leche
- kg_maiz
- kg_sorgo
- costo_alimento
- lluvia_mm
- temperatura_promedio
- animales_activos
- incidencia_sanitaria
- observacion

## ¿Qué hace el script?
1. Carga el CSV.
2. Calcula resumen general.
3. Genera ranking de fincas.
4. Busca una finca específica.
5. Muestra las mejores semanas por producción.
6. Genera alertas por baja producción, lluvia alta o seguimiento sanitario.
7. Exporta un reporte `.txt`.
8. Muestra un gráfico de producción de leche por finca si `matplotlib` está instalado.

## Cómo ejecutarlo
1. Abre la carpeta en VS Code.
2. Entra a la carpeta `src`.
3. Ejecuta:

```bash
python agrodata_mini.py
```

Para usar la opción de gráficos instala primero:

```bash
python -m pip install matplotlib
```

## Por qué este proyecto se ve profesional
- Usa un conjunto de datos amplio.
- Aplica lógica de programación con secuencia, condicionales y ciclos.
- Organiza archivos como un mini proyecto real.
- Genera análisis y reporte.
- Se puede ampliar fácilmente a gráficos, pandas o base de datos SQL.

## Ideas de mejora
- agregar visualizaciones con matplotlib;
- usar pandas para análisis más avanzado;
- exportar a CSV y JSON;
- conectar una base SQLite;
- crear dashboard web con Streamlit.

## Nota técnica
El menú principal usa bibliotecas estándar de Python. La opción de gráfico requiere `matplotlib` como dependencia opcional.
