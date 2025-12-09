from fastapi import FastAPI

app = FastAPI()

@app.get("/)
async def get_things(name):
    return {"hi there": name}




