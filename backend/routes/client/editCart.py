from flask import Blueprint, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

editCart_bp = Blueprint(
    "editCart", __name__, template_folder="../../../frontend/templates/client"
)


@editCart_bp.route("/cart/update/<int:cart_id>/<action>", methods=["POST"])
@role_required("user")
def editCart(cart_id, action):

    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if action == "add":
        cursor.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id=%s AND user_id=%s",
            (cart_id, user_id),
        )
    elif action == "minus":
        # prevent quantity from going below 1
        cursor.execute(
            "UPDATE cart SET quantity = GREATEST(quantity - 1, 1) WHERE id=%s AND user_id=%s",
            (cart_id, user_id),
        )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("cart.cart"))
