from flask import Blueprint, session, request, jsonify
from database.database import get_db_connection
from werkzeug.security import generate_password_hash
import re

profile_bp = Blueprint(
    "profile", __name__, template_folder="../../../frontend/templates"
)


@profile_bp.route("/client/edit-profile", methods=["POST"])
def edit_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to edit your profile."}), 401

    firstname = request.form.get("firstname", "").strip()
    lastname = request.form.get("lastname", "").strip()
    address = request.form.get("address", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    is_admin = request.form.get("is_admin", "user").strip()

    if not firstname or not username:
        return jsonify({"error": "Firstname and Username are required."}), 400

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return (
            jsonify(
                {
                    "error": "Username can only contain alphanumeric characters and underscores."
                }
            ),
            400,
        )

    if address and len(address) > 255:
        return jsonify({"error": "Address must be less than 255 characters."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if password:
            hashed_password = generate_password_hash(password)
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
                    hashed_password,
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
        conn.close()

        return jsonify({"success": "Profile updated successfully."})

    except Exception as e:
        print(f"Error updating profile: {e}")
        return (
            jsonify(
                {
                    "error": "An error occurred while updating your profile. Please try again later."
                }
            ),
            500,
        )
