from flask import Blueprint, session, render_template, redirect, url_for, flash
from ...utils.decorators import role_required
from database.database import get_db_connection
from datetime import datetime

clientOrders_bp = Blueprint(
    "clientOrders", __name__, template_folder="../../../frontend/templates/client"
)


@clientOrders_bp.route("/client/clientOrders")
@role_required("user")
def clientOrders():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your orders.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
            SELECT id, username, firstname, lastname, address, is_admin, created_at
            FROM users
            WHERE id = %s
            """,
        (user_id,),
    )
    user = cursor.fetchone()

    cursor.execute(
        """
        SELECT id, total, created_at, status
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    orders = cursor.fetchall()

    order_items = {}
    for order in orders:
        cursor.execute(
            """
            SELECT oi.product_id, oi.size, oi.quantity, oi.price, p.name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            """,
            (order["id"],),
        )
        order_items[order["id"]] = cursor.fetchall()

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
    conn.close()

    return render_template(
        "clientOrders.html",
        user=user,
        orders=orders,
        order_items=order_items,
        purchases=purchases,
    )


@clientOrders_bp.route("/clientOrders/<int:order_id>")
@role_required("user")
def view_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT o.id, o.total, o.created_at,
           oi.product_id, oi.size, oi.quantity, oi.price,
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
    conn.close()

    return render_template("clientOrderDetails.html", order=order_details)


@clientOrders_bp.route("/clientOrders/undo/<int:order_id>", methods=["POST"])
@role_required("user")
def undo_checkout(order_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to undo checkout.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, status FROM orders WHERE id=%s AND user_id=%s",
        (order_id, user_id),
    )
    order = cursor.fetchone()

    if not order:
        flash("Order not found.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("clientCart.cart_page"))

    if order["status"] != "Pending":
        flash("You can only undo orders that are still pending.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("clientOrders.clientOrders"))

    cursor.execute(
        "SELECT product_id, size, quantity FROM order_items WHERE order_id = %s",
        (order_id,),
    )
    items = cursor.fetchall()

    for item in items:
        cursor.execute(
            "SELECT id, quantity FROM cart WHERE user_id=%s AND product_id=%s AND size=%s",
            (user_id, item["product_id"], item["size"]),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE cart SET quantity=%s WHERE id=%s",
                (existing["quantity"] + item["quantity"], existing["id"]),
            )
        else:
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, size, quantity) VALUES (%s, %s, %s, %s)",
                (user_id, item["product_id"], item["size"], item["quantity"]),
            )

    cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Order has been undone and items restored to your cart.", "success")
    return redirect(url_for("clientCart.cart_page"))


@clientOrders_bp.route("/mark_as_received/<int:order_id>", methods=["POST"])
@role_required("user")
def mark_as_received(order_id):
    user_id = session.get("user_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT oi.product_id, p.name, oi.size, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
        """,
        (order_id,),
    )
    order_items = cursor.fetchall()

    for item in order_items:
        total = item["price"] * item["quantity"]

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

    cursor.execute("UPDATE orders SET status = 'Received' WHERE id = %s", (order_id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Order marked as received and added to purchase history!", "success")
    return redirect(url_for("clientOrders.clientOrders"))
