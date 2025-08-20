from flask import Blueprint, render_template
from ...utils.decorators import admin_required



admin_bp = Blueprint('admin',__name__,template_folder='../../../frontend/templates/admin')



@admin_bp.route('/admin/dashboard')
@admin_required
def admin():
    return render_template('adminDashboard.html')