from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection


adminUserList_bp = Blueprint(
    "adminUserList", __name__, template_folder="../../../frontend/templates/admin"
)


@adminUserList_bp.route("/admin/users")
@role_required("admin")
def userList():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, firstname, lastname, username, is_admin, created_at FROM users"
    )
    users = cursor.fetchall()
    conn.close()

    return render_template("adminUserList.html", users=users)
