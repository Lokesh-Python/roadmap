from fastapi import FastAPI
from .routers import questions, roadmap

app = FastAPI()

app.include_router(questions.router)
app.include_router(roadmap.router)

@app.get("/root")
def root():
    return "connection test working"