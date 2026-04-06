from fastapi import APIRouter
from cloudflare import execute_sql

router = APIRouter()

current_offset = 0
LIMIT = 5

@router.get("/posts")
def get_posts():
    global current_offset

    query = "SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?"
    posts = execute_sql(query, [LIMIT, current_offset])

    # لو مفيش نتائج، ارجع من الأول
    if not posts:
        current_offset = 0
        posts = execute_sql(query, [LIMIT, current_offset])

    current_offset += LIMIT

    return posts
