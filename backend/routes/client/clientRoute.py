from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required
from database.database import get_db_connection

client_bp = Blueprint(
    "client", __name__, template_folder="../../../frontend/templates/client"
)


@client_bp.route("/client/dashboard")
@role_required("user")
def client():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to access the dashboard.", "error")
        return redirect(url_for("login.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, firstname, lastname, username, address, is_admin, created_at
        FROM users
        WHERE id = %s
        """,
        (user_id,),
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("clientDashboard.html", user=user)
