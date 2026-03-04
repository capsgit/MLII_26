# from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import pytz

client = MongoClient("mongodb://localhost:27017/")
db = client["unsere_tool"]

collection = db["benutzer"]

# insertar un horizontal
"""collection.insert_one({"name": "Juan Juarez", "alter": 68})"""

# que db hay?
# print(client.list_database_names())

"""addList = [
    {
    "name": "Pablo Picasso",
    "alter": 39,
    "rolle": "tester"
    },
    {
    "name": "Pedro Picapiedra",
    "alter": 69,
    "rolle": "Benutzer"
    }
]"""

# insertar varios (many) horizontales
"""collection.insert_many(addList)"""

# encontrar/BUSCAR ! HORIZONTAL
# daten = collection.find_one({"name": "Pablo Picasso"})
# print("daten", daten)

#for k, v in daten.items():
 #   print(f"for: {k}: {v}")

# print("Name: ->", daten["name"])
# print("Alter: ->", daten["alter"])

#obj_id = ObjectId(daten["_id"])
# print("ID normal: -->", obj_id)
# print("Tiempo: -->", obj_id.generation_time)
# print("Longitud: -->", len(obj_id.binary)) # 12 bytes => |timestamp *4|random *5|counter *3|


berlin = pytz.timezone('Europe/Berlin')
bogota = pytz.timezone('America/Bogota')


# Start Datum & Zeit
start_date = berlin.localize(datetime(2026, 1,26, 8, 0, 0))
end_date =  berlin.localize(datetime(2026, 1,27, 18, 0, 0))

# Umgewandelte Zeitstempel für die Suche in UTC
start_utc = start_date.astimezone(pytz.utc)
end_utc = end_date.astimezone(pytz.utc)

daten = collection.find({"_id": {"$gte": start_utc, "$lt": end_utc}})

# Umschlüsseln
#start_object = ObjectId.from_datetime(start_date)

#documents = collection.find({"_id": {"$gte": start_object}})

#for doc in documents:
#    print("doc --->", doc)
print("DB:", db.name, "| Collection:", collection.name, "| Docs:", collection.count_documents({}))

for doc in daten:
    print(doc)

