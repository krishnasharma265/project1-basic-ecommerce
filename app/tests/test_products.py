from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    login_data = {
        "username": "KRISHNA",
        "password": "123456"
    }

    login_response = client.post(
        "/auth/login",
        json=login_data
    )

    print(login_response.json())
    token = login_response.json()["data"]["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/products",
        headers=headers
    )

    # response = client.get("/products")

    assert response.status_code == 200