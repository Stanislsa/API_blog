from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.dependencies import DBDep, AuthDep, AdminDep, JwtDep
from psycopg2.extras import DictCursor
from psycopg2.extras import RealDictCursor
from psycopg2 import errors

router = APIRouter(prefix="/posts")

class User(BaseModel):
    user_id: int
    username: str

class Category(BaseModel):
    categorie_id: int
    name: str

class Post(BaseModel):
    post_id: int
    user_id: int
    categorie_id: int
    title: str | None
    content: str | None
    status: str
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    user: Optional[User] = None
    category: Optional[Category] = None

class UpdatePostReq(BaseModel):
    post_id: int
    user_id: int
    categorie_id: int
    title: str | None
    content: str | None
    status: str
    published_at: datetime | None
    updated_at: datetime
    

@router.get("/")
def get_posts(conn: DBDep, jwt_payload: JwtDep, category: Optional[str] = None, author: Optional[str] = None, sort: Optional[str] = None, page: int = 0):
    with (
        conn.cursor(cursor_factory=DictCursor) as post_cursor, 
        conn.cursor(cursor_factory=DictCursor) as category_cursor, 
        conn.cursor(cursor_factory=DictCursor) as users_cursor
    ):
        
        params = {}
        
        if not jwt_payload:
            sql = "select * from posts where status = 'public'"
        elif jwt_payload["is_admin"]:
            sql = "select * from posts where 1 = 1"
        elif not jwt_payload["is_admin"]:
            sql = "select * from posts where status != 'draft'"
        
        if category:
            category_cursor.execute("select * from categories where name = %s", [category])
            category_record = category_cursor.fetchone()
            if not category_record:
                raise HTTPException(status_code=404, detail="category not found")

            sql += " and categorie_id = %(categorie_id)s"
            params["categorie_id"] = category_record["categorie_id"]  
            
        if author:
            users_cursor.execute("select * from users where username = %s", [author])
            users_record = users_cursor.fetchone()
            if not users_record:
                raise HTTPException(status_code=404, detail="auther not found")
            
            sql += " and user_id = %(user_id)s"
            params["user_id"] = users_record["user_id"]  
        
        if sort:
            match sort:
                case "-published_at":
                    sql += " order by published_at desc"
                case "published_at":
                    sql += " order by published_at asc"
                case _:
                    HTTPException(status_code=400, detail="invalid sort param")
                    
        limit = 10
        offset = 0
        
        if page:
            offset = page * limit
            
        sql += " limit %(limit)s offset %(offset)s"
        params["limit"] = limit
        params["offset"] = offset
                
        post_cursor.execute(sql, params)
        records = post_cursor.fetchall()
        posts = [
            Post(
                post_id= record["post_id"],
                user_id= record["user_id"],
                categorie_id= record["categorie_id"],
                title= record["title"],
                content= record["content"],
                status= record["status"],
                published_at= record["published_at"],
                created_at= record["created_at"],
                updated_at= record["updated_at"]
            )
            for record in records
        ]
        
        print(sql)
        print(params)
        
        category_ids = [post.categorie_id for post in posts]
        category_cursor.execute("select * from categories where categorie_id = any(%s)", [category_ids])
        categories = category_cursor.fetchall()
        category_dict = {category["categorie_id"]: Category(**category) for category in categories}
        
        post_user_ids = [post.user_id for post in posts]
        users_cursor.execute("select * from users where user_id = any(%s)", [post_user_ids])
        users = users_cursor.fetchall()
        user_dict = {user["user_id"]: User(**user) for user in users}
                
        for post in posts:
            post.category = category_dict.get(post.categorie_id)
            post.user = user_dict.get(post.user_id)

            post.category = {
                "categorie_id": post.category.categorie_id,
                "name": post.category.name
            } if post.category else None
            
            post.user = {
                "user_id": post.user.user_id,
                "username": post.user.username
            } if post.user else None

        return posts
    
@router.get("/{post_id}")
def get_post(post_id: int, jwt_payload: JwtDep, conn:DBDep):
    with conn.cursor(cursor_factory=DictCursor) as post_cursor:
        if not jwt_payload:
            sql = "select * from posts where status = 'public'"
        elif jwt_payload["is_admin"]:
            sql = "select * from posts where 1 = 1"
        elif not jwt_payload["is_admin"]:
            sql = "select * from posts where status != 'draft'"
            
        sql += " and post_id = %s"
        post_cursor.execute(sql, [post_id])
        post_record = post_cursor.fetchone()
        
        if not post_record:
            raise HTTPException(status_code=404, detail="post not found")
        
        post = {
            "post_id": post_record["post_id"],
            "user_id": post_record["user_id"],
            "categorie_id": post_record["categorie_id"],
            "title": post_record["title"],
            "content": post_record["content"],
            "status": post_record["status"],
            "published_at": post_record["published_at"],
            "created_at": post_record["created_at"],
            "updated_at": post_record["updated_at"],
        }
        
        return Post(**post)
    
@router.put("/{post_id}")
def update_post(post_id: int, update_poste_req: UpdatePostReq, is_admin: AdminDep, conn: DBDep):
    post = {
        "post_id": post_id,
        "user_id": update_poste_req.user_id,
        "categorie_id": update_poste_req.categorie_id,
        "title": update_poste_req.title,
        "content": update_poste_req.content,
        "status": update_poste_req.status,
        "published_at": update_poste_req.published_at,
        "updated_at": update_poste_req.updated_at,
    }

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE posts 
            SET user_id = %(user_id)s, 
                categorie_id = %(categorie_id)s, 
                title = %(title)s, 
                content = %(content)s, 
                status = %(status)s, 
                published_at = %(published_at)s, 
                updated_at = %(updated_at)s 
            WHERE post_id = %(post_id)s 
            RETURNING *;
            """,
            post,
        )
        record = cursor.fetchone()
        
        if not record:
            raise HTTPException(status_code=404, detail="Post not found")

        # Récupérer l'utilisateur associé
        cursor.execute("SELECT * FROM users WHERE user_id = %s", [record["user_id"]])
        user_record = cursor.fetchone()
        user = User(**user_record) if user_record else None

        # Récupérer la catégorie associée
        cursor.execute("SELECT * FROM categories WHERE categorie_id = %s", [record["categorie_id"]])
        category_record = cursor.fetchone()
        category = Category(**category_record) if category_record else None

        # Retourner le post sous forme de DTO
        updated_post = Post(
            post_id=record["post_id"],
            user_id=record["user_id"],
            categorie_id=record["categorie_id"],
            title=record["title"],
            content=record["content"],
            status=record["status"],
            published_at=record["published_at"],
            created_at=record["created_at"],
            updated_at=record["updated_at"],
            user=user,
            category=category,
        )
        return updated_post