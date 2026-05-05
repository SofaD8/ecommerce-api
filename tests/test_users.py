from httpx import AsyncClient

from app.models.user_db import UserRole
from app.services.user_service import user_service
from app.schemas.user import UserCreate


async def test_admin_can_get_all_users(client: AsyncClient, db):
    admin_data = UserCreate(
        email="admin_list@example.com",
        password="super_secret_admin_password",
        full_name="Super Admin"
    )
    admin_user = await user_service.create(db, obj_in=admin_data)
    admin_user.role = UserRole.ADMIN
    await db.commit()

    login_res = await client.post(
        "/api/v1/users/login",
        data={"username": "admin_list@example.com", "password": "super_secret_admin_password"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/users/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


async def test_admin_can_delete_user(client: AsyncClient, db):
    admin = await user_service.create(db, obj_in=UserCreate(
        email="admin_del@example.com", password="secure_password_123", full_name="Admin"
    ))
    admin.role = UserRole.ADMIN
    await db.commit()

    victim = await user_service.create(db, obj_in=UserCreate(
        email="victim@example.com", password="secure_password_123", full_name="Victim"
    ))

    login_res = await client.post(
        "/api/v1/users/login",
        data={"username": "admin_del@example.com", "password": "secure_password_123"}
    )
    token = login_res.json()["access_token"]

    response = await client.delete(
        f"/api/v1/users/{victim.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    deleted_user = await user_service.get_by_id(db, obj_id=victim.id)
    assert deleted_user is None


async def test_admin_access_denied_for_regular_user(client: AsyncClient, db):
    user_data = {
        "email": "user@test.com",
        "password": "secure_password_123",
        "full_name": "Regular User"
    }
    await client.post("/api/v1/users/", json=user_data)

    login_res = await client.post(
        "/api/v1/users/login",
        data={"username": "user@test.com", "password": "secure_password_123"}
    )
    token = login_res.json()["access_token"]

    response = await client.delete(
        "/api/v1/users/999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


async def test_register_user_success(client: AsyncClient):
    payload = {
        "email": "new_unique_user@example.com",
        "password": "strong_password_123",
        "full_name": "Test User"
    }
    response = await client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new_unique_user@example.com"
    assert "id" in data
    assert data["role"] == UserRole.USER


async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "password123_secure",
        "full_name": "First User"
    }
    await client.post("/api/v1/users/", json=payload)

    response = await client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_login_success(client: AsyncClient):
    email = "login_unique@example.com"
    password = "secret_password_123"

    await client.post("/api/v1/users/", json={
        "email": email,
        "password": password,
        "full_name": "Login Tester"
    })

    response = await client.post(
        "/api/v1/users/login",
        data={"username": email, "password": password}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_get_all_users_forbidden_for_regular_user(client: AsyncClient):
    email = "user@example.com"
    password = "password123_secure"
    await client.post("/api/v1/users/", json={
        "email": email, "password": password, "full_name": "Regular User"
    })

    login_res = await client.post(
        "/api/v1/users/login",
        data={"username": email, "password": password}
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users/", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"
