from flask import Flask, render_template, Blueprint, session
from backend.routes.home import home_bp
from backend.routes.login import login_bp
from backend.routes.register import register_bp

app = Flask(__name__, template_folder='./frontend/templates')
app.secret_key = "supersecret"

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)


@app.context_processor
def inject_user():
    return {"user": session.get("user")}

@app.route("/")
def home():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)