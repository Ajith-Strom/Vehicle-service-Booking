from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.vehicle import Vehicle
from app import db
from datetime import datetime

bp = Blueprint('vehicle', __name__, url_prefix='/vehicles')

@bp.route('/')
@login_required
def list_vehicles():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('vehicle/list.html', vehicles=vehicles)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        year = int(request.form.get('year'))
        license_plate = request.form.get('license_plate')
        
        if Vehicle.query.filter_by(license_plate=license_plate).first():
            flash('A vehicle with this license plate already exists')
            return redirect(url_for('vehicle.add_vehicle'))
        
        vehicle = Vehicle(
            make=make,
            model=model,
            year=year,
            license_plate=license_plate,
            user_id=current_user.id
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('vehicle.list_vehicles'))
    
    return render_template('vehicle/add.html', now=datetime.now())

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    
    if vehicle.user_id != current_user.id:
        flash('You do not have permission to edit this vehicle.', 'error')
        return redirect(url_for('vehicle.list_vehicles'))
    
    if request.method == 'POST':
        vehicle.make = request.form.get('make')
        vehicle.model = request.form.get('model')
        vehicle.year = int(request.form.get('year'))
        vehicle.license_plate = request.form.get('license_plate')
        
        db.session.commit()
        flash('Vehicle updated successfully!', 'success')
        return redirect(url_for('vehicle.list_vehicles'))
    
    return render_template('vehicle/edit.html', vehicle=vehicle, now=datetime.now())

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    
    if vehicle.user_id != current_user.id:
        flash('You do not have permission to delete this vehicle.', 'error')
        return redirect(url_for('vehicle.list_vehicles'))
    
    db.session.delete(vehicle)
    db.session.commit()
    
    flash('Vehicle deleted successfully!', 'success')
    return redirect(url_for('vehicle.list_vehicles')) 