from flask import Blueprint, request, redirect, url_for, flash, current_app
import os
from werkzeug.utils import secure_filename
from database.database import get_db_connection
from ....utils.decorators import role_required

addProduct_bp = Blueprint(
    "addProduct", __name__, template_folder="../../../../frontend/templates/admin"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@addProduct_bp.route("/add-product", methods=["GET", "POST"])
@role_required("admin")
def add_product():
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price", 0))

        file = request.files.get("image")
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))

        cursor.execute(
            "INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)",
            (name, description, price, filename),
        )
        product_id = cursor.lastrowid

        sizes = ["S", "M", "L", "XL", "XXL"]
        for size in sizes:
            stock = int(request.form.get(f"stock_{size}", 0))
            cursor.execute(
                "INSERT INTO product_variants (product_id, size, stock) VALUES (%s, %s, %s)",
                (product_id, size, stock),
            )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Product added successfully with size variants!", "success")
        return redirect(url_for("adminProductlist.admin_product_list"))

    return redirect(url_for("adminProductlist.admin_product_list"))


@addProduct_bp.route("/admin/update-stock/<int:variant_id>", methods=["POST"])
@role_required("admin")
def update_stock(variant_id):
    new_stock = request.form.get("stock")

    if not new_stock or not new_stock.isdigit():
        flash("Invalid stock value!", "danger")
        return redirect(url_for("adminProductlist.admin_product_list"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE product_variants SET stock = %s WHERE id = %s", (new_stock, variant_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Stock updated successfully!", "success")
    return redirect(url_for("adminProductlist.admin_product_list"))
