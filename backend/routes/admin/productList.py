from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

productList_bp = Blueprint(
    "productList", __name__, template_folder="../../../frontend/templates/admin"
)


@productList_bp.route("/admin/products")
@role_required("admin")
def productList():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("productList.html", products=products)
