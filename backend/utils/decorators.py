from functools import wraps
from flask import session, redirect, flash, url_for

def role_required(role):
    """Decorator to restrict access by role ('admin' or 'client')."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get("is_admin")  # this holds 'admin' or 'client'
            
            if role == "admin" and user_role != "admin":
                flash("Admin access only.", "error")
                return redirect(url_for("home.home"))  # change 'main.home' to your homepage route
            
            if role == "client" and user_role != "client":
                flash("Client access only.", "error")
                return redirect(url_for("home.home"))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
