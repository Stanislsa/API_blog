from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.dependencies import DBDep, AuthDep
from psycopg2.extras import DictCursor
from psycopg2.extras import RealDictCursor
from psycopg2 import errors

router = APIRouter(prefix="/categories")

class Category(BaseModel):
    category_id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
class CategoryReq(BaseModel):
    name: str
    
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

@router.post("/")
def create_category(conn: DBDep, current_user_id: AuthDep, category_req: CategoryReq):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Insérer la catégorie
            cursor.execute(
                "INSERT INTO categories (name) VALUES (%s) RETURNING *",
                [category_req.name]
            )
            record = cursor.fetchone()
            categorie = {
                "id": record["categorie_id"],
                "name": record["name"],
                "created_at": record["created_at"],
                "updated_at": record["updated_at"]
            }
        return categorie
    except errors.UniqueViolation:
        # Gestion de la violation de contrainte d'unicité
        raise HTTPException(status_code=400, detail="Category already exists")
    except Exception as e:
        # Gestion générique des erreurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")