from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

adminProductlist_bp = Blueprint(
    "adminProductlist", __name__, template_folder="../../../frontend/templates/admin"
)


@adminProductlist_bp.route("/admin/products")
@role_required("admin")
def admin_product_list():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view products.", "danger")
        return redirect(url_for("login.login"))

    conn = None
    products = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        for p in products:
            cursor.execute(
                "SELECT * FROM product_variants WHERE product_id = %s", (p["id"],)
            )
            p["variants"] = cursor.fetchall()

        cursor.close()
    except Exception as e:
        flash(f"Error fetching products: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return render_template("adminProductList.html", products=products)
