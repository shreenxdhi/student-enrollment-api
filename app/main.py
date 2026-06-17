from fastapi import FastAPI
from app.database.database import engine
from app.models import models
from app.routes import auth

# Create the database tables
models.Base.metadata.create_all(bind=engine)

from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(
    title="Student Enrollment Portal API",
    description="REST API for a university enrollment management system",
    version="1.0.0"
)

@app.get("/migrate")
def run_migration():
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;"))
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register our routers
app.include_router(auth.router)
from app.routes import students, courses, enrollments, advisor
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(advisor.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Enrollment Portal API!"}

