import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR  = BASE_DIR.parent / "web"

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY") or "INSECURE_DEV_KEY_set_SECRET_KEY_in_.env"
JWT_ALGO   = "HS256"
TOKEN_DAYS = int(os.getenv("TOKEN_DAYS", "7"))
PORT       = int(os.getenv("PORT", "8000"))

if SECRET_KEY.startswith("INSECURE_"):
    print("[WARN] SECRET_KEY not set in .env — using insecure default.")
