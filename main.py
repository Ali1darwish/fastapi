from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# البيانات محفوظة في الميموري (مش في قاعدة بيانات)
items = []

class Item(BaseModel):
    name: str
    description: str
    url:str

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def add_item(item: Item):
    items.append(item)
    return {"message": "Item added"}

@app.put("/items/{index}")
def update_item(index: int, item: Item):
    if index < len(items):
        items[index] = item
        return {"message": "Item updated"}
    return {"error": "Item not found"}

@app.delete("/items/{index}")
def delete_item(index: int):
    if index < len(items):
        del items[index]
        return {"message": "Item deleted"}
    return {"error": "Item not found"}
