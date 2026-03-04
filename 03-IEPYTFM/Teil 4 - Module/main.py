# necesario para poder importar archivos de otras carpetas
from sys import path
path.append("mis_modulos")

#-------------------------------------------------
# importar el modulo
import rechenmodul

"""
# importar cada metodo por separado (mejor)
from rechenmodul import sumar, restar, multiplicar, dividir
"""
"""
# importar todo con * (no tan recomendado)
from rechenmodul import *"""
#-------------------------------------------------


a = 2
b = 0

print(f"aca la funcion 1: {rechenmodul.sumar(a,b)}")
print(f"aca la funcion 2: {rechenmodul.restar(a,b)}")
print(f"aca la funcion 3: {rechenmodul.multiplicar(a,b)}")
print(f"aca la funcion 4: {rechenmodul.dividir(a,b)}")

# con "importar metodo por separado"
# print(f"aca la funcion 1: {sumar(a,b)}")
