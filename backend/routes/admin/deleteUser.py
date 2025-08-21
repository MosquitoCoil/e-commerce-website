from flask import Blueprint, redirect, url_for, flash
from ...utils.decorators import admin_required
from database.database import get_db_connection

deleteUser_bp = Blueprint('deleteUser', __name__)

@deleteUser_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def deleteUser(user_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash(f"User deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "error")
    return redirect(url_for("userList.userList"))