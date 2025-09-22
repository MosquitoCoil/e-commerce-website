# 🛍️ E-Commerce Website

<p align="center">
  <img src="static/images/bg/jaymar.png" width="800" alt="E-Commerce Website Banner" />
</p>

An end-to-end full-stack **E-Commerce Website** built with **Flask (Python), MySQL, and modern frontend tools**.  
It allows users to browse products, manage carts, and checkout, while admins can manage products and orders.

---

## 📸 Screenshots

<details>
  <summary>📸 View All Screenshots</summary>
  <p align="center">
    <b>Landing Page</b><br/>
    <img src="screenshots/home header.PNG" width="300" />
    <img src="screenshots/landing page.png" width="300" />
    <img src="screenshots/home footer.PNG" width="300" />
    <img src="screenshots/login form modal.PNG" width="300" />
    <img src="screenshots/registration form modal.PNG" width="300" />
    <img src="screenshots/profile modal.PNG" width="300" />
    <img src="screenshots/edit profile modal.PNG" width="300" />
    <br/><br/>
    <b>Client Pages</b><br/>
    <img src="screenshots/client cart.png" width="300" />
    <img src="screenshots/client checkout.png" width="300" />
    <img src="screenshots/client order.png" width="300" />
    <img src="screenshots/client order details.png" width="300" />
    <br/><br/>
    <b>Admin Pages</b><br/>
    <img src="screenshots/admin dashboard.png" width="300" />
    <img src="screenshots/admin product.png" width="300" />
    <img src="screenshots/admin add product modal.PNG" width="300" />
    <img src="screenshots/admin edit product modal.PNG" width="300" />
    <img src="screenshots/admin delete product modal.PNG" width="300" />
    <img src="screenshots/admin order.png" width="300" />
    <img src="screenshots/admin user.png" width="300" />
    <img src="screenshots/admin add user modal.PNG" width="300" />
    <img src="screenshots/admin edit user modal.PNG" width="300" />
    <img src="screenshots/admin delete user modal.PNG" width="300" />
    <img src="screenshots/admin report.png" width="300" />
  </p>
</details>

---

## ✨ Features

- 🔑 User Authentication (Register/Login/Logout)
- 🛒 Product Listings
- 📦 Shopping Cart & Checkout
- 💳 Order Management (Client & Admin)
- 📊 Admin Dashboard for Products & Sales
- 📱 Responsive Design (Mobile-Friendly)

---

## 🛠 Tech Stack

**Frontend:** HTML, CSS (Bootstrap), JavaScript  
**Backend:** Python Flask (Blueprints)  
**Database:** MySQL (via phpMyAdmin)  
**Tools:** Jinja2, Flask-Login, REST API, Git  

---

## ⚙️ Installation & Setup

1. **Clone the repo**
```bash
   git clone https://github.com/your-username/e-commerce-website.git
   cd e-commerce-website
```
2. **Set up virtual environment & install dependencies**
```bash
  python -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
```
3. **Configure database**
- Create a MySQL database
- Import e-commerece-web.sql
- Update connection settings in backend/database/database.py
4. **Run the app**
```bash
flask run
Your app will be live at: http://127.0.0.1:5000/
```
5. **Folder Structure**
```php  
ecommerce-website/
│── backend/
│   ├── auth/ (login, register)
│   ├── routes/ (email, home, profile)
│       ├── admin/ (adminProductList, adminReports, adminRoute, adminTransaction, adminUserList)
│           ├── products/ (addProduct, deleteProduct, editProduct)
│           ├── users/ (addUser, deleteUser, editUser)
│       ├── client (addToCart, checkout, clientCart, clientOrders, clientRoute, deleteCart, editCart)
│   ├── utils/ (decorators)
│   ├── database/ (database)
│── frontend/
│   ├── templates/ (base, home, productDetail)
│       ├── admin/ (adminPages)
│           ├── partials/ (adminHeader, adminFooter)
│       ├── client/ (clientPages)
│       ├── partials/ (header, footer)
│── static/ (CSS, JS, images)
│── screenshots/ (project screenshots for README)
│── requirements.txt
│── app.py (register blueprints)
```
## 📜 License
- Distributed under the MIT License. See LICENSE for more information.
## 👤 Author
- Jaymar
- 📧 Email: jaymarroco.j@gmail.com
- 🌐 Portfolio: [jaymarportfolio.netlify.app](https://jaymarportfolio.netlify.app/)
## 
