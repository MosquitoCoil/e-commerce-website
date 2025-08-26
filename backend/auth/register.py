from flask import Blueprint, render_template, request, redirect, flash, url_for
from database.database import get_db_connection
from werkzeug.security import generate_password_hash
import mysql.connector

register_bp = Blueprint(
    "register", __name__, template_folder="../../Frontend/templates"
)


# register
@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname: str = request.form["firstname"]
        lastname: str = request.form["lastname"]
        username: str = request.form["username"]
        password = request.form["password"]
        is_admin = request.form["is_admin"]

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (`firstname`, `lastname`, `username`, `password`, `is_admin`) VALUES (%s, %s, %s, %s, %s)",
                (firstname, lastname, username, hashed_pw, is_admin),
            )
            conn.commit()
            flash("Registered Successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()
        return redirect(url_for("products.home"))
    return render_template("register.html")
