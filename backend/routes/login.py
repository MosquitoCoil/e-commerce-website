from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from werkzeug.security import check_password_hash
from database.database import get_db_connection
from datetime import datetime

login_bp = Blueprint("login", __name__, template_folder="../frontend/templates")


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * from users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user["role"] == 1:
            return redirect('/admin')
        else:
            return redirect('/user')
    else:
        flash('Access denied. Incorrect username or password.', "error")

    return redirect(url_for("home.home") + "?login=1")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))