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
        
        return posts