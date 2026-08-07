import uuid

import pytest
from fastapi.testclient import TestClient

# Import our FastAPI app instance
from src.api.routes import app


@pytest.fixture
def client():
    """
    Provides a FastAPI test client for subsequent test
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def random_user():
    """
    Generates a random/unique user credentials payload per run
    """
    unique_id = uuid.uuid4().hex[:8]
    return {
        'email': f'user_{unique_id}@example.com',
        'username': f'user_{unique_id}@example.com',
        'password': 'testPassword123!',
    }


# PUBLIC ROUTES


def test_root_endpoint(client):
    """
    Verifies that the root is reachable .
    """
    response = client.get('/')
    assert response.status_code == 200


# AUTH


def test_register_user_success(client, random_user):
    """
    Tests is a new user can succesfully register.
    """
    response = client.post('/register', json=random_user)
    assert response.status_code in (200, 201)


def test_login_invalid_credentials(client):
    """
    Checks if non valid credentials are rejected
    """
    payload = {'username': 'nonexistent@example.com', 'password': 'wrongpassword'}
    response = client.post('/login', data=payload)
    assert response.status_code in (400, 401)


# PROTECTED ROUTES


def test_protected_route_unauthorized_without_token(client):
    """
    Tests if protected endpoints reject requests missing an auth header
    """
    response = client.get('/transactions')
    assert response.status_code == 401


def test_protected_route_unauthorized_invalid_token(client):
    """
    Tests if protected endpoints reject requests with invalid bearer token
    """
    headers = {'Authorization': 'Bearer invalid_token_123'}
    response = client.get('/transactions', headers=headers)
    assert response.status_code == 401


def test_full_auth_and_protected_access_flow(client, random_user):
    """
    End-to-end integration test verifying the complete user auth cycle
    """
    # Register
    reg_response = client.post('/register', json=random_user)
    assert reg_response.status_code in (200, 201)

    # Login
    login_payload = {
        'username': random_user['email'],
        'password': random_user['password'],
    }
    login_response = client.post('/login', data=login_payload)
    assert login_response.status_code == 200

    token_data = login_response.json()
    assert 'access_token' in token_data

    # 3. Access protected route
    headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
    protected_response = client.get('/transactions', headers=headers)
    assert protected_response.status_code == 200
