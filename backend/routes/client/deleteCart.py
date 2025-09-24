from flask import Blueprint, redirect, url_for, flash, session
from ...utils.decorators import role_required
from database.database import get_db_connection

deleteCart_bp = Blueprint(
    "deleteCart", __name__, template_folder="../../../frontend/templates/client"
)


@deleteCart_bp.route("/clientCart/delete/<int:cart_id>", methods=["POST"])
@role_required("user")
def deleteCart(cart_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to delete cart.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM cart WHERE id=%s AND user_id=%s", (cart_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Item removed from cart.", "success")
    return redirect(url_for("clientCart.cart_page"))
