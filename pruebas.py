import RPi.GPIO as GPIO
import time
import os
from datetime import datetime

# ==============================
# CONFIGURACIÓN
# ==============================
SENSOR_PIN = 17
OUTPUT_DIR = os.path.expanduser("~/capturas")
COOLDOWN = 0.3   # segundos (evita múltiples disparos)

last_trigger_time = 0

# Crear carpeta si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# CONFIGURACIÓN GPIO
# ==============================
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ==============================
# FUNCIÓN DE CAPTURA
# ==============================
def capturar_imagen():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{OUTPUT_DIR}/img_{timestamp}.jpg"

    cmd = (
        f"rpicam-still -o {filename} "
        f"--width 1280 --height 720 "
        f"--shutter 500 "
        f"--gain 2 "
        f"--nopreview"
    )

    os.system(cmd)

    print(f"[OK] Imagen capturada: {filename}")

# ==============================
# CALLBACK DEL SENSOR
# ==============================
def sensor_callback(channel):
    global last_trigger_time

    current_time = time.time()

    # Anti-rebote / anti-múltiples capturas
    if current_time - last_trigger_time < COOLDOWN:
        return

    last_trigger_time = current_time

    print("[TRIGGER] Envase detectado")

    capturar_imagen()

# ==============================
# ACTIVAR INTERRUPCIÓN
# ==============================
GPIO.add_event_detect(
    SENSOR_PIN,
    GPIO.RISING,
    callback=sensor_callback,
    bouncetime=50
)

print("Sistema listo. Esperando envases...")

# ==============================
# LOOP PRINCIPAL
# ==============================
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Saliendo...")
    GPIO.cleanup()