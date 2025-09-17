from flask import Blueprint, render_template, flash, session, redirect, url_for
from database.database import get_db_connection
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

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Daily sales (with total products sold)
    cursor.execute(
        """
        SELECT DATE(received_at) AS sale_date,
               SUM(total) AS total_sales,
               SUM(quantity) AS total_products_sold
        FROM purchase_history
        GROUP BY DATE(received_at)
        ORDER BY sale_date ASC
        """
    )
    daily_sales = cursor.fetchall()

    # Monthly sales (with total products sold)
    cursor.execute(
        """
        SELECT DATE_FORMAT(received_at, '%Y-%m') AS sale_month,
               SUM(total) AS total_sales,
               SUM(quantity) AS total_products_sold
        FROM purchase_history
        GROUP BY DATE_FORMAT(received_at, '%Y-%m')
        ORDER BY sale_month ASC
        """
    )
    monthly_sales = cursor.fetchall()

    cursor.close()
    db.close()

    # Chart data
    daily_sales_labels = [
        (
            row["sale_date"].strftime("%Y-%m-%d")
            if hasattr(row["sale_date"], "strftime")
            else str(row["sale_date"])
        )
        for row in daily_sales
    ]
    daily_sales_values = [float(row["total_sales"] or 0) for row in daily_sales]

    monthly_sales_labels = [str(row["sale_month"]) for row in monthly_sales]
    monthly_sales_values = [float(row["total_sales"] or 0) for row in monthly_sales]

    return render_template(
        "adminDashboard.html",
        daily_sales=daily_sales,
        monthly_sales=monthly_sales,
        daily_sales_labels=daily_sales_labels,
        daily_sales_values=daily_sales_values,
        monthly_sales_labels=monthly_sales_labels,
        monthly_sales_values=monthly_sales_values,
    )
