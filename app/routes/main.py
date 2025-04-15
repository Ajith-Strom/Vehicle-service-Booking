from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.appointment import Appointment
from app.models.vehicle import Vehicle

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    user_appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
    user_vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', appointments=user_appointments, vehicles=user_vehicles) 