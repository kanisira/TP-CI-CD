# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()  # not bound yet

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

def create_app(test_config: dict | None = None):
    app = Flask(__name__)

    if test_config and "SQLALCHEMY_DATABASE_URI" in test_config:
        # Tests: SQLite in memory
        app.config["SQLALCHEMY_DATABASE_URI"] = test_config["SQLALCHEMY_DATABASE_URI"]
    else:
        # Runtime: MySQL via env vars
        DB_USER = os.getenv("MYSQL_USER", "root")
        DB_PASS = os.getenv("MYSQL_PASSWORD", "root")
        DB_HOST = os.getenv("MYSQL_HOST", "localhost")
        DB_PORT = os.getenv("MYSQL_PORT", "3306")
        DB_NAME = os.getenv("MYSQL_DB", "shop")
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.get("/api/products")
    def list_products():
        return jsonify([p.to_dict() for p in Product.query.all()])

    @app.post("/api/products")
    def create_product():
        data = request.get_json(force=True)
        p = Product(name=data["name"], price=float(data["price"]))
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    # local dev run
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
