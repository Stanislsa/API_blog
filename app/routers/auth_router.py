
import bcrypt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.db import get_conn

router = APIRouter(prefix="/auth")

class SignUpReq(BaseModel):
    email: EmailStr
    username: str
    password: str

@router.post("/signup")
def signup(sign_up_req: SignUpReq):
    hashed = bcrypt.hashpw(sign_up_req.password.encode("utf-8"), bcrypt.gensalt())
    with get_conn() as conn:
        with conn.cursor() as cursor:
            record = cursor.execute(
                "select * from users where email = %s or username = %s",
                [sign_up_req.email, sign_up_req.username],
            )
            record = cursor.fetchone()
             
            if record:
                raise HTTPException(status_code=400, detail="user aleready exists")
            
            cursor.execute(
                "insert into users (email, username, password) values (%s,%s,%s)", [sign_up_req.email, sign_up_req.username, hashed]
            )
    return {"message": "sign up succcess"}