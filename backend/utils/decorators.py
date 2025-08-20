from functools import wraps
from flask import session, redirect, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_admin") != "admin":
            flash("Admin access only.", "error")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function