# test_app.py
import json
import pytest
from app import create_app, db, Product

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client

def test_create_product(client):
    resp = client.post(
        "/api/products",
        data=json.dumps({"name": "Laptop", "price": 1200.5}),
        content_type="application/json"
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1200.5

def test_get_products(client):
    # seed
    client.post(
        "/api/products",
        data=json.dumps({"name": "Phone", "price": 800}),
        content_type="application/json"
    )
    resp = client.get("/api/products")
    assert resp.status_code == 200
    products = resp.get_json()
    assert len(products) >= 1
