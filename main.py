from fastapi import FastAPI

app = FastAPI()

@app.get("/hi")
async def get_things():
    return {"hi there": "hihhhhhhhhhhhhhhhhh"}



