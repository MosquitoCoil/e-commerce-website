from flask import Blueprint, render_template, flash, redirect, url_for, session
from ...utils.decorators import role_required


admin_bp = Blueprint(
    "admin", __name__, template_folder="../../../frontend/templates/admin"
)


@admin_bp.route("/admin/dashboard")
@role_required("admin")
def admin():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to checkout.", "error")
        return redirect(url_for("login.login"))

    return render_template("adminDashboard.html")
