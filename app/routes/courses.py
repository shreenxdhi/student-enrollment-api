from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post("/", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: schemas.CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    existing_course = db.query(models.Course).filter(models.Course.course_code == course.course_code).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
        
    new_course = models.Course(**course.model_dump())
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course

@router.get("/", response_model=List[schemas.CourseResponse])
def get_all_courses(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Course).all()

@router.get("/{id}", response_model=schemas.CourseResponse)
def get_course(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{id}", response_model=schemas.CourseResponse)
def update_course(
    id: int, 
    updated_course: schemas.CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    course_query.update(updated_course.model_dump(), synchronize_session=False)
    db.commit()
    
    return course_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    db.delete(course)
    db.commit()
    
    return None
