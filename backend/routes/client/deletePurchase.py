from flask import Blueprint, redirect, url_for, flash, session
from ...utils.decorators import role_required
from database.database import get_db_connection

deletePurchase_bp = Blueprint(
    "deletePurchase", __name__, template_folder="../../../frontend/templates/client"
)


@deletePurchase_bp.route("/clientOrder/delete/<int:product_id>", methods=["POST"])
@role_required("user")
def deletePurchase(product_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to delete purchase.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "DELETE FROM purchase_history WHERE id=%s AND user_id=%s", (product_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Item removed from purchase history.", "success")
    return redirect(url_for("clientOrders.clientOrders"))
