from flask import Blueprint, render_template
from ...utils.decorators import admin_required
from database.database import get_db_connection

productList_bp = Blueprint('productList', __name__, template_folder='../../../frontend/templates/admin')

@productList_bp.route("/products")
@admin_required
def productList():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM products"
    )
    products = cursor.fetchall()
    conn.close()

    return render_template("productList.html", products=products)