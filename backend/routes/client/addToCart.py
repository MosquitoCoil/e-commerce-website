from flask import Blueprint, redirect, url_for, flash, request, session, render_template
from ...utils.decorators import role_required
from database.database import get_db_connection

addToCart_bp = Blueprint(
    "addToCart", __name__, template_folder="../../../frontend/templates/client"
)


@addToCart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
@role_required("user")
def addToCart(product_id):

    user_id = session["user_id"]
    quantity = int(request.form.get("quantity", 1))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if already in cart
    cursor.execute(
        "SELECT * FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "UPDATE cart SET quantity = quantity + %s WHERE user_id=%s AND product_id=%s",
            (quantity, user_id, product_id),
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
            (user_id, product_id, quantity),
        )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Item added to cart!", "success")
    return redirect(url_for("authHome.authHome"))


# View cart page
@addToCart_bp.route("/cart")
@role_required("user")
def cart_page():

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT c.id, p.image, p.name, p.price, c.quantity, (p.price * c.quantity) AS total
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
