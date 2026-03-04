from sys import path
path.append("mis_modulos")

import utils
import statistik

fahrenheit = 75
kilometer = 175

print(utils.convert_farenheit_to_celsius(fahrenheit))
print(utils.convert_kilometer_to_mile(kilometer))

print(f"mittelwert: {statistik.mittelwert(1,2,3,4,5)}")
print(f"median: {statistik.median(1,2,3,4,5)}")
