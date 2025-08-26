from flask import Blueprint, request, redirect, flash, url_for, current_app
from database.database import get_db_connection
from ...utils.decorators import admin_required
import os
from werkzeug.utils import secure_filename

editProduct_bp = Blueprint(
    "editProduct", __name__, template_folder="../../../frontend/templates/admin"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@editProduct_bp.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@admin_required
def editProduct(product_id):
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    stock = request.form.get("stock")

    # check for uploaded file
    image_file = request.files.get("image")
    image_filename = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
        image_file.save(upload_path)
        image_filename = filename

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if image_filename:
        # update including new image
        cursor.execute(
            """UPDATE products 
               SET name=%s, description=%s, price=%s, stock=%s, image=%s 
               WHERE id=%s""",
            (name, description, price, stock, image_filename, product_id),
        )
    else:
        # update without changing image
        cursor.execute(
            """UPDATE products 
               SET name=%s, description=%s, price=%s, stock=%s 
               WHERE id=%s""",
            (name, description, price, stock, product_id),
        )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Product updated successfully.", "success")
    return redirect(url_for("addProducts.addProducts"))
