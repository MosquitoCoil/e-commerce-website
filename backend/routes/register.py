from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database.database import get_db_connection

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password_hash = request.form["password"]
        role = ["role"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # check if email or username already exists
        cursor.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or Email already exists!", "danger")
            return redirect(url_for("register.register"))

        # insert new user with hashed password
        hashed_password = generate_password_hash(password_hash)
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                       (username, email, hashed_password, role == 1))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")