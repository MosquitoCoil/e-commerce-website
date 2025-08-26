from flask import Blueprint, request, flash, redirect, url_for, render_template
from ....utils.decorators import admin_required
from database.database import get_db_connection
from werkzeug.security import generate_password_hash

addUser_bp = Blueprint(
    "addUser", __name__, template_folder="../../../../frontend/templates/admin"
)

@addUser_bp.route("/add-user", methods=["GET", "POST"])
@admin_required
def addUser():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        is_admin = request.form.get("is_admin")

        if not firstname or not lastname or not username or not password:
            flash(f"All fields are required!", "danger")
            return redirect(url_for("userList.userList"))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (firstname, lastname, username, password, is_admin) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (firstname, lastname, username, hashed_password, is_admin),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f"User successfully added!", "success")
        return redirect(url_for("userList.userList"))

    # If GET request → just redirect back to users list
    return redirect(url_for("userList.userList"))