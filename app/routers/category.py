from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
# from app.dependencies import get_db, AdminDep
# from app.models import Category as CategoryModel

router = APIRouter()

# Pydantic models for request and response
class Category(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True

class CategoryReq(BaseModel):
    name: str

# Endpoint to get all categories
@router.get("/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

# Endpoint to create a new category
@router.post("/", response_model=Category)
def create_category(
    category_req: CategoryReq, 
    db: Session = Depends(get_db), 
    admin_id: AdminDep = Depends()
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
@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int, 
    category_req: CategoryReq, 
    db: Session = Depends(get_db), 
    admin_id: AdminDep = Depends()
):
    category = db.query(CategoryModel).filter_by(id=category_id).first()
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
    db: Session = Depends(get_db), 
    admin_id: AdminDep = Depends()
):
    category = db.query(CategoryModel).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": f"Category with ID {category_id} deleted successfully"}
