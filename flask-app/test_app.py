# test_app.py
import json
import pytest
from app import app, db, Product

@pytest.fixture
def client():
    # configuration spéciale pour tests (base SQLite en mémoire)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    # nettoyage
    with app.app_context():
        db.drop_all()

def test_create_product(client):
    response = client.post(
        "/api/products",
        data=json.dumps({"name": "Laptop", "price": 1200.50}),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1200.50

def test_get_products(client):
    # d'abord on ajoute un produit
    client.post(
        "/api/products",
        data=json.dumps({"name": "Phone", "price": 800}),
        content_type="application/json"
    )
    # puis on récupère
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) >= 1
    assert "name" in products[0]
    assert "price" in products[0]
