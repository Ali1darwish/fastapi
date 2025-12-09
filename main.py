
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get_things():
    return {"Hello": "World"}

