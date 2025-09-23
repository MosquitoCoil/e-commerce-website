from flask import Blueprint, request, redirect, flash, url_for
from database.database import get_db_connection
from werkzeug.security import generate_password_hash
import mysql.connector

register_bp = Blueprint(
    "register", __name__, template_folder="../../Frontend/templates"
)


@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        address = request.form.get("address")
        username = request.form.get("username")
        password = request.form.get("password")
        is_admin = request.form.get("is_admin")

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
            flash("Registered successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Registration error: {err}", "error")
        finally:
            conn.close()

        return redirect(url_for("home.home"))

    return redirect(url_for("home.home"))
