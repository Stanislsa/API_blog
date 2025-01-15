from fastapi import APIRouter

from app.db import get_conn

router = APIRouter(prefix="/manage")

# @router.get("/ping")
# def ping():
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("select 1")
#         record = cursor.fetchone()
#         cursor.close()
#         print(record)
#         return "pong"

@router.get("/ping")
def ping():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            record = cursor.fetchone()
            print(record)
            return "pong"