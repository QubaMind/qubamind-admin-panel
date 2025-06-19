from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "QubaMind Panel is Running ✅"}
