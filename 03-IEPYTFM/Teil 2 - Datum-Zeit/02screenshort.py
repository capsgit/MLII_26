import schedule
import time
import mss, mss.tools

counter = 0


def bildschirmaufnahme():
    """Screenshot von einem bestimmten Monitor (1, 2, 3, ...)"""
    global counter
    monitor = 1
    counter += 1
    filename = f"screenshot{counter}.png"

    with mss.mss() as sct:
        monitor = sct.monitors[monitor]
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

        print("Screenshot gespeichert unter: " + filename)


schedule.every(1).seconds.do(bildschirmaufnahme)

# Endlos-Schleife:
while True:
    schedule.run_pending()  # Hier wird überprüft, ob ein Job "fällig" ist
    if counter == 10:
        break

    time.sleep(1)  # Wartet 1 Sekunde. Kann angepasst werden, abhängig davon, wie oft ein Job erwartet wird.

