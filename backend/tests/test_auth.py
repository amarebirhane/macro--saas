import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test successful user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test user login after registration."""
    # 1. Register
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpassword123",
            "username": "loginuser"
        }
    )
    
    # 2. Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email": "login@example.com",
            "password": "loginpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with incorrect credentials."""
    # 1. Register
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "rightpassword123",
            "username": "wronguser"
        }
    )
    
    # 2. Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email": "wrong@example.com",
            "password": "wrongpassword123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email/username or password"
