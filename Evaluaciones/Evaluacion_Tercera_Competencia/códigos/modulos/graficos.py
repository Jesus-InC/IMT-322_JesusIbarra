import matplotlib.pyplot as plt
import os
from datetime import datetime

DIR_MODULOS = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(os.path.dirname(DIR_MODULOS))

def generar_grafica(lista_tiempos, lista_distancias):
    if len(lista_distancias) == 0:
        print("\nNo hay suficientes datos registrados.")
        return

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    archivo_grafica = os.path.join(DIR_BASE, "graficas", f"grafica_{fecha_hoy}.png")

    plt.figure(figsize=(10, 6))
    plt.plot(lista_tiempos, lista_distancias, marker='o', linestyle='-', color='b', label='Distancia (cm)')

    # Pintar las zonas de los estados de fondo
    plt.axhspan(50, 100, color='green', alpha=0.1, label='Zona LIBRE (>50cm)')
    plt.axhspan(20, 50, color='yellow', alpha=0.1, label='Zona CERCA (20-50cm)')
    plt.axhspan(0, 20, color='red', alpha=0.1, label='Zona OCUPADO (<20cm)')

    plt.title(f"Distancia vs Tiempo ({fecha_hoy})", fontsize=14, fontweight='bold')
    plt.xlabel("Tiempo", fontsize=12)
    plt.ylabel("Distancia (cm)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(archivo_grafica)
    print(f"\nGrafica generada y guardada en la carpeta de graficas.")
    plt.show()
