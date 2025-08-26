from flask import Blueprint, redirect, url_for, flash, request, session
from ..utils.decorators import role_required
from database.database import get_db_connection

addToCart_bp = Blueprint('addToCart', __name__, template_folder='../../frontend/templates/client')

@addToCart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
@role_required('user')
def addToCart(product_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch product info
    cursor.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("home.home"))  # adjust to your product list route

    cart = session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)] = {
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": 1
        }

    session["cart"] = cart
    flash(f"Added {product['name']} to cart!", "success")
    return redirect(url_for("home.home"))  # go back to shop