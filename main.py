from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_things(name: str):
    return {"Hello": name}

