import json
import sqlite3
import sys, io
from pathlib import Path

from app import db

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

JSON_FILE = Path(__file__).parent / "users.json"


def main():
    if not JSON_FILE.exists():
        print(f"[skip] {JSON_FILE} không tồn tại — không có gì để migrate.")
        return

    try:
        data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[error] users.json không hợp lệ: {e}")
        return

    if not isinstance(data, list):
        print("[error] users.json phải là một JSON array.")
        return

    added   = 0
    skipped = 0
    empty   = 0

    for user in data:
        username = (user.get("username") or "").strip()
        if not username:
            empty += 1
            continue

        if db.username_exists(username):
            print(f"[skip] '{username}' đã tồn tại trong DB.")
            skipped += 1
            continue

        try:
            db.create_user(
                username      = username,
                password_hash = user.get("password_hash", ""),
                adafruit_user = user.get("adafruit_user", ""),
                adafruit_key  = user.get("adafruit_key", ""),
            )
            added += 1
            print(f"[ok]   migrated '{username}'")
        except sqlite3.IntegrityError as e:
            print(f"[error] không thể migrate '{username}': {e}")
            skipped += 1

    print()
    print("-" * 50)
    print(f"[done] Migrated: {added} | Skipped: {skipped} | Empty: {empty}")
    print(f"[done] Tổng số user trong DB: {db.count_users()}")
    print("-" * 50)


if __name__ == "__main__":
    main()
