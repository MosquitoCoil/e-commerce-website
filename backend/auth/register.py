from flask import Blueprint, request, redirect, flash, url_for
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
        address = request.form["address"]
        username: str = request.form["username"]
        password = request.form["password"]
        is_admin = request.form["is_admin"]

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (username, firstname, lastname, password, is_admin, address)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (username, firstname, lastname, hashed_pw, is_admin, address),
            )
            conn.commit()
            flash("Registered Successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()
        return redirect(url_for("home.home"))
    return redirect(url_for("home.home"))
