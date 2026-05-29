import smbus2
import time
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN I2C ---
BUS_I2C = 1
ADDR_ESP32 = 0x08
bus = smbus2.SMBus(BUS_I2C)

# --- CONFIGURACIÓN DE LA PRÁCTICA ---
INTERVALO_MUESTREO = 2.0  # Segundos entre lecturas (Requisito: entre 1 y 5s)
MUESTRAS_MINIMAS = 30     # Cantidad mínima de muestras a registrar

# Generar nombres de archivos con la fecha actual (Requisito 8.1 y 9)
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
archivo_csv = f"registro_{fecha_hoy}.csv"
archivo_grafica = f"grafica_{fecha_hoy}.png"

# --- LISTAS PARA ALMACENAR DATOS EN MEMORIA (PARA LA GRÁFICA) ---
lista_tiempos = []
lista_distancias = []

def clasificar_estado(distancia):
    """Clasifica el estado según los umbrales definidos (Requisito 6.2)"""
    if distancia > 50.0:
        return "LIBRE"
    elif 20.0 <= distancia <= 50.0:
        return "CERCA"
    else:
        return "OCUPADO"

def guardar_en_csv(fecha_hora, distancia, estado):
    """Guarda una fila en el archivo CSV (Requisito 8)"""
    # Si el archivo no existe, lo creamos y escribimos el encabezado
    escribir_encabezado = not os.path.exists(archivo_csv)
    
    with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if escribir_encabezado:
            escritor.writerow(["fecha_hora", "distancia_cm", "estado"])
        escritor.writerow([fecha_hora, distancia, estado])

def generar_grafica():
    """Genera y guarda la gráfica en formato PNG a partir de los datos obtenidos (Requisito 9)"""
    print("\n\nGenerando gráfica de datos registrados...")
    
    if len(lista_distancias) == 0:
        print("No hay datos suficientes para graficar.")
        return

    plt.figure(figsize=(10, 6))
    
    # Graficar la línea de distancia vs tiempo
    plt.plot(lista_tiempos, lista_distancias, marker='o', linestyle='-', color='b', label='Distancia (cm)')
    
    # Líneas de referencia para los umbrales de clasificación (Opcional, se ve muy profesional)
    plt.axhline(y=50, color='g', linestyle='--', alpha=0.6, label='Umbral LIBRE (>50cm)')
    plt.axhline(y=20, color='r', linestyle='--', alpha=0.6, label='Umbral OCUPADO (<20cm)')
    
    # Formato y requisitos de la gráfica
    plt.title(f"Medición de Distancia en Función del Tiempo ({fecha_hoy})", fontsize=14, fontweight='bold')
    plt.xlabel("Tiempo de ejecución (Muestras)", fontsize=12)
    plt.ylabel("Distancia medida (cm)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    # Rotar las etiquetas de tiempo para que no se amontonen si son muchas
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfico
    plt.savefig(archivo_grafica)
    print(f"¡Gráfica guardada exitosamente como: '{archivo_grafica}'!")
    plt.show()

# --- PROGRAMA PRINCIPAL ---
print("=========================================================")
print(f"SISTEMA MAESTRO I2C - SENSOR DE PROXIMIDAD (ESP32: 0x{ADDR_ESP32:02X})")
print(f"Archivo de registro asignado: {archivo_csv}")
print(f"Se registrarán un mínimo de {MUESTRAS_MINIMAS} muestras.")
print("=========================================================\n")

contador_muestras = 0

try:
    while True:
        try:
            # 1. Solicitar datos al microcontrolador por I2C (Requisito 5.2.3)
            word = bus.read_word_data(ADDR_ESP32, 0)
            
            # 2. Decodificar datos y corregir endianness (Requisito 5.2.4)
            byte_1 = word & 0xFF
            byte_2 = (word >> 8) & 0xFF
            distancia_entera = (byte_1 << 8) | byte_2
            distancia_final = distancia_entera / 10.0

            # Filtro básico para descartar ruido del bus
            if 0.0 <= distancia_final <= 400.0:
                # 3. Agregar estampado de tiempo (Requisito 5.2.5)
                ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ahora_corto = datetime.now().strftime("%H:%M:%S") # Para el eje X de la gráfica
                
                # 4. Clasificar el estado según la distancia (Requisito 5.2.7)
                estado_actual = clasificar_estado(distancia_final)
                
                # 5. Guardar en el archivo CSV (Requisito 5.2.6)
                guardar_en_csv(ahora_str, distancia_final, estado_actual)
                
                # Guardar en memoria para graficar al final
                lista_tiempos.append(ahora_corto)
                lista_distancias.append(distancia_final)
                
                contador_muestras += 1
                
                # Imprimir progreso en pantalla sin romper la línea
                print(f"[{ahora_str}] Muestra #{contador_muestras:02d} | Distancia: {distancia_final:5.1f} cm | Estado: {estado_actual:<7}", end="\r")

        except Exception as e:
            # Los errores de I2C momentáneos no deben tumbar el script
            pass 
            
        # Control de tiempo de muestreo periódico
        time.sleep(INTERVALO_MUESTREO)

except KeyboardInterrupt:
    print(f"\n\nLectura detenida por el usuario de forma manual.")
    if contador_muestras >= MUESTRAS_MINIMAS:
        generar_grafica()
    else:
        print(f"Alerta: Solo registraste {contador_muestras} muestras. Se requieren al menos {MUESTRAS_MINIMAS} para generar la gráfica obligatoria.")




