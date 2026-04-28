import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.product_service import products_db


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    products_db.clear()
    import app.services.product_service as service

    service.next_product_id = 1


def test_create_product():
    response = client.post(
        "/api/v1/products/",
        json={"name": "Laptop", "price": 999.999, "description": "High-end laptop"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1000.0
    assert data["id"] == 1


def test_get_products_filtering():
    client.post("/api/v1/products/", json={"name": "Apple", "price": 10.0})
    client.post("/api/v1/products/", json={"name": "Banana", "price": 20.0})
    client.post("/api/v1/products/", json={"name": "Cherry", "price": 30.0})

    response = client.get("/api/v1/products/?min_price=15&max_price=25")
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Banana"

    response = client.get("/api/v1/products/?name=ap")
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Apple"


def test_update_product_partial():
    client.post("/api/v1/products/", json={"name": "Old Name", "price": 50.0})

    response = client.patch("/api/v1/products/1", json={"price": 75.555})
    assert response.status_code == 200
    assert response.json()["price"] == 75.56
    assert response.json()["name"] == "Old Name"


def test_delete_product():
    client.post("/api/v1/products/", json={"name": "To be deleted", "price": 10.0})

    delete_response = client.delete("/api/v1/products/1")
    assert delete_response.status_code == 204

    get_response = client.get("/api/v1/products/1")
    assert get_response.status_code == 404


def test_get_product_not_found():
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
