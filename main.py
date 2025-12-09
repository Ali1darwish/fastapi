from fastapi import FastAPI

app = FastAPI()

@app.get("/{name}")
async def get_things(name: str):
    return {"hi there": name}
