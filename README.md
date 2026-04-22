# AgroData Mini - Analizador de datos semanales

Mini proyecto en Python orientado a ciencia de datos basica aplicada al contexto rural.
Permite cargar una base de datos semanal, analizar produccion, clasificar resultados y exportar un reporte.

## Que incluye?
- Base de datos CSV amplia con **416 registros**.
- Script principal para analizar datos semanales.
- Menu interactivo en consola.
- Reporte exportable en TXT.
- Estructura lista para abrir en **Visual Studio Code**.

## Estructura del proyecto
```bash
agrodata-mini/
├── data/
│   └── agrodata_semanal.csv
├── docs/
├── reports/
├── src/
│   └── agrodata_mini.py
└── README.md
```

## Datos incluidos
La base contiene informacion semanal de 8 fincas durante 52 semanas.
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

## Que hace el script?
1. Carga el CSV.
2. Calcula resumen general.
3. Genera ranking de fincas.
4. Busca una finca especifica.
5. Muestra las mejores semanas por produccion.
6. Genera alertas por baja produccion, lluvia alta o seguimiento sanitario.
7. Exporta un reporte `.txt`.

## Como ejecutarlo
1. Abre la carpeta en VS Code.
2. Entra a la carpeta `src`.
3. Ejecuta:

```bash
python agrodata_mini.py
```

## Por que este proyecto se ve profesional
- Usa un conjunto de datos amplio.
- Aplica logica de programacion con secuencia, condicionales y ciclos.
- Organiza archivos como un mini proyecto real.
- Genera analisis y reporte.
- Se puede ampliar facilmente a graficos, pandas o base de datos SQL.

## Ideas de mejora
- agregar visualizaciones con matplotlib;
- usar pandas para analisis mas avanzado;
- exportar a CSV y JSON;
- conectar una base SQLite;
- crear dashboard web con Streamlit.

## Nota tecnica
El proyecto usa solo bibliotecas estandar de Python, para que sea facil de correr sin instalar dependencias.
