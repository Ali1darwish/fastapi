
from fastapi import FastAPI

app = FastAPI()

@app.get('/{name}')
async def get_things():
    return {f'hello': '{name} is that you''}


