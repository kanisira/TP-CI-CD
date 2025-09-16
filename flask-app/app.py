from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config MySQL (env vars ou valeurs par défaut)
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DB", "shop")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

with app.app_context():
    db.create_all()

@app.route("/api/products", methods=["GET"])
def list_products():
    return jsonify([p.to_dict() for p in Product.query.all()])

@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    p = Product(name=data["name"], price=data["price"])
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
