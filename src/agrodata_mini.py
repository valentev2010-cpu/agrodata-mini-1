from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "agrodata_semanal.csv"
REPORTS_DIR = BASE_DIR / "reports"


def cargar_datos() -> list[dict]:
    registros = []
    with DATA_FILE.open(encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila["finca_id"] = int(fila["finca_id"])
            fila["semana"] = int(fila["semana"])
            fila["litros_leche"] = int(fila["litros_leche"])
            fila["kg_maiz"] = int(fila["kg_maiz"])
            fila["kg_sorgo"] = int(fila["kg_sorgo"])
            fila["costo_alimento"] = int(fila["costo_alimento"])
            fila["lluvia_mm"] = float(fila["lluvia_mm"])
            fila["temperatura_promedio"] = float(fila["temperatura_promedio"])
            fila["animales_activos"] = int(fila["animales_activos"])
            registros.append(fila)
    return registros


def formatear_moneda(valor: float) -> str:
    return f"${valor:,.0f}".replace(",", ".")


def clasificar_produccion(promedio_leche: float) -> str:
    if promedio_leche >= 1800:
        return "Alta"
    elif promedio_leche >= 1400:
        return "Media"
    return "Baja"


def resumen_general(registros: list[dict]) -> dict:
    total_leche = 0
    total_maiz = 0
    total_sorgo = 0
    total_costo = 0
    total_lluvia = 0.0

    for fila in registros:
        total_leche += fila["litros_leche"]
        total_maiz += fila["kg_maiz"]
        total_sorgo += fila["kg_sorgo"]
        total_costo += fila["costo_alimento"]
        total_lluvia += fila["lluvia_mm"]

    cantidad = len(registros)
    return {
        "registros": cantidad,
        "total_leche": total_leche,
        "total_maiz": total_maiz,
        "total_sorgo": total_sorgo,
        "total_costo": total_costo,
        "promedio_lluvia": total_lluvia / cantidad if cantidad else 0,
        "promedio_leche": total_leche / cantidad if cantidad else 0,
    }


def resumen_por_finca(registros: list[dict]) -> list[dict]:
    agrupado = defaultdict(lambda: {
        "finca": "",
        "municipio": "",
        "semanas": 0,
        "total_leche": 0,
        "total_maiz": 0,
        "total_sorgo": 0,
        "total_costo": 0,
    })

    for fila in registros:
        item = agrupado[fila["finca"]]
        item["finca"] = fila["finca"]
        item["municipio"] = fila["municipio"]
        item["semanas"] += 1
        item["total_leche"] += fila["litros_leche"]
        item["total_maiz"] += fila["kg_maiz"]
        item["total_sorgo"] += fila["kg_sorgo"]
        item["total_costo"] += fila["costo_alimento"]

    resultado = []
    for item in agrupado.values():
        item["promedio_leche"] = item["total_leche"] / item["semanas"]
        item["clasificacion"] = clasificar_produccion(item["promedio_leche"])
        resultado.append(item)

    resultado.sort(key=lambda x: x["total_leche"], reverse=True)
    return resultado


def top_semanas(registros: list[dict], limite: int = 10) -> list[dict]:
    ordenado = sorted(registros, key=lambda x: x["litros_leche"], reverse=True)
    return ordenado[:limite]


def filtrar_finca(registros: list[dict], nombre_finca: str) -> list[dict]:
    nombre_finca = nombre_finca.strip().lower()
    return [fila for fila in registros if fila["finca"].lower() == nombre_finca]


def generar_alertas(registros: list[dict]) -> list[str]:
    alertas = []
    for fila in registros:
        if fila["litros_leche"] < fila["animales_activos"] * 50:
            alertas.append(
                f"Semana {fila['semana']} - {fila['finca']}: producción de leche por debajo del umbral esperado."
            )
        if fila["lluvia_mm"] > 130:
            alertas.append(
                f"Semana {fila['semana']} - {fila['finca']}: lluvia alta ({fila['lluvia_mm']} mm), revisar humedad y pastos."
            )
        if fila["incidencia_sanitaria"] == "observacion":
            alertas.append(
                f"Semana {fila['semana']} - {fila['finca']}: requiere seguimiento veterinario."
            )
    return alertas


def guardar_reporte(registros: list[dict]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    destino = REPORTS_DIR / "reporte_agrodata.txt"
    general = resumen_general(registros)
    fincas = resumen_por_finca(registros)[:5]
    alertas = generar_alertas(registros)[:20]

    lineas = []
    lineas.append("AGRODATA MINI - REPORTE SEMANAL")
    lineas.append("=" * 45)
    lineas.append(f"Registros analizados: {general['registros']}")
    lineas.append(f"Total leche: {general['total_leche']} litros")
    lineas.append(f"Total maíz: {general['total_maiz']} kg")
    lineas.append(f"Total sorgo: {general['total_sorgo']} kg")
    lineas.append(f"Costo estimado de alimento: {formatear_moneda(general['total_costo'])}")
    lineas.append(f"Promedio de lluvia: {general['promedio_lluvia']:.2f} mm")
    lineas.append("")
    lineas.append("TOP 5 FINCAS POR PRODUCCIÓN")
    lineas.append("-" * 45)
    for posicion, finca in enumerate(fincas, start=1):
        lineas.append(
            f"{posicion}. {finca['finca']} ({finca['municipio']}) - "
            f"Leche: {finca['total_leche']} L - Clasificación: {finca['clasificacion']}"
        )
    lineas.append("")
    lineas.append("ALERTAS PRINCIPALES")
    lineas.append("-" * 45)
    if alertas:
        lineas.extend(alertas)
    else:
        lineas.append("No se generaron alertas relevantes.")

    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino

def graficar_leche_por_finca(registros: list[dict]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se pudo generar el gráfico porque matplotlib no está instalado.")
        print("Instálalo con: python -m pip install matplotlib")
        return

    resumen = resumen_por_finca(registros)

    nombres = [finca["finca"] for finca in resumen]
    leche = [finca["total_leche"] for finca in resumen]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres, leche)
    plt.title("Producción total de leche por finca")
    plt.xlabel("Finca")
    plt.ylabel("Litros de leche")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def mostrar_menu() -> None:
    print("\\nAGRODATA MINI - ANALIZADOR DE DATOS SEMANALES")
    print("1. Ver resumen general")
    print("2. Ver ranking de fincas")
    print("3. Buscar una finca")
    print("4. Ver top de semanas")
    print("5. Generar alertas")
    print("6. Exportar reporte TXT")
    print("7. Ver gráfico de leche por finca")
    print("8. Salir")


def ejecutar() -> None:
    registros = cargar_datos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            general = resumen_general(registros)
            print("\nRESUMEN GENERAL")
            print("-" * 40)
            print(f"Registros: {general['registros']}")
            print(f"Total leche: {general['total_leche']} litros")
            print(f"Total maíz: {general['total_maiz']} kg")
            print(f"Total sorgo: {general['total_sorgo']} kg")
            print(f"Costo total de alimento: {formatear_moneda(general['total_costo'])}")
            print(f"Promedio de lluvia: {general['promedio_lluvia']:.2f} mm")
            print(f"Clasificación promedio de producción: {clasificar_produccion(general['promedio_leche'])}")

        elif opcion == "2":
            print("\nRANKING DE FINCAS")
            print("-" * 70)
            for posicion, finca in enumerate(resumen_por_finca(registros), start=1):
                print(
                    f"{posicion}. {finca['finca']} - {finca['municipio']} | "
                    f"Leche: {finca['total_leche']} L | "
                    f"Promedio semanal: {finca['promedio_leche']:.2f} | "
                    f"Clasificación: {finca['clasificacion']}"
                )

        elif opcion == "3":
            nombre = input("Ingrese el nombre de la finca: ")
            datos = filtrar_finca(registros, nombre)
            if datos:
                general = resumen_general(datos)
                print(f"\nRESULTADOS PARA {nombre.upper()}")
                print("-" * 40)
                print(f"Semanas encontradas: {general['registros']}")
                print(f"Leche total: {general['total_leche']} litros")
                print(f"Maíz total: {general['total_maiz']} kg")
                print(f"Sorgo total: {general['total_sorgo']} kg")
                print(f"Costo total: {formatear_moneda(general['total_costo'])}")
                print(f"Clasificación: {clasificar_produccion(general['promedio_leche'])}")
            else:
                print("No se encontraron datos para esa finca.")

        elif opcion == "4":
            print("\nTOP 10 SEMANAS POR PRODUCCIÓN DE LECHE")
            print("-" * 70)
            for fila in top_semanas(registros):
                print(
                    f"Semana {fila['semana']} | {fila['finca']} | "
                    f"{fila['litros_leche']} litros | {fila['fecha_inicio']}"
                )

        elif opcion == "5":
            alertas = generar_alertas(registros)
            print("\nALERTAS DETECTADAS")
            print("-" * 70)
            if alertas:
                for alerta in alertas[:30]:
                    print("-", alerta)
                if len(alertas) > 30:
                    print(f"... y {len(alertas) - 30} alertas adicionales.")
            else:
                print("No se detectaron alertas.")

        elif opcion == "6":
            ruta = guardar_reporte(registros)
            print(f"Reporte exportado en: {ruta}")

        elif opcion == "7":
            graficar_leche_por_finca(registros)

        elif opcion == "8":
            print("Gracias por usar AgroData Mini.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    ejecutar()

