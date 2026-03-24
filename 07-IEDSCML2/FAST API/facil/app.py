
"""

Im Terminal:
> uvicorn app:app --reload

"""

import os
from pathlib import Path
from fastapi import FastAPI

os.chdir(Path(__file__).parent)


# 1) crear la aplicacion FAST API
app = FastAPI(title="Mi API", description="Esta es una API de prueba", version="0.0.1")

# importante!! -> para decirle a app que se vuelva endpoint
# http://127.0.0.1:8000/
@app.get("/") # root address
def root():
    return {"message": "Hello World"}

@app.get("/greeting") # endpoint para esta funcion
def greeting():
    return {"message": "Holis"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item_id =+ 10
    return {"item_id": item_id}

# http://127.0.0.1:8000/users?emp_id=1&name=Mohamed
# http://127.0.0.1:8000/users?emp_id=2&name=5 ---> valid , fastapi can convert 5 to "5"
# http://127.0.0.1:8000/users?emp_id=apfel&name=thomas  -> ERROR
@app.get("/users")
async def get_user_info(emp_id: int, name: str):
    print(f"emp_id: {emp_id} name: {name}")
    return {"User ID": emp_id,
            "Name": name}



# def add(x:int, y:int):
#    total = x + y
#    print(total)

"""pydantinc hace la validacion del type"""
# print(add(3, 6))
# print(add("hola", " perra"))

