from copy import deepcopy

array = [9, 8, 3,[1, 0], {"name": "christian", "age": 38}]

clon = array

acopy = array.copy()
ccopy = clon.copy()

adeep = deepcopy(array)
cdeep = deepcopy(clon)

def drucken() :
    print("----------------------------------------------------------")
    print("Array", array)
    print("------------------------------------")
    print("CLon ", clon)
    print("-----------")
    print("Acopy", acopy)
    print("Copy ", ccopy)
    print("------------")
    print("Adeep", adeep)
    print("Deep ", cdeep)
    print("-----------------    -------------------------------------")

drucken()

array[0] = 654
drucken()

array[4] = 0
array[3][1] = 999
array[2] = {"si": "ja", "no": "nein" }
drucken()



