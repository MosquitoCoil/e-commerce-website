from flask import Blueprint, render_template, request
from database.database import get_db_connection

home_bp = Blueprint("home", __name__, template_folder="../../frontend/templates/admin")


@home_bp.route("/")
def home():
    view_all = request.args.get("view_all", default=0, type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", products=products, view_all=view_all)


@home_bp.route("/product/<int:product_id>")
def productDetail(product_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()

    if not product:
        return "Product not found", 404

    return render_template("productDetail.html", product=product)
