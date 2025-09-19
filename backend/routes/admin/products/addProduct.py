from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
import os
from ....utils.decorators import role_required
from werkzeug.utils import secure_filename
from database.database import get_db_connection

addProduct_bp = Blueprint(
    "addProduct", __name__, template_folder="../../../../frontend/templates/admin"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@addProduct_bp.route("/add-product", methods=["GET", "POST"])
@role_required("admin")
def addProduct():
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = int(request.form["price"])
        stock = int(request.form["stock"])

        file = request.files["image"]
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))

        cursor.execute(
            "INSERT INTO products (name, description, price, stock, image) VALUES (%s, %s, %s, %s, %s)",
            (name, description, price, stock, filename),
        )
        conn.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("adminProductlist.adminProductlist"))

    # If GET request → just redirect back to users list
    return redirect(url_for("adminProductlist.adminProductlist"))
