from flask import Blueprint, render_template
from ...utils.decorators import role_required
from database.database import get_db_connection

authHome_bp = Blueprint(
    "authHome", __name__, template_folder="../../../frontend/templates/client"
)


@authHome_bp.route("/client/home")
@role_required("user")
def authHome():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clientHome.html", products=products)
