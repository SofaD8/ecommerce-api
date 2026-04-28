from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_read_product():
    payload = {"name": "Smart Watch", "price": 99.999}
    post_res = client.post("/api/v1/products/", json=payload)
    assert post_res.status_code == 200

    created_product = post_res.json()
    product_id = created_product["id"]
    assert created_product["price"] == 100.0

    get_res = client.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Smart Watch"
