from fastapi import FastAPI
from router import router as posts_router
from questions import router as questions_router

app = FastAPI()

app.include_router(posts_router)
app.include_router(questions_router)
