import pyperclip
cantidad = int(input("Caballos a 0.7 €, cuantos se quiere llevar? "))

precio = 0.7

total = precio * cantidad

dinero = float(input(f"su total es {total} €. El pago es en efectivo, con cuanto paga? "))

cambio = dinero - (cantidad * precio)

print(f"sus vueltas son {cambio:.2f} €, gracias por preferirnos")

#----------------------------------------------------------------

print("Artikelnummer:%5d, Preis:%8.2f" % (4504, 65.056))

#----------------------------------------------------------------

print("{0:<4}{1:<19}{2:<25}{3:>5}".format("Nr.", "Servername", "Adresse", "Port"))
print("{0:<4}{1:<19}{2:<25}{3:>5}".format("1", "Server1", "192.168.0.1", "22"))
print("{0:<4}{1:<19}{2:<25}{3:>5}".format("2", "Server2", "192.168.0.2", "22"))

#----------------------------------------------------------------
