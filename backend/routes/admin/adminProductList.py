from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

adminProductlist_bp = Blueprint(
    "adminProductlist", __name__, template_folder="../../../frontend/templates/admin"
)


@adminProductlist_bp.route("/admin/products")
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

    return render_template("adminProductList.html", products=products)
