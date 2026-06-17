from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

@router.post("/", response_model=schemas.EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(
    enrollment: schemas.EnrollmentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing_enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
        
    new_enrollment = models.Enrollment(**enrollment.model_dump())
    
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment

@router.get("/", response_model=List[schemas.EnrollmentResponse])
def get_all_enrollments(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Enrollment).all()

@router.get("/student/{student_id}", response_model=List[schemas.EnrollmentResponse])
def get_student_enrollments(
    student_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_enrollment(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment record not found")
        
    db.delete(enrollment)
    db.commit()
    
    return None
