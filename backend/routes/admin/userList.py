from flask import Blueprint, render_template
from ...utils.decorators import role_required
from database.database import get_db_connection


userList_bp = Blueprint(
    "userList", __name__, template_folder="../../../frontend/templates/admin"
)

@userList_bp.route("/users")
@role_required('admin')
def userList():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, firstname, lastname, username, is_admin, created_at FROM users"
    )
    users = cursor.fetchall()
    conn.close()

    return render_template("userList.html", users=users)