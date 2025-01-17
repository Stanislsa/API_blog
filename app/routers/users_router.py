from fastapi import APIRouter, Depends
from pydantic import BaseModel
from psycopg2.extras import DictCursor

from app.db import get_conn
from app.dependencies import get_current_user_id

router = APIRouter(prefix="/users")

class UserRes(BaseModel):
    user_id: int
    email: str
    username: str

@router.get("/me")
def me(current_user_id: str =  Depends(get_current_user_id)):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("select * from users where user_id  = %s", [current_user_id])
            record = cursor.fetchone()

            user_data = {
                "user_id": record["user_id"],
                "email": record["email"],
                "username": record["username"],
            }
            
    return UserRes(**user_data)