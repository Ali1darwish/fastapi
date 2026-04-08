from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from cloudflare import execute_sql

router = APIRouter()

# =========================
# Helper (حماية بسيطة)
# =========================
def safe(text: str) -> str:
    return text.replace("'", "''")


# =========================
# Models
# =========================
class QuestionRequest(BaseModel):
    question: str
    questioner: str


class AnswerRequest(BaseModel):
    answer: str


# =========================
# 1. ADD QUESTION
# =========================
@router.post("/questions")
async def add_question(data: QuestionRequest):
    try:
        question = safe(data.question)
        questioner = safe(data.questioner)

        query = f"""
        INSERT INTO questions (question, questioner, answered, likes)
        VALUES ('{question}', '{questioner}', 0, 0)
        """
        execute_sql(query=query)

        return {"message": "Question added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 2. GET QUESTIONS (pagination)
# =========================
@router.get("/questions")
async def get_questions(page: int = 1, limit: int = 5):
    try:
        offset = (page - 1) * limit

        query = f"SELECT * FROM questions LIMIT {limit} OFFSET {offset}"
        result = execute_sql(query=query)

        return {
            "page": page,
            "count": len(result),
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 3. ADD ANSWER
# =========================
@router.post("/questions/{question_id}/answer")
async def answer_question(question_id: int, data: AnswerRequest):
    try:
        # check if exists
        check_query = f"SELECT id FROM questions WHERE id = {question_id}"
        question = execute_sql(query=check_query)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        answer = safe(data.answer)

        update_query = f"""
        UPDATE questions
        SET answer = '{answer}', answered = 1
        WHERE id = {question_id}
        """
        execute_sql(query=update_query)

        return {
            "message": "Answer added successfully",
            "answered": True
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 4. LIKE QUESTION
# =========================
@router.post("/questions/{question_id}/like")
async def like_question(question_id: int):
    try:
        check_query = f"SELECT id FROM questions WHERE id = {question_id}"
        question = execute_sql(query=check_query)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        update_query = f"""
        UPDATE questions
        SET likes = COALESCE(likes, 0) + 1
        WHERE id = {question_id}
        """
        execute_sql(query=update_query)

        return {"message": "Like added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 5. DELETE QUESTION
# =========================
@router.delete("/questions/{question_id}")
async def delete_question(question_id: int):
    try:
        # تأكد إن السؤال موجود
        check_query = f"SELECT id FROM questions WHERE id = {question_id}"
        question = execute_sql(query=check_query)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # حذف السؤال
        delete_query = f"DELETE FROM questions WHERE id = {question_id}"
        execute_sql(query=delete_query)

        return {"message": "Question deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))