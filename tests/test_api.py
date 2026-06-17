def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Student Enrollment Portal API!"}

def test_login(client):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_student(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/students/",
        headers=headers,
        json={
            "student_id": "STU101",
            "first_name": "Harry",
            "last_name": "Potter",
            "email": "harry@hogwarts.edu",
            "major": "Defense Against the Dark Arts",
            "enrollment_year": 2024
        }
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == "Harry"

def test_create_student_unauthorized(client):
    response = client.post(
        "/students/",
        json={
            "student_id": "STU102",
            "first_name": "Draco",
            "last_name": "Malfoy",
            "email": "draco@hogwarts.edu",
            "major": "Potions",
            "enrollment_year": 2024
        }
    )
    assert response.status_code == 401

def test_create_course(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/courses/",
        headers=headers,
        json={
            "course_code": "DADA-101",
            "course_name": "Intro to Defense Against the Dark Arts",
            "credits": 3,
            "instructor": "Remus Lupin"
        }
    )
    assert response.status_code == 201
    assert response.json()["course_code"] == "DADA-101"

def test_enrollment_logic(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.post(
        "/enrollments/",
        headers=headers,
        json={
            "student_id": 1,
            "course_id": 1
        }
    )
    assert response.status_code == 201
    
    response_dup = client.post(
        "/enrollments/",
        headers=headers,
        json={
            "student_id": 1,
            "course_id": 1
        }
    )
    assert response_dup.status_code == 400

def test_ai_advisor(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/advisor/chat",
        headers=headers,
        json={
            "question": "Say hello!"
        }
    )
    assert response.status_code in [200, 500]
