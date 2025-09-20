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
    size = request.form.get("size")

    if not size:
        flash("Please select a size!", "warning")
        return redirect(url_for("home.productDetail", product_id=product_id))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔎 Check if enough stock exists for this variant
    cursor.execute(
        "SELECT stock FROM product_variants WHERE product_id = %s AND size = %s",
        (product_id, size),
    )
    variant = cursor.fetchone()

    if not variant or variant["stock"] < quantity:
        flash("Not enough stock for this size!", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("shop.product_detail", product_id=product_id))

    # 🔒 Deduct stock safely (prevent overselling if multiple users add at once)
    cursor.execute(
        """
        UPDATE product_variants
        SET stock = stock - %s
        WHERE product_id = %s AND size = %s AND stock >= %s
        """,
        (quantity, product_id, size, quantity),
    )

    if cursor.rowcount == 0:  # nothing updated → stock ran out
        flash("Stock ran out for this size!", "danger")
        conn.rollback()
        cursor.close()
        conn.close()
        return redirect(url_for("shop.product_detail", product_id=product_id))

    # 🛒 Check if already in cart (same product + same size)
    cursor.execute(
        "SELECT * FROM cart WHERE user_id=%s AND product_id=%s AND size=%s",
        (user_id, product_id, size),
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "UPDATE cart SET quantity = quantity + %s WHERE id=%s",
            (quantity, existing["id"]),
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, size, quantity) VALUES (%s, %s, %s, %s)",
            (user_id, product_id, size, quantity),
        )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Item added to cart!", "success")
    return redirect(url_for("home.home"))


# 🛒 Cart Page
@addToCart_bp.route("/clientCart")
@role_required("user")
def cart_page():
    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT c.id, p.image, p.name, p.price, c.size, c.quantity,
               (p.price * c.quantity) AS total
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
