from flask import render_template, request, redirect, url_for, session, flash, Blueprint

login_bp = Blueprint("login", __name__, template_folder="../frontend/templates")

users = {
    "jaymar": "12345",
    "admin": "admin123"
}

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = {"username": username}
            flash("Login successful!", "success")
            return redirect(url_for("login.home"))  # ✅ fixed
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login.login"))

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))

@login_bp.route("/")
def home():
    return render_template("home.html")