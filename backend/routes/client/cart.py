from flask import Blueprint, session, render_template
from ...utils.decorators import role_required
from database.database import get_db_connection

cart_bp = Blueprint(
    "cart", __name__, template_folder="../../../frontend/templates/client"
)


@cart_bp.route("/cart")
@role_required("user")
def cart():
    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT c.id, p.name, p.price, p.image, c.quantity, (p.price * c.quantity) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
        """,
        (user_id,),
    )

    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("clientCart.html", items=items)
