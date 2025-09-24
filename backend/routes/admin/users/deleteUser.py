from flask import Blueprint, redirect, url_for, flash
from database.database import get_db_connection
from ....utils.decorators import role_required

deleteUser_bp = Blueprint("deleteUser", __name__)


@deleteUser_bp.route("/delete-user/<int:user_id>", methods=["POST"])
@role_required("admin")
def delete_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        flash("User deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "error")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminUserList.admin_user_list"))
