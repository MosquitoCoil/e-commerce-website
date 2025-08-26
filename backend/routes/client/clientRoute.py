from flask import Blueprint, render_template
from ...utils.decorators import role_required

client_bp = Blueprint('client',__name__, template_folder='../../../frontend/templates/client')

@client_bp.route('/client/dashboard')
@role_required('user')
def client():
    return render_template('clientDashboard.html')