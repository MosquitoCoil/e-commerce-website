from flask import Blueprint, redirect, url_for, flash
from ....utils.decorators import admin_required
from database.database import get_db_connection

deleteProduct_bp = Blueprint('deleteProduct', __name__)

@deleteProduct_bp.route('/delete-product/<int:product_id>', methods=['POST'])
@admin_required
def deleteProduct(product_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        cursor.close()
        flash(f"Product deleted successfully.","success")
    except Exception as e:
        flash(f"Error deleting Product: {str(e)}", "error")
    return redirect(url_for("productList.productList"))