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
def adminOrders():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "error")
        return redirect(url_for("login.login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

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
    db.close()
    return render_template("adminOrder.html", orders=orders)


@adminOrders_bp.route("/admin/orders/update/<int:order_id>/<string:status>")
@role_required("admin")
def update_order_status(order_id, status):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
    db.commit()
    cursor.close()
    db.close()

    flash(f"Order #{order_id} updated to {status}", "success")
    return redirect(url_for("adminOrders.adminOrders"))
