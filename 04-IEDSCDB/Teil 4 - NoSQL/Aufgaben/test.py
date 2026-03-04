from pymongo import MongoClient
from bson.objectid import ObjectId

def create_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["warenkatalog"]
    return db

def create_products_collection():
    db = create_connection()
    collection = db["products"]
    return collection

def add_product():
    product_name = input("Bitte geben Sie den Namen des Produktes ein: ")
    article_number = input("Bitte geben Sie die Artikelnummer ein: ")
    net_price = float(input("Bitte geben Sie Die den Netto-Preis ein: "))
    stock = 0

    collection = create_products_collection()
    product_data = {"product_name": product_name, "article_number": article_number, "net_price": net_price, "stock": stock}
    collection.insert_one(product_data)
    print("Artikel hinzugefügt")
    menu()

def list_products():
    collection = create_products_collection()
    products = collection.find()

    print("ID | Produktname | Artikelnummer | Nettopreis | Bestand")
    for product in products:
        print(f"{product['_id']} | {product['product_name']} | {product['article_number']} | {product['net_price']} | {product['stock']}")

    menu()


def delete_product():
    collection = create_products_collection()
    article_number = input("Bitte geben Sie die Artikelnummer des zu löschenden Produktes ein: ")

    result = collection.delete_one({"article_number": article_number})
    if result.deleted_count > 0:
        print(f"Das Produkt mit der Artikelnummer: {article_number} wurde gelöscht.")
    else:
        print("Produkt nicht gefunden oder konnte nicht gelöscht werden.")

    menu()


def update_product():
    collection = create_products_collection()
    article_number = input("Bitte geben Sie die Artikelnummer des zu ändernden Produktes ein: ")
    product = collection.find_one({"article_number": article_number})

    if product:
        update_data = {}
        product_name = input("Bitte geben Sie den neuen Namen des Produktes ein (leer lassen, wenn keine Änderung erforderlich): ")
        new_article_number = input("Bitte geben Sie die neue Artikelnummer des Produktes ein (leer lassen, wenn keine Änderung erforderlich): ")
        net_price = input("Bitte geben Sie den neuen Netto-Preis des Produktes ein (leer lassen, wenn keine Änderung erforderlich): ")

        if product_name:
            update_data["product_name"] = product_name
        if new_article_number:
            update_data["article_number"] = new_article_number
        if net_price:
            update_data["net_price"] = float(net_price)

        if update_data:
            collection.update_one({"article_number": article_number}, {"$set": update_data})
            print("Die Eigenschaften des Produktes wurden erfolgreich geändert")
        else:
            print("Keine Änderungen vorgenommen.")
    else:
        print("Produkt nicht gefunden.")

    menu()


def change_stock(direction):
    collection = create_products_collection()
    article_number = input("Für welche Artikelnummer wollen Sie den Bestand ändern? ")
    product = collection.find_one({"article_number": article_number})

    if product:
        if direction == "inc":
            quantity = int(input("Um welche Anzahl wollen Sie den Bestand erhöhen? "))
            collection.update_one({"article_number": article_number}, {"$inc": {"stock": quantity}})
        else:
            quantity = int(input("Um welche Anzahl wollen Sie den Bestand verringern? "))
            collection.update_one({"article_number": article_number}, {"$inc": {"stock": -quantity}})

        updated_product = collection.find_one({"article_number": article_number})
        print(f"Bestand geändert! Aktueller Bestand von Artikelnummer {article_number}: {updated_product['stock']}")
    else:
        print("Produkt nicht gefunden.")

    menu()


def menu():
    entrys = ["Produkt hinzufügen", "Produkt ändern", "Produkte auflisten", "Produkt löschen", "Bestand erhöhen",
              "Bestand verringern", "Programmende"]
    for n, i in enumerate(entrys, 1):
        print(f"{n}\t\t{i}")

    while True:
        choice = input("Bitte treffen sie eine Auswahl: ")

        match choice:
            case "1":
                add_product()

            case "2":
                update_product()

            case "3":
                list_products()
            case "4":
                delete_product()
            case "5":
                change_stock("inc")
            case "6":
                change_stock("dec")

            case "7":
                exit()

if __name__ == "__main__":
    menu()
