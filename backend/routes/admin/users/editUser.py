from flask import Blueprint, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash
from database.database import get_db_connection
from ....utils.decorators import role_required

editUser_bp = Blueprint(
    "editUser", __name__, template_folder="../../../../frontend/templates/admin"
)


@editUser_bp.route("/edit-user/<int:user_id>", methods=["POST"])
@role_required("admin")
def edit_user(user_id):
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    address = request.form.get("address")
    username = request.form.get("username")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin")

    if not firstname or not lastname or not username:
        flash("Firstname, Lastname, and Username are required.", "danger")
        return redirect(url_for("adminUserList.admin_user_list"))

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if password:
            new_password = generate_password_hash(password)
            cursor.execute(
                """
                UPDATE users 
                SET firstname=%s, lastname=%s, address=%s, username=%s, password=%s, is_admin=%s 
                WHERE id=%s
                """,
                (
                    firstname,
                    lastname,
                    address,
                    username,
                    new_password,
                    is_admin,
                    user_id,
                ),
            )
        else:
            cursor.execute(
                """
                UPDATE users 
                SET firstname=%s, lastname=%s, address=%s, username=%s, is_admin=%s 
                WHERE id=%s
                """,
                (firstname, lastname, address, username, is_admin, user_id),
            )

        conn.commit()
        cursor.close()
        flash("User updated successfully.", "success")
    except Exception as e:
        flash(f"Error updating user: {e}", "danger")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("adminUserList.admin_user_list"))
