from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from sqlalchemy.orm import Session
from typing import Optional
from app.core.dependencies import AdminDep, DBDep
from app.models.models import Post as PostModel

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
@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = DBDep):
    posts = db.query(PostModel).all()
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
