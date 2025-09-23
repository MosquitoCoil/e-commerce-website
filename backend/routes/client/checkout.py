from flask import Blueprint, redirect, url_for, flash, session
from ...utils.decorators import role_required
from database.database import get_db_connection

checkout_bp = Blueprint(
    "checkout", __name__, template_folder="../../../frontend/templates/client"
)


@checkout_bp.route("/client/checkout", methods=["POST"])
@role_required("user")
def checkout():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "danger")
        return redirect(url_for("login.login"))

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT c.id AS cart_id, c.product_id, p.image, p.name,
                   c.quantity, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            """,
            (user_id,),
        )
        cart_items = cursor.fetchall()

        if not cart_items:
            flash("Your cart is empty.", "danger")
            return redirect(url_for("addToCart.cart_page"))

        total = sum(item["price"] * item["quantity"] for item in cart_items)

        cursor.execute(
            "INSERT INTO orders (user_id, total, status) VALUES (%s, %s, %s)",
            (user_id, total, "Pending"),
        )
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                """,
                (order_id, item["product_id"], item["quantity"], item["price"]),
            )

        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        conn.commit()

        flash("Order placed successfully. Waiting for admin approval.", "success")
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f"Error during checkout: {e}", "danger")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect(url_for("clientOrders.clientOrders"))
