from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import jwt, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "qubamind_secret_key"
ADMIN_EMAIL = "admin@qubamind.ai"
ADMIN_PASSWORD = "admin123"

def create_token(email):
    payload = {"email": email, "exp": time.time() + 86400}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["email"] == ADMIN_EMAIL
    except:
        return False

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    if data.get("email") == ADMIN_EMAIL and data.get("password") == ADMIN_PASSWORD:
        return { "token": create_token(data["email"]) }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/verify-token")
async def verify(request: Request):
    token = request.headers.get("Authorization")
    if token and verify_token(token):
        return { "status": "valid" }
    raise HTTPException(status_code=401, detail="Invalid or missing token")

@app.post("/command")
async def command(request: Request):
    token = request.headers.get("Authorization")
    if not token or not verify_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = await request.json()
    cmd = data.get("command", "").lower()
    if "pause bot" in cmd:
        return {"response": "⏸️ Instagram bot paused for 3 hours."}
    elif "show status" in cmd:
        return {"response": "🧠 QubaMind Panel is healthy and live!"}
    elif "add feature" in cmd:
        return {"response": f"🔧 New feature added: {cmd.replace('add feature', '').strip()}"}
    else:
        return {"response": "🤖 Command received: " + cmd}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
