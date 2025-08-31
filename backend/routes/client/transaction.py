from flask import Blueprint, session, render_template, redirect, url_for, flash
from ...utils.decorators import role_required
from database.database import get_db_connection

transaction_bp = Blueprint(
    "transaction", __name__, template_folder="../../../frontend/templates/client"
)


# Show ALL orders of the client
@transaction_bp.route("/transaction")
@role_required("user")
def transaction():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your orders.", "error")
        return redirect(url_for("auth.login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get all orders for this user
    cursor.execute(
        "SELECT id, total, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )
    orders = cursor.fetchall()

    # Get order items for each order
    order_items = {}
    for order in orders:
        cursor.execute(
            """
            SELECT oi.product_id, oi.quantity, oi.price, p.name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            """,
            (order["id"],),
        )
        order_items[order["id"]] = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("clientOrders.html", orders=orders, order_items=order_items)


# Show ONE specific order
@transaction_bp.route("/transaction/<int:order_id>")
@role_required("user")
def view_order(order_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT o.id, o.total, o.created_at,
               oi.product_id, oi.quantity, oi.price,
               p.name
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.id = %s
        """,
        (order_id,),
    )
    order_details = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("clientOrderDetails.html", order=order_details)


@transaction_bp.route("/transaction/undo/<int:order_id>", methods=["POST"])
@role_required("user")
def undo_checkout(order_id):
    user_id = session["user_id"]  # who owns the cart
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 1. Get all items from this order
    cursor.execute(
        """
        SELECT product_id, quantity
        FROM order_items
        WHERE order_id = %s
    """,
        (order_id,),
    )
    items = cursor.fetchall()

    # 2. Insert back into cart
    for item in items:
        # Check if already in cart
        cursor.execute(
            """
            SELECT id, quantity FROM cart
            WHERE user_id = %s AND product_id = %s
        """,
            (user_id, item["product_id"]),
        )
        existing = cursor.fetchone()

        if existing:
            # Update quantity
            new_qty = existing["quantity"] + item["quantity"]
            cursor.execute(
                """
                UPDATE cart SET quantity = %s
                WHERE id = %s
            """,
                (new_qty, existing["id"]),
            )
        else:
            # Insert new row
            cursor.execute(
                """
                INSERT INTO cart (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """,
                (user_id, item["product_id"], item["quantity"]),
            )

    # 3. Delete order + order_items
    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Order has been undone and items restored to your cart.", "success")
    return redirect(url_for("cart.cart"))
