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
    return app.test_client()

def test_create_product(client):
    r = client.post(
        "/api/products",
        data=json.dumps({"name": "Laptop", "price": 1200.5}),
        content_type="application/json",
    )
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1200.5

def test_get_products(client):
    client.post(
        "/api/products",
        data=json.dumps({"name": "Phone", "price": 800}),
        content_type="application/json",
    )
    r = client.get("/api/products")
    assert r.status_code == 200
    products = r.get_json()
    assert len(products) >= 1
