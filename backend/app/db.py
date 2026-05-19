import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE  = BASE_DIR / "yolohome.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    adafruit_user   TEXT    NOT NULL,
    adafruit_key    TEXT    NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def create_user(username, password_hash, adafruit_user, adafruit_key):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, adafruit_user, adafruit_key) "
            "VALUES (?, ?, ?, ?)",
            (username, password_hash, adafruit_user, adafruit_key),
        )
        return cur.lastrowid


def find_user(username):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT username, password_hash, adafruit_user, adafruit_key, created_at "
            "FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None


def username_exists(username):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ? LIMIT 1", (username,)
        ).fetchone()
        return row is not None


def count_users():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


init_db()
