import sqlite3
from fastapi import APIRouter, HTTPException, Header

from . import db
from .schemas import RegisterReq, LoginReq, LoginResp, MeResp
from .auth import hash_pw, verify_pw, make_token, auth

router = APIRouter(prefix="/api")


@router.post("/register", status_code=201)
def register(req: RegisterReq):
    if db.username_exists(req.username):
        raise HTTPException(400, "Username already exists")
    try:
        db.create_user(
            username      = req.username,
            password_hash = hash_pw(req.password),
            adafruit_user = req.adafruit_user,
            adafruit_key  = req.adafruit_key,
        )
    except sqlite3.IntegrityError:
        raise HTTPException(400, "Username already exists")
    return {"message": "User created"}


@router.post("/login", response_model=LoginResp)
def login(req: LoginReq):
    user = db.find_user(req.username)
    if not user or not verify_pw(req.password, user["password_hash"]):
        raise HTTPException(401, "Invalid username or password")
    return LoginResp(
        token         = make_token(req.username),
        username      = req.username,
        adafruit_user = user["adafruit_user"],
        adafruit_key  = user["adafruit_key"],
    )


@router.get("/me", response_model=MeResp)
def me(authorization: str = Header(None)):
    payload = auth(authorization)
    user = db.find_user(payload["sub"])
    if not user:
        raise HTTPException(404, "User not found")
    return MeResp(
        username      = user["username"],
        adafruit_user = user["adafruit_user"],
        adafruit_key  = user["adafruit_key"],
    )


@router.get("/stats")
def stats():
    return {"total_users": db.count_users()}
