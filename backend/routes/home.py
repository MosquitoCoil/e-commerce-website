from flask import Blueprint, render_template, request, session
from database.database import get_db_connection

home_bp = Blueprint("home", __name__, template_folder="../../frontend/templates/admin")


@home_bp.route("/")
def home():
    user_id = session.get("user_id")
    view_all = request.args.get("view_all", default=0, type=int)
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
    users = cursor.fetchone()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        "home.html", products=products, user=users, view_all=view_all
    )


@home_bp.route("/product/<int:product_id>")
def productDetail(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM product_variants WHERE product_id = %s", (product_id,)
    )
    variants = cursor.fetchall()

    conn.close()

    if not product:
        return "Product not found", 404

    return render_template("productDetail.html", product=product, variants=variants)
