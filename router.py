from fastapi import APIRouter
from cloudflare import execute_sql

router = APIRouter()

# متغير بسيط يحفظ آخر نقطة وقفنا عندها
current_offset = 0
LIMIT = 5  # تقدر تخليها 10

@router.get("/posts")
def get_posts():
    global current_offset

    query = "SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?"
    posts = execute_sql(query, [LIMIT, current_offset])

    current_offset += LIMIT  # كل مرة يزود

    return posts


@router.post("/posts")
def add_post(title: str, link: str, likes: int):
    global current_offset

    query = "INSERT INTO posts (title, link, likes) VALUES (?, ?, ?)"
    result = execute_sql(query, [title, link, likes])

    # لما تضيف بوست جديد، نرجع من الأول عشان يظهر في الأول
    current_offset = 0

    return result


@router.delete("/posts/{post_id}")
def delete_post(post_id: int):
    query = "DELETE FROM posts WHERE id = ?"
    return execute_sql(query, [post_id])
