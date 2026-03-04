###   -------->   \  <--- importante

text = "Python"
largo = len(text)

print(f"{text: ^1}")
print(f"{text:#^{largo}}")


print("Hallo ich bin 'Mr R.'")
print("""Hallo ich bin "Mr R." """)
print("Hallo ich bin 'Mr R.'")
print("Hallo ich bin \"Mr R.\"")
print('Hallo ich bin \'Mr R.\'')

saludo = "Hallo Welt"
split = saludo.split()
reverse = split[::-1]


definitiv = " ".join(reverse)

print(saludo, split, reverse, "R: ", definitiv)


# \t = sangria
# \n = linea nueva


###### menu/edit
####   alt + shift + einfg seleccion columna modus

#------------------------------------------------------------
woerter = "Hallo Welt".split()

print(woerter)
wort1, wort2 = woerter

print(wort2)
print(wort1)
#------------------------------------------------------------

name = input("Bitte geben Sie ihren Namen ein: ")
print(name.upper())
print(name.lower())
print(name.capitalize())
print(name.swapcase())
print(name.isupper())
print(name.islower())
print(name.istitle())
#------------------------------------------------------------

"""
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
"""

#------------------------------------------------------------
