import os
from fastapi import APIRouter, Depends, HTTPException
from groq import Groq

from app.schemas import schemas
from app.models import models
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/advisor",
    tags=["AI Academic Advisor"]
)

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    client = None

@router.post("/chat", response_model=schemas.AdvisorResponse)
def chat_with_advisor(
    request: schemas.AdvisorRequest,
    current_user: models.User = Depends(get_current_user)
):
    if not client:
        raise HTTPException(status_code=500, detail="Groq API key is missing or invalid.")
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, professional academic advisor for a university computer science department. You help students pick classes, explain concepts, and plan their degrees."
                },
                {
                    "role": "user",
                    "content": request.question,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=500,
        )
        
        answer_text = chat_completion.choices[0].message.content
        
        return {"answer": answer_text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Advisor error: {str(e)}")
