from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.appointment import Appointment

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    
    return render_template('user/dashboard.html', appointments=appointments) 