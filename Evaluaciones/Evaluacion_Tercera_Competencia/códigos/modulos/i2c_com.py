import smbus2

BUS_I2C = 1
ADDR_ESP32 = 0x08
bus = smbus2.SMBus(BUS_I2C)

def leer_distancia_i2c():
    try:
        word = bus.read_word_data(ADDR_ESP32, 0)
        
        byte_1 = word & 0xFF
        byte_2 = (word >> 8) & 0xFF
        distancia_entera = (byte_1 << 8) | byte_2
        distancia_final = distancia_entera / 10.0
        
        # Filtro basico para evitar lecturas ruidosas del sensor
        if 0.0 <= distancia_final <= 400.0:
            return distancia_final
        return None
    except Exception:
        # Si falla temporalmente el I2C, devolvemos None para que el main no se cuelgue
        return None
