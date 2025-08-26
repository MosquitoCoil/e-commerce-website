from flask import Blueprint, redirect, request, flash, url_for
from database.database import get_db_connection
from ....utils.decorators import admin_required
from werkzeug.security import generate_password_hash

editUser_bp = Blueprint(
    "editUser", __name__, template_folder="../../../../frontend/templates/admin"
)

# edit users
@editUser_bp.route("/edit-user/<int:user_id>", methods=["POST"])
@admin_required
def editUser(user_id):
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get("password")
    is_admin = request.form.get('is_admin')

    if not firstname or not lastname or not username:
        flash(f"Firstname, Lastname, and Username are required.", "danger")
        return redirect(url_for("userList.userList"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if password:  # update password only if new one entered
        new_password = generate_password_hash(password)
        cursor.execute(
            """UPDATE users 
               SET firstname=%s, lastname=%s, username=%s, password=%s, is_admin=%s 
               WHERE id=%s""",
            (firstname, lastname, username, new_password, is_admin, user_id),
        )
    else:  # don’t overwrite password if empty
        cursor.execute(
            """UPDATE users 
               SET firstname=%s, lastname=%s, username=%s, is_admin=%s 
               WHERE id=%s""",
            (firstname, lastname, username, is_admin, user_id),
        )

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"User updated successfully.", "success")
    return redirect(url_for("userList.userList"))