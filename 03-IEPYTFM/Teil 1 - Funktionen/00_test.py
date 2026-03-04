
def cuadrado(num):
    print(f"{num}^2 = {num**2}")

ingreso = int(input("Ingrese un numero que quiera elevar al cuadrado: "))
cuadrado(ingreso)

#-----------------------------------------------------------------------------------

valores = [1, 2, 3, 4, 5]
a, b, c, d, z = valores
print(z)

#-----------------------------------------------------------------------------------

def suma(num1, num2, num3):
    print(num1 + num2 + num3)

numeros = [8, 14, 100]
suma(*numeros)

