from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.db import get_db
from psycopg import Connection
from psycopg2.extras import DictCursor

router = APIRouter(prefix="/categories")

class Category(BaseModel):
    category_id: int
    name: str
    create_at: datetime
    update_at: datetime
    
@router.get("/")
def get_categories(conn: Connection = Depends(get_db)):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("select * from categories")
        records = cursor.fetchall()
        
        categories = [
            Category(
                category_id= record["categorie_id"],
                name= record["name"],
                create_at= record["created_at"],
                update_at= record["update_at"]
            )
            for record in records
        ]
    return categories
        