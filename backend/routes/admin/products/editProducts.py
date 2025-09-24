from flask import Blueprint, request, redirect, flash, url_for, current_app
import os
from werkzeug.utils import secure_filename
from database.database import get_db_connection
from ....utils.decorators import role_required

editProduct_bp = Blueprint(
    "editProduct", __name__, template_folder="../../../../frontend/templates/admin"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@editProduct_bp.route("/edit-product/<int:product_id>", methods=["POST"])
@role_required("admin")
def edit_product(product_id):
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")

    image_file = request.files.get("image")
    image_filename = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
        image_file.save(upload_path)
        image_filename = filename

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if image_filename:
            cursor.execute(
                """
                UPDATE products 
                SET name=%s, description=%s, price=%s, image=%s 
                WHERE id=%s
                """,
                (name, description, price, image_filename, product_id),
            )
        else:
            cursor.execute(
                """
                UPDATE products 
                SET name=%s, description=%s, price=%s, 
                WHERE id=%s
                """,
                (name, description, price, product_id),
            )

        conn.commit()
        cursor.close()
        flash("Product updated successfully.", "success")
    except Exception as e:
        flash(f"Error updating product: {e}", "error")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminProductlist.admin_product_list"))
