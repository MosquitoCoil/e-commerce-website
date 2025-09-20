from flask import Blueprint, redirect, url_for, flash, session
from ...utils.decorators import role_required
from database.database import get_db_connection

checkout_bp = Blueprint(
    "checkout", __name__, template_folder="../../../frontend/templates/client"
)


@checkout_bp.route("/client/checkout", methods=["POST"])
@role_required("user")  # if you also want admins allowed, remove this line
def checkout():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "error")
        return redirect(url_for("login.login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch all cart items for the user
    cursor.execute(
        """
        SELECT c.id as cart_id, c.product_id, p.image, p.name, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """,
        (user_id,),
    )
    cart_items = cursor.fetchall()

    if not cart_items:
        flash("Your cart is empty!", "error")
        return redirect(url_for("clientCart.clientCart"))

    # Calculate total
    total = sum(item["price"] * item["quantity"] for item in cart_items)

    # Insert into orders
    cursor.execute(
        "INSERT INTO orders (user_id, total, status) VALUES (%s, %s, %s)",
        (user_id, total, "Pending"),
    )
    order_id = cursor.lastrowid

    # Insert order items
    for item in cart_items:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, price) 
            VALUES (%s, %s, %s, %s)
        """,
            (order_id, item["product_id"], item["quantity"], item["price"]),
        )

    # Clear cart
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Order placed successfully! Waiting for admin approval.", "success")
    return redirect(url_for("clientOrders.clientOrders"))
