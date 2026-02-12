import pytest
import random
import string

# Helper to generate random email
def random_email():
    return f"{''.join(random.choices(string.ascii_lowercase, k=10))}@example.com"

# --- UNIT TESTS (Small Checks) ---

def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to the DocuSafe API"}

def test_create_user_success(client):
    email = random_email()
    payload = {
        "email": email,
        "password": "strongpassword123", # FIXED: Must be >6 chars
        "name": "Test Master",
        "experience_years": 5
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 201
    assert res.json()["email"] == email

def test_create_user_weak_password(client):
    """Test that Schema Hardening blocks weak passwords"""
    payload = {
        "email": random_email(),
        "password": "123", # Too short!
        "name": "Hacker",
        "experience_years": 1
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 422 # Expecting Rejection

# --- INTEGRATION TEST (The Grand Slam) ---

def test_full_workflow(client):
    """
    The Grand Slam: Register -> Login -> Create Document
    """
    email = random_email()
    password = "strongpassword123" # FIXED: Length > 6

    # 1. Register
    client.post("/users", json={
        "email": email, "password": password, 
        "name": "Grand Slam User", "experience_years": 2
    })

    # 2. Login
    login_res = client.post("/login", data={"username": email, "password": password})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # 3. Create Document (Authenticated)
    headers = {'Authorization': f'Bearer {token}'}
    doc_res = client.post(
        "/documents/",
        json={"title": "Secret Doc", "content": "Classified Info"},
        headers=headers
    )
    assert doc_res.status_code == 201
    assert doc_res.json()["title"] == "Secret Doc"