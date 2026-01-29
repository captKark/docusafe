from fastapi.testclient import TestClient # <-- Import TestClient
from main import app
import random # for generating random numbers
import string # for generating random strings

# Create a TestClient using the FastAPI app
client = TestClient(app)

# Test root endpoint
def test_root_endpoint():
    '''
    Checks if the root endoint returns a 200 OK response and Welcome message
    '''
    response = client.get("/") # <-- Assuming there's a root endpoint

    # The Assertion- Did it work?
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DocuSafe API"}

# test maths sanity check
def test_math_sanity_check():
    '''
    A simple sanity check to ensure the testing framework is working
    '''
    assert 2 + 2 == 4

# Helper function to generate random text
def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def test_create_user():
    random_email = f"{random_string()}@example.com"
    random_password = "password123"

    response = client.post(
            "/users", 
            json={
                "email": random_email, 
                "password": random_password,
                "name": "Test Robot",      # <--- Added field
                "experience_years": 1      # <--- Added field
            }
        )

    # --- DEBUGGING BLOCK ---
    if response.status_code != 201:
        print("\n⚠️ TEST FAILED. API Response:", response.json())
    # -----------------------

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == random_email
    assert "password" not in data

# Test Full Worlflow
def test_full_workflow():
    """
    The Grand Slam Test:
    1. Register new user
    2. Login to get Token
    3. Use Token to create a document
    4. Verify document creation
    """
    # Step 1: Register new user
    email = f"{random_string()}@example.com"
    password = "123"
    response = client.post(
        "/users",
        json={
            "email": email,
            "password":password,
            "name": "Tester",
            "experience_years": 2
        }
    )

    # Step 2: Login to get Token
    login_response = client.post(
        "/login",
        data = {"username": email, "password": password} # Note: OAuth2 uses 'username' field for email
    )

    assert login_response.status_code == 200 # <-- Ensure login worked
    token = login_response.json()['access_token'] # <-- Extract Token

    # Step 3: Use Token to create a document
    # We add the Authorization Header: Bearer <token>
    headers = {'Authorization': f'Bearer {token}'}

    # Create Document Data
    doc_data = {
        "title": "Test Document",
        "content": "This is a test document content." 
    }

    create_response = client.post(
        "/documents/",
        json=doc_data,
        headers=headers
    )

    # Step 4: Verify document creation
    assert create_response.status_code == 201
    created_doc = create_response.json() #<-- Extract created document data
    assert created_doc["title"] == "Test Document"
    assert created_doc["content"] == doc_data["content"]
    assert created_doc['owner_id'] is not None # <-- Ensure owner_id is set
