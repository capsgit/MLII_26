import time

try:
    while True:
        print("Corriendo... Ctrl+C para salir")
        time.sleep(1)
except KeyboardInterrupt:
    print("✅ Ctrl+C capturado correctamente")
