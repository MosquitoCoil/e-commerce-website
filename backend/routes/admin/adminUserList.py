from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

adminUserList_bp = Blueprint(
    "adminUserList", __name__, template_folder="../../../frontend/templates/admin"
)


@adminUserList_bp.route("/admin/users")
@role_required("admin")
def admin_user_list():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view users.", "danger")
        return redirect(url_for("login.login"))

    conn = None
    users = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, username, firstname, lastname, address, is_admin, created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )
        user = cursor.fetchone()
        cursor.execute(
            "SELECT id, firstname, lastname, address, username, is_admin, created_at FROM users"
        )
        users = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(f"Error fetching users: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return render_template("adminUserList.html", users=users, user=user)
