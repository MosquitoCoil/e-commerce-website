from flask import Blueprint, redirect, url_for, flash
from ....utils.decorators import role_required
from database.database import get_db_connection

deleteProduct_bp = Blueprint("deleteProduct", __name__)


@deleteProduct_bp.route("/delete-product/<int:product_id>", methods=["POST"])
@role_required("admin")
def delete_product(product_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))

        conn.commit()
        cursor.close()
        flash("Product deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting product: {e}", "error")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminProductlist.admin_product_list"))
