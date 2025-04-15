from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.service import Service
from app.models.appointment import Appointment
from app import db
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    return render_template('admin/dashboard.html', appointments=appointments)

@bp.route('/appointments')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    return render_template('admin/appointments.html', appointments=appointments)

@bp.route('/appointments/<int:id>/update', methods=['POST'])
@login_required
@admin_required
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status not in ['pending', 'confirmed', 'cancelled', 'completed']:
        flash('Invalid status')
        return redirect(url_for('admin.appointments'))
    
    appointment.status = new_status
    db.session.commit()
    
    flash(f'Appointment status updated to {new_status}')
    return redirect(url_for('admin.appointments'))

@bp.route('/services')
@login_required
@admin_required
def list_services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@bp.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        duration = int(request.form.get('duration'))
        price = float(request.form.get('price'))
        
        service = Service(
            name=name,
            description=description,
            duration=duration,
            price=price
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully!')
        return redirect(url_for('admin.list_services'))
    
    return render_template('admin/add_service.html')

@bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.description = request.form.get('description')
        service.duration = int(request.form.get('duration'))
        service.price = float(request.form.get('price'))
        
        db.session.commit()
        
        flash('Service updated successfully!')
        return redirect(url_for('admin.list_services'))
    
    return render_template('admin/edit_service.html', service=service)

@bp.route('/services/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    
    # Check if service has any appointments
    if service.appointments:
        flash('Cannot delete service with existing appointments')
        return redirect(url_for('admin.list_services'))
    
    db.session.delete(service)
    db.session.commit()
    
    flash('Service deleted successfully!')
    return redirect(url_for('admin.list_services')) 