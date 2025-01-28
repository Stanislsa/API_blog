from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import AdminDep, DBDep
from app.models.models import Post as PostModel
from app.models.models import Category as CategoryModel
from app.models.models import User as UserModel

router = APIRouter()


class StatusEnum(str, Enum):
    draft = "draft"
    private = "private"
    public = "public"


class User(BaseModel):
    user_id: int
    username: str

class Category(BaseModel):
    categorie_id: int
    name: str

class PostResponse(BaseModel):
    post_id: int
    title: str
    content: str
    categorie_id: int
    created_at: datetime
    updated_at: datetime

    status: StatusEnum
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    user: Optional[User] = None
    category: Optional[Category] = None
    
    class Config:
        orm_mode = True


class PostReq(BaseModel):
    title: str
    content: str
    categorie_id: int
    status: StatusEnum


# Endpoint to get all posts
@router.get("/", response_model=List[PostResponse])
def get_posts(
    db: Session = DBDep,
    category: Optional[str] = None,
    author: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100)
):
    # Base query
    query = db.query(PostModel).join(UserModel).outerjoin(CategoryModel)

    # Filtering by category
    if category:
        category_obj = db.query(CategoryModel).filter(CategoryModel.name == category).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail="Category not found")
        query = query.filter(PostModel.categorie_id == category_obj.categorie_id)

    # Filtering by author
    if author:
        user_obj = db.query(UserModel).filter(UserModel.username == author).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="Author not found")
        query = query.filter(PostModel.user_id == user_obj.user_id)

    # Sorting
    sort_options = {
        "-published_at": desc(PostModel.published_at),
        "published_at": asc(PostModel.published_at),
        "-author": desc(UserModel.username),
        "author": asc(UserModel.username),
    }
    if sort:
        if sort not in sort_options:
            raise HTTPException(status_code=400, detail="Invalid sort parameter")
        query = query.order_by(sort_options[sort])

    # Pagination
    offset = page * limit
    query = query.offset(offset).limit(limit)

    # Execute query
    posts = query.all()

    # Return response
    return posts

# Endpoint to create a new post
@router.post("/", response_model=PostResponse)
def create_post(
    post_req: PostReq,
    admin_id: AdminDep,
    db: Session = DBDep
):
    # Vérification si un post avec le même titre existe déjà
    existing_post = db.query(PostModel).filter_by(title=post_req.title).first()
    if existing_post:
        raise HTTPException(status_code=400, detail="Post with the same title already exists")

    # Création du post
    new_post = PostModel(
        user_id= admin_id,
        title=post_req.title,
        content=post_req.content,
        categorie_id=post_req.categorie_id,
        status=post_req.status,
        published_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Endpoint to update a post
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_req: PostReq,
    admin_id: AdminDep,
    db: Session = DBDep
):
    post = db.query(PostModel).filter_by(post_id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.user_id = admin_id
    post.title = post_req.title
    post.content = post_req.content
    post.categorie_id = post_req.categorie_id
    post.updated_at = datetime.now()
    db.commit()
    db.refresh(post)
    return post

# Endpoint to delete a post
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    admin_id: AdminDep,
    db: Session = DBDep
):
    post = db.query(PostModel).filter_by(post_id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"message": f"Post with ID {post_id} deleted successfully"}
