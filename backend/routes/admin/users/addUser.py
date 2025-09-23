from flask import Blueprint, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from database.database import get_db_connection
from ....utils.decorators import role_required

addUser_bp = Blueprint(
    "addUser", __name__, template_folder="../../../../frontend/templates/admin"
)


@addUser_bp.route("/add-user", methods=["POST"])
@role_required("admin")
def add_user():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin")

    if not firstname or not lastname or not username or not password:
        flash("All fields are required!", "danger")
        return redirect(url_for("adminUserList.adminUserList"))

    hashed_password = generate_password_hash(password)

    conn = None
    try:
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
        flash("User successfully added!", "success")
    except Exception as e:
        flash(f"Error adding user: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminUserList.adminUserList"))
