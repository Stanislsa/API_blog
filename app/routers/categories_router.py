from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.dependencies import DBDep, AuthDep, AdminDep
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
def create_category(conn: DBDep, is_admin: AdminDep, category_req: CategoryReq):
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
    
@router.put("/{category_id}")
def update_category(conn: DBDep, is_admin: AdminDep, category_id: int, category_req: CategoryReq):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("update categories set name = %s, updated_at = %s where categorie_id = %s returning *", 
            [category_req.name, datetime.now(), category_id]
        )
        record = cursor.fetchone()
        return record

@router.delete("/{category_id}")
def delete_category(conn: DBDep, is_admin: AdminDep, category_id: int):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM categories WHERE categorie_id = %s", [category_id])
        
        # Vérification des lignes affectées
        if cursor.rowcount > 0:
            return {"message": f"Category with ID {category_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Category not found")
        