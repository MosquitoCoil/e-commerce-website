from flask import Flask, session, render_template
from backend.routes.home import home_bp
from backend.auth.login import login_bp
from backend.auth.register import register_bp

# Admin Side
from backend.routes.admin.adminRoute import admin_bp
from backend.routes.admin.adminUserList import adminUserList_bp
from backend.routes.admin.adminProductList import adminProductlist_bp
from backend.routes.admin.users.addUser import addUser_bp
from backend.routes.admin.users.editUser import editUser_bp
from backend.routes.admin.users.deleteUser import deleteUser_bp
from backend.routes.admin.products.addProduct import addProduct_bp
from backend.routes.admin.products.editProducts import editProduct_bp
from backend.routes.admin.products.deleteProduct import deleteProduct_bp
from backend.routes.admin.adminTransaction import adminOrders_bp
from backend.routes.admin.adminReports import adminReports_bp


# Client Side
from backend.routes.client.clientRoute import client_bp
from backend.routes.client.addToCart import addToCart_bp
from backend.routes.client.clientCart import clientCart_bp
from backend.routes.client.editCart import editCart_bp
from backend.routes.client.deleteCart import deleteCart_bp
from backend.routes.client.checkout import checkout_bp
from backend.routes.client.clientOrders import clientOrders_bp

# Profile
from backend.routes.profile import profile_bp


app = Flask(__name__, template_folder="./frontend/templates")
app.secret_key = "supersecret"

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
# Admin Side
app.register_blueprint(admin_bp)
app.register_blueprint(adminUserList_bp)
app.register_blueprint(adminProductlist_bp)
app.register_blueprint(addUser_bp)
app.register_blueprint(editUser_bp)
app.register_blueprint(deleteUser_bp)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB
app.register_blueprint(addProduct_bp)
app.register_blueprint(editProduct_bp)
app.register_blueprint(deleteProduct_bp)
app.register_blueprint(adminOrders_bp)
app.register_blueprint(adminReports_bp)

# Client Side
app.register_blueprint(client_bp)
app.register_blueprint(addToCart_bp)
app.register_blueprint(clientCart_bp)
app.register_blueprint(editCart_bp)
app.register_blueprint(deleteCart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(clientOrders_bp)

# Profile
app.register_blueprint(profile_bp)


@app.route("/test")
def test():
    products = [
        {
            "id": 1,
            "name": "Oversized Hoodie",
            "price": 1800,
            "stock": 5,
            "image": "hoodie.jpg",
        },
        {
            "id": 2,
            "name": "Cargo Pants",
            "price": 1600,
            "stock": 0,
            "image": "pants.jpg",
        },
    ]
    lookbook_images = ["look1.jpg", "look2.jpg", "look3.jpg", "look4.jpg"]
    return render_template(
        "test.html", products=products, lookbook_images=lookbook_images
    )


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
