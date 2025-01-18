from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from app.dependencies import DBDep
from psycopg2.extras import DictCursor

router = APIRouter(prefix="/categories")

class Category(BaseModel):
    category_id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
@router.get("/")
def get_categories(conn: DBDep):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("select * from categories")
        records = cursor.fetchall()
        
        categories = [
            Category(
                category_id= record["categorie_id"],
                name= record["name"],
                created_at= record["created_at"],
                updated_at= record["updated_at"]
            )
            for record in records
        ]
    return categories
        