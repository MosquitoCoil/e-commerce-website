from functools import wraps
from flask import session, redirect, flash, url_for


def role_required(role):
    """Restrict access by role: 'admin' or 'user'."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in first.", "error")
                return redirect(url_for("login.login"))

            user_role = session.get("is_admin")

            if role == "admin" and user_role != "admin":
                flash("Admin access only.", "error")
                return redirect(url_for("home.home"))

            if role == "user" and user_role != "user":
                flash("Client access only.", "error")
                return redirect(url_for("home.home"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
