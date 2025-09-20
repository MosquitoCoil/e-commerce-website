from flask import Blueprint, session, render_template, redirect, url_for, flash
from ...utils.decorators import role_required
from database.database import get_db_connection
from datetime import datetime


clientOrders_bp = Blueprint(
    "clientOrders", __name__, template_folder="../../../frontend/templates/client"
)


# Show ALL orders of the client
@clientOrders_bp.route("/client/clientOrders")
@role_required("user")
def clientOrders():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your orders.", "error")
        return redirect(url_for("login.login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get all orders for this user
    cursor.execute(
        "SELECT id, total, created_at, status FROM orders WHERE user_id = %s ORDER BY created_at DESC",
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

    # ✅ Get purchase history
    cursor.execute(
        """
        SELECT id, order_id, product_name, quantity, price, total, received_at
        FROM purchase_history
        WHERE user_id = %s
        ORDER BY received_at DESC
        """,
        (user_id,),
    )
    purchases = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "clientOrders.html",
        orders=orders,
        order_items=order_items,
        purchases=purchases,
    )


# Show ONE specific order
@clientOrders_bp.route("/clientOrders/<int:order_id>")
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


@clientOrders_bp.route("/clientOrders/undo/<int:order_id>", methods=["POST"])
@role_required("user")
def undo_checkout(order_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to undo checkout.", "error")
        return redirect(url_for("login.login"))  # who owns the cart
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # ✅ Check if order exists and is still Pending
    cursor.execute(
        "SELECT id, status FROM orders WHERE id=%s AND user_id=%s",
        (order_id, user_id),
    )
    order = cursor.fetchone()

    if not order:
        flash("Order not found.", "error")
        cursor.close()
        db.close()
        return redirect(url_for("clientCart.clientCart"))

    if order["status"] != "Pending":
        flash("You can only undo orders that are still pending.", "error")
        cursor.close()
        db.close()
        return redirect(url_for("clientOrders.clientOrders"))

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
        cursor.execute(
            "SELECT id, quantity FROM cart WHERE user_id=%s AND product_id=%s",
            (user_id, item["product_id"]),
        )
        existing = cursor.fetchone()

        if existing:
            new_qty = existing["quantity"] + item["quantity"]
            cursor.execute(
                "UPDATE cart SET quantity=%s WHERE id=%s",
                (new_qty, existing["id"]),
            )
        else:
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                (user_id, item["product_id"], item["quantity"]),
            )

    # 3. Delete order + order_items
    cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Order has been undone and items restored to your cart.", "success")
    return redirect(url_for("clientCart.clientCart"))


@clientOrders_bp.route("/mark_as_received/<int:order_id>", methods=["POST"])
@role_required("user")
def mark_as_received(order_id):
    user_id = session.get("user_id")
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 1. Get all order items
    cursor.execute(
        """
        SELECT oi.product_id, oi.quantity, oi.price, p.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
        """,
        (order_id,),
    )
    order_items = cursor.fetchall()

    # 2. Insert each item into purchase_history
    for item in order_items:
        total = item["price"] * item["quantity"]

        # Check if product still exists (to avoid FK error)
        cursor.execute("SELECT id FROM products WHERE id = %s", (item["product_id"],))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(
                """
                INSERT INTO purchase_history 
                (user_id, order_id, product_id, product_name, quantity, price, total, received_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    order_id,
                    item["product_id"],
                    item["name"],
                    item["quantity"],
                    item["price"],
                    total,
                    datetime.now(),
                ),
            )
        else:
            # fallback: insert without product_id
            cursor.execute(
                """
                INSERT INTO purchase_history 
                (user_id, order_id, product_name, quantity, price, total, received_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    order_id,
                    item["name"],
                    item["quantity"],
                    item["price"],
                    total,
                    datetime.now(),
                ),
            )

    # 3. Update order status
    cursor.execute("UPDATE orders SET status = 'Received' WHERE id = %s", (order_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Order marked as received and added to purchase history!", "success")
    return redirect(url_for("clientOrders.clientOrders"))
