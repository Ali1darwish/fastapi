from fastapi import APIRouter
from cloudflare import execute_sql

router = APIRouter()

current_offset = 0
LIMIT = 5  # غيرها لـ 10 لو عايز

@router.get("/posts")
def get_posts():
    global current_offset

    query = "SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?"
    
    result = execute_sql(query, [LIMIT, current_offset])

    # ناخد الداتا الصح من Cloudflare
    posts = result["result"][0]["results"]

    # لو مفيش بيانات (وصلنا للآخر) نرجع من الأول
    if not posts:
        current_offset = 0
        result = execute_sql(query, [LIMIT, current_offset])
        posts = result["result"][0]["results"]

    current_offset += LIMIT

    return posts


@router.post("/posts")
def add_post(title: str, link: str, likes: int):
    global current_offset

    query = "INSERT INTO posts (title, link, likes) VALUES (?, ?, ?)"
    result = execute_sql(query, [title, link, likes])

    # عشان الجديد يظهر الأول
    current_offset = 0

    return result


@router.delete("/posts/{post_id}")
def delete_post(post_id: int):
    query = "DELETE FROM posts WHERE id = ?"
    return execute_sql(query, [post_id])
