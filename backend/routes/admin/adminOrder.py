from flask import Blueprint, render_template, redirect, url_for, flash, session
from database.database import get_db_connection
from ...utils.decorators import role_required

adminOrders_bp = Blueprint(
    "adminOrders",
    __name__,
    template_folder="../../../frontend/templates/admin",
)


@adminOrders_bp.route("/admin/orders")
@role_required("admin")
def admin_orders():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view orders.", "danger")
        return redirect(url_for("login.login"))

    conn = None
    orders = []
    try:
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
            SELECT o.id, o.status, u.firstname, o.created_at
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
            """
        )
        orders = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(f"Error fetching orders: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return render_template("adminOrder.html", orders=orders, user=user)


@adminOrders_bp.route("/admin/orders/update/<int:order_id>/<string:status>")
@role_required("admin")
def update_order_status(order_id, status):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view orders.", "danger")
        return redirect(url_for("login.login"))
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
        conn.commit()
        cursor.close()
        flash(f"Order #{order_id} updated to {status}.", "success")
    except Exception as e:
        flash(f"Error updating order: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminOrders.admin_orders"))
