from flask import Blueprint, redirect, url_for, flash, request, session
from ...utils.decorators import role_required
from database.database import get_db_connection

addToCart_bp = Blueprint(
    "addToCart", __name__, template_folder="../../../frontend/templates/client"
)


@addToCart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
@role_required("user")
def add_to_cart(product_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to add to cart.", "danger")
        return redirect(url_for("login.login"))

    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        flash("Invalid quantity.", "danger")
        return redirect(url_for("home.product_detail", product_id=product_id))

    size = request.form.get("size")

    if not size:
        flash("Please select a size.", "danger")
        return redirect(url_for("home.product_detail", product_id=product_id))

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT stock FROM product_variants WHERE product_id = %s AND size = %s",
            (product_id, size),
        )
        variant = cursor.fetchone()

        if not variant or variant["stock"] < quantity:
            flash("Not enough stock for this size.", "danger")
            return redirect(url_for("shop.product_detail", product_id=product_id))

        cursor.execute(
            """
            UPDATE product_variants
            SET stock = stock - %s
            WHERE product_id = %s AND size = %s AND stock >= %s
            """,
            (quantity, product_id, size, quantity),
        )

        if cursor.rowcount == 0:
            flash("Stock ran out for this size.", "danger")
            conn.rollback()
            return redirect(url_for("shop.product_detail", product_id=product_id))

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
        flash("Item added to cart.", "success")

    except Exception as e:
        flash(f"Error adding to cart: {e}", "danger")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect(url_for("home.home"))
