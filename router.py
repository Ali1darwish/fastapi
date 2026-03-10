from fastapi import APIRouter
from cloudflare import execute_sql

router = APIRouter()

@router.get("/posts")
def get_posts():
    query = "SELECT * FROM posts"
    return execute_sql(query)


@router.post("/posts")
def add_post(title: str, link: str,likes: int):
    query = "INSERT INTO posts (title, link,likes) VALUES (?, ?, ?)"
    return execute_sql(query, [title, link,likes])


@router.delete("/posts/{post_id}")
def delete_post(post_id: int):
    query = "DELETE FROM posts WHERE id = ?"
    return execute_sql(query, [post_id])
