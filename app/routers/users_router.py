from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from psycopg2.extras import DictCursor
from psycopg import Connection


from app.dependencies import DBDep, AuthDep

router = APIRouter(prefix="/users")

class UserRes(BaseModel):
    user_id: int
    email: str
    username: str

@router.get("/me")
def me(current_user_id: AuthDep, conn : DBDep):
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
def get_users(conn = Depends(DBDep)):
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

@router.get("/{user_id}")
def get_user(user_id: int, conn: DBDep):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("select * from users where user_id = %s", [user_id])
        record = cursor.fetchone()
        
        user_data = {
            "user_id": record["user_id"],
            "email": record["email"],
            "username": record["username"],
        }
        
    return UserRes(**user_data)