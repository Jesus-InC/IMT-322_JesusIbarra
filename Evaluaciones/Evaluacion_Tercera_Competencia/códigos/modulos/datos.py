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

def limpiar_archivo_al_inicio():
    # Esta funcion borra el CSV viejo para empezar una sesion limpia
    archivo = obtener_ruta_csv()
    if os.path.exists(archivo):
        os.remove(archivo)

def guardar_en_csv(fecha_hora, distancia, estado):
    archivo_csv = obtener_ruta_csv()
    # El modo 'a' permite ir agregando lineas sin borrar las anteriores
    with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        
        # Si el archivo esta vacio (posicion 0), escribimos encabezados
        if f.tell() == 0:
            escritor.writerow(["fecha_hora", "distancia_cm", "estado"])
            
        escritor.writerow([fecha_hora, distancia, estado])

