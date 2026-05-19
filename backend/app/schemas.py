from pydantic import BaseModel, Field


class RegisterReq(BaseModel):
    username:      str = Field(min_length=3, max_length=32)
    password:      str = Field(min_length=6, max_length=64)
    adafruit_user: str = Field(min_length=1)
    adafruit_key:  str = Field(min_length=1)


class LoginReq(BaseModel):
    username: str
    password: str


class LoginResp(BaseModel):
    token:         str
    username:      str
    adafruit_user: str
    adafruit_key:  str


class MeResp(BaseModel):
    username:      str
    adafruit_user: str
    adafruit_key:  str
