
import bcrypt
from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_conn

router = APIRouter(prefix="/auth")

class SignUpReq(BaseModel):
    email: str
    username: str
    password: str

@router.post("/signup")
def signup(sign_up_req: SignUpReq):
    print(sign_up_req)
    hashed = bcrypt.hashpw(sign_up_req.password.encode("utf-8"), bcrypt.gensalt())
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "insert into users (email, username, password) values (%s,%s,%s)", [sign_up_req.email, sign_up_req.username, hashed]
            )
    return {"message": "sign up succcess"}