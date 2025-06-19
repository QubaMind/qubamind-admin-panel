from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "QubaMind Panel is Running ✅"}

from fastapi.staticfiles import StaticFiles
import os

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
