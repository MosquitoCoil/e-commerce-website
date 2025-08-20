from flask import Flask
from backend.routes.home import home_bp
from backend.auth.login import login_bp
from backend.auth.register import register_bp
from backend.routes.admin.adminRoute import admin_bp
from backend.routes.admin.userList import userList_bp
from backend.routes.admin.addUser import addUser_bp


app = Flask(__name__, template_folder='./frontend/templates')
app.secret_key = "supersecret"

# Register blueprint for python flask
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(userList_bp)
app.register_blueprint(addUser_bp)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)