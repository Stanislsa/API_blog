from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from psycopg2.extras import DictCursor

from app.db import get_conn, get_db
from app.dependencies import get_current_user_id

router = APIRouter(prefix="/users")

class UserRes(BaseModel):
    user_id: int
    email: str
    username: str

@router.get("/me")
def me(current_user_id: str =  Depends(get_current_user_id), conn = Depends(get_db)):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("select * from users where user_id  = %s", [current_user_id])
        record = cursor.fetchone()

        user_data = {
            "user_id": record["user_id"],
            "email": record["email"],
            "username": record["username"],
        }
        
    return UserRes(**user_data)

@router.get("/",response_model=List[UserRes])
def get_users(conn = Depends(get_db)):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("select * from users where is_admin  = true")
        records =  cursor.fetchall()
        
        users = [
            UserRes(
                user_id=record["user_id"],
                email=record["email"],
                username=record["username"],
            )
            for record in records
        ]     
    return users