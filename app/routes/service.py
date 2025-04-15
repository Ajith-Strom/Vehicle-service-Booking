from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.service import Service
from app.models.appointment import Appointment
from app.models.vehicle import Vehicle
from app import db
from datetime import datetime, timedelta

bp = Blueprint('service', __name__, url_prefix='/services')

@bp.route('/')
def list_services():
    services = Service.query.all()
    return render_template('service/list.html', services=services)

@bp.route('/book/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book_service(service_id):
    service = Service.query.get_or_404(service_id)
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    
    if not vehicles:
        flash('Please add a vehicle before booking a service')
        return redirect(url_for('vehicle.add_vehicle'))
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        appointment_date = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d').date()
        appointment_time = datetime.strptime(request.form.get('appointment_time'), '%H:%M').time()
        
        # Check if the time slot is available
        existing_appointment = Appointment.query.filter_by(
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='confirmed'
        ).first()
        
        if existing_appointment:
            flash('This time slot is already booked. Please choose another time.')
            return redirect(url_for('service.book_service', service_id=service_id))
        
        appointment = Appointment(
            user_id=current_user.id,
            vehicle_id=vehicle_id,
            service_id=service_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='pending'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Service appointment booked successfully!')
        return redirect(url_for('user.dashboard'))
    
    return render_template('service/book.html', service=service, vehicles=vehicles)

@bp.route('/appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    return render_template('service/appointments.html', appointments=appointments)

@bp.route('/appointments/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    
    if appointment.user_id != current_user.id:
        flash('You do not have permission to cancel this appointment')
        return redirect(url_for('service.my_appointments'))
    
    appointment.status = 'cancelled'
    db.session.commit()
    
    flash('Appointment cancelled successfully!')
    return redirect(url_for('service.my_appointments')) 