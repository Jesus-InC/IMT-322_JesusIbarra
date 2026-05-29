import time
from datetime import datetime
from modulos import leer_distancia_i2c, clasificar_estado, guardar_en_csv, generar_grafica

INTERVALO_MUESTREO = 2.0 
MUESTRAS_MINIMAS = 30     

lista_tiempos = []
lista_distancias = []

print("Iniciando comunicacion I2C con ESP32...")
contador_muestras = 0

try:
    while True:
        distancia = leer_distancia_i2c()

        if distancia is not None:
            ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ahora_corto = datetime.now().strftime("%H:%M:%S") 

            estado = clasificar_estado(distancia)
            guardar_en_csv(ahora_str, distancia, estado)

            lista_tiempos.append(ahora_corto)
            lista_distancias.append(distancia)
            contador_muestras += 1

            print(f"[{ahora_str}] Muestra #{contador_muestras:02d} | Distancia: {distancia:5.1f} cm | Estado: {estado:<7}", end="\r")

        time.sleep(INTERVALO_MUESTREO)

except KeyboardInterrupt:
    print("\nLectura detenida manualmente.")
    
    if contador_muestras >= MUESTRAS_MINIMAS:
        print("Generando graficos, por favor espera...")
        generar_grafica(lista_tiempos, lista_distancias)
    else:
        print(f"Registro incompleto: {contador_muestras}/{MUESTRAS_MINIMAS} muestras minimas requeridas.")
