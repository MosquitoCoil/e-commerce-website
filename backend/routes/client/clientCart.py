from flask import Blueprint, session, render_template, redirect, url_for, flash
from ...utils.decorators import role_required
from database.database import get_db_connection

clientCart_bp = Blueprint(
    "clientCart", __name__, template_folder="../../../frontend/templates/client"
)


@clientCart_bp.route("/client/clientCart")
@role_required("user")
def cart_page():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view cart.", "danger")
        return redirect(url_for("login.login"))

    conn = None
    user, items = None, []
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
            SELECT c.id, p.name, p.price, p.image, c.size, c.quantity,
            (p.price * c.quantity) AS total
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            """,
            (user_id,),
        )
        items = cursor.fetchall()

        cursor.close()
    except Exception as e:
        flash(f"Error loading cart: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return render_template("clientCart.html", user=user, items=items)
