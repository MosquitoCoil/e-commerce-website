from flask import Blueprint, render_template, session
from database.database import get_db_connection

home_bp = Blueprint("home",__name__,template_folder='/frontend/templates')

@home_bp.route("/home")
def home():
    products = [
        {
            "name": "Classic T-Shirt",
            "description": "Soft cotton T-shirt available in multiple colors. Perfect for everyday wear.",
            "price": 15.99,
            "image": "images/product1.jpg"
        },
        {
            "name": "Stylish Sneakers",
            "description": "Comfortable sneakers with modern design, great for casual outings.",
            "price": 45.00,
            "image": "images/product2.jpg"
        },
        {
            "name": "Leather Wallet",
            "description": "Durable leather wallet with multiple compartments for cards and cash.",
            "price": 25.50,
            "image": "images/product3.jpg"
        }
    ]
    return render_template("home.html", user=session.get("user"), products=products)