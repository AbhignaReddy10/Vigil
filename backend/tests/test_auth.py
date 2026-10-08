def test_register_new_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "ammu@example.com", "password": "StrongPass123", "full_name": "Ammu"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "ammu@example.com"
    assert body["role"] == "analyst"
    assert "hashed_password" not in body  # must never leak


def test_register_duplicate_email_rejected(client):
    payload = {"email": "dupe@example.com", "password": "StrongPass123", "full_name": "Dupe"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_with_correct_credentials_returns_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "StrongPass123", "full_name": "Login Test"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "StrongPass123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_with_wrong_password_rejected(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "StrongPass123", "full_name": "Test"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpass@example.com", "password": "WrongPassword"},
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_with_valid_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "me@example.com", "password": "StrongPass123", "full_name": "Me Test"},
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "me@example.com", "password": "StrongPass123"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
