class Hund:
    number_dogs = 0
    def __init__(self, raza, nombre, color):
        self.raza = raza        # atributo Instanzbasiertes
        self.nombre = nombre    # atributo Instanzbasiertes
        self.color = color      # atributo Instanzbasiertes

        # para que cada vez q se cree un nuevo Hund, aumente el numero en 1+
        Hund.number_dogs += 1

    def bellen(self, anzahl):
        #  Instanzbasiertes METHODE
        print(anzahl * "Wuff! ")

    def essen(self, essen: str):
        #  Instanzbasiertes METHODE
        print(f"{self.nombre} isst {essen}")

    def __del__(self):
        Hund.number_dogs -= 1
        print("un perro ha sido adoptado")

    @classmethod
    def get_number_dogs(cls):
        print("el numero de perros es: ", cls.number_dogs)

# Instanzen erstellen
luna = Hund("mix", "Luna", "Blanca")
annie = Hund("poodle", "Annie", "Negro")

luna.bellen(2)
annie.bellen(5)

luna.essen("Leckerlie")
annie.essen("Schnack")
"""
print(luna.nombre)
print(luna.color)
print(luna.raza)
"""
print(Hund.get_number_dogs())
print("luna", luna.number_dogs)

del annie
print(Hund.get_number_dogs())

