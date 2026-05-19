import uvicorn

from app import app
from app import db
from app.config import PORT, WEB_DIR


if __name__ == "__main__":
    print(f"[DB]    {db.DB_FILE}")
    print(f"[WEB]   serving {WEB_DIR}")
    print(f"[USERS] {db.count_users()} user(s) in database")
    print(f"[URL]   http://localhost:{PORT}/")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
