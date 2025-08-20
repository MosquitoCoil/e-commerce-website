from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...utils.decorators import admin_required
from database.database import get_db_connection
from werkzeug.security import generate_password_hash

addUser_bp = Blueprint(
    "addUser", __name__, template_folder="../../../frontend/templates/admin"
)

@addUser_bp.route("/add-user", methods=["GET", "POST"])
@admin_required
def addUser():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]
    is_admin = int(request.form.get("is_admin", 0))

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

    flash("User successfully added!", "success")
    return redirect(url_for("userList_bp.userList"))
