from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    existing_student = db.query(models.Student).filter(
        (models.Student.student_id == student.student_id) | (models.Student.email == student.email)
    ).first()
    
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID or Email already registered")
        
    new_student = models.Student(**student.model_dump())
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student

@router.get("/", response_model=List[schemas.StudentResponse])
def get_all_students(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Student).all()

@router.get("/{id}", response_model=schemas.StudentResponse)
def get_student(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{id}", response_model=schemas.StudentResponse)
def update_student(
    id: int, 
    updated_student: schemas.StudentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    student_query.update(updated_student.model_dump(), synchronize_session=False)
    db.commit()
    
    return student_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    db.delete(student)
    db.commit()
    
    return None
