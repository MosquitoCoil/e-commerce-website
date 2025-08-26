from flask import Blueprint, render_template
from werkzeug.utils import secure_filename
from database.database import get_db_connection

home_bp = Blueprint(
    "products", __name__, template_folder="../../frontend/templates/admin"
)


@home_bp.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", products=products)
