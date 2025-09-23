from flask import Blueprint, redirect, session, request, flash
from werkzeug.security import check_password_hash
from database.database import get_db_connection
from datetime import datetime

login_bp = Blueprint(
    "login", __name__, template_folder="../../Frontend/admin/templates"
)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session.update(
                {
                    "user_id": user["id"],
                    "username": user["username"],
                    "firstname": user["firstname"],
                    "is_admin": user["is_admin"],
                }
            )
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flash(f"Welcome, {user['firstname']}! Logged in at {login_time}", "success")
            return redirect("/")

        flash("Access denied. Incorrect username or password.", "error")
        return redirect("/")

    return redirect("/")


@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect("/")
