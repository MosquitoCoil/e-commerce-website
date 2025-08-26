from flask import Flask, session
from backend.routes.home import home_bp
from backend.auth.login import login_bp
from backend.auth.register import register_bp
from backend.routes.admin.adminRoute import admin_bp
from backend.routes.admin.userList import userList_bp
from backend.routes.admin.productList import productList_bp
from backend.routes.admin.users.addUser import addUser_bp
from backend.routes.admin.users.editUser import editUser_bp
from backend.routes.admin.users.deleteUser import deleteUser_bp
from backend.routes.admin.products.addProduct import addProduct_bp
from backend.routes.admin.products.editProducts import editProduct_bp
from backend.routes.admin.products.deleteProduct import deleteProduct_bp



app = Flask(__name__, template_folder="./frontend/templates")
app.secret_key = "supersecret"

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(userList_bp)
app.register_blueprint(productList_bp)
app.register_blueprint(addUser_bp)
app.register_blueprint(editUser_bp)
app.register_blueprint(deleteUser_bp)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB
app.register_blueprint(addProduct_bp)
app.register_blueprint(editProduct_bp)
app.register_blueprint(deleteProduct_bp)



def inject_user():
    """Make 'user' available in all templates."""
    user = None
    if "username" in session:
        user = {
            "username": session.get("username"),
            "firstname": session.get("firstname"),
            "is_admin": session.get("is_admin"),
        }
    return dict(user=user)


app.context_processor(inject_user)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
