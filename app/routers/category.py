from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# from app.core.db import get_conn
from app.core.dependencies import AdminDep, DBDep
from app.models.models import Category as CategoryModel

router = APIRouter()

class CategoryResponse(BaseModel):
    categorie_id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryReq(BaseModel):
    name: str

# Endpoint to get all categories
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = DBDep):
    categories = db.query(CategoryModel).all()
    return categories

# Endpoint to create a new category
@router.post("/", response_model=CategoryResponse)
def create_category(
    category_req: CategoryReq, 
    admin_id: AdminDep,
    db: Session = DBDep
):
    # Vérification si la catégorie existe déjà
    existing_category = db.query(CategoryModel).filter_by(name=category_req.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    # Création de la catégorie
    new_category = CategoryModel(
        name=category_req.name,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Endpoint to update a category
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category_req: CategoryReq, 
    admin_id: AdminDep ,
    db: Session = DBDep 
):
    category = db.query(CategoryModel).filter_by(categorie_id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = category_req.name
    category.updated_at = datetime.now()
    db.commit()
    db.refresh(category)
    return category

# Endpoint to delete a category
@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    admin_id: AdminDep,
    db: Session = DBDep
):
    category = db.query(CategoryModel).filter_by(categorie_id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": f"Category with ID {category_id} deleted successfully"}
