from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    major: str
    enrollment_year: int

class StudentResponse(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    major: str
    enrollment_year: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    course_code: str
    course_name: str
    credits: int
    instructor: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    course_code: str
    course_name: str
    credits: int
    instructor: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: datetime
    status: str
    
    student: StudentResponse
    course: CourseResponse
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdvisorRequest(BaseModel):
    question: str

class AdvisorResponse(BaseModel):
    answer: str
