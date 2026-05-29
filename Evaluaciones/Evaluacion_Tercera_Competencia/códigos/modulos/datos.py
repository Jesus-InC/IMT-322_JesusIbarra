import csv
import os
from datetime import datetime

# Retrocedemos dos niveles de carpetas para llegar a la raiz de la practica
DIR_MODULOS = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(os.path.dirname(DIR_MODULOS)) 

def obtener_ruta_csv():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DIR_BASE, "registro", f"registro_{fecha_hoy}.csv")

def clasificar_estado(distancia):
    if distancia > 50.0:
        return "LIBRE"
    elif 20.0 <= distancia <= 50.0:
        return "CERCA"
    else:
        return "OCUPADO"

def guardar_en_csv(fecha_hora, distancia, estado):
    archivo_csv = obtener_ruta_csv()
    escribir_encabezado = not os.path.exists(archivo_csv)

    with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if escribir_encabezado:
            escritor.writerow(["fecha_hora", "distancia_cm", "estado"])
        escritor.writerow([fecha_hora, distancia, estado])
