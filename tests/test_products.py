from httpx import AsyncClient


async def test_create_product_with_keywords(client: AsyncClient):
    payload = {
        "name": "Coffee Bean",
        "price": 12.556,
        "description": "Premium dark roast",
        "keyword": ["coffee", "beverage", "dark"]
    }
    response = await client.post("/api/v1/products/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Coffee Bean"
    assert data["price"] == 12.56
    assert data["keyword"] == ["coffee", "beverage", "dark"]


async def test_search_by_keyword_in_array(client: AsyncClient):
    await client.post("/api/v1/products/", json={
        "name": "Green Tea",
        "price": 5.0,
        "description": "Healthy drink",
        "keyword": ["tea", "green"]
    })

    response = await client.get("/api/v1/products/?keyword=green")

    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(item["name"] == "Green Tea" for item in results)


async def test_search_by_keyword_in_description(client: AsyncClient):
    unique_name = "Latte Special Mixture"
    await client.post("/api/v1/products/", json={
        "name": unique_name,
        "price": 4.5,
        "description": "Milk and espresso mixture",
        "keyword": ["coffee"]
    })

    response = await client.get("/api/v1/products/?keyword=mixture")

    assert response.status_code == 200
    results = response.json()

    names = [item["name"] for item in results]
    assert unique_name in names
