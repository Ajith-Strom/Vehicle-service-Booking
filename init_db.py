from app import create_app, db
from app.models.user import User
from app.models.service import Service
from app.models.vehicle import Vehicle
from app.models.appointment import Appointment
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            # Create admin user
            admin = User(
                name='Admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        # Add default services if none exist
        if Service.query.count() == 0:
            services = [
                Service(
                    name='Oil Change',
                    description='Complete oil change service with filter replacement',
                    duration=60,
                    price=1499.00
                ),
                Service(
                    name='Brake Service',
                    description='Comprehensive brake inspection and service',
                    duration=120,
                    price=3999.00
                ),
                Service(
                    name='Tire Rotation',
                    description='Tire rotation and balancing service',
                    duration=45,
                    price=999.00
                ),
                Service(
                    name='AC Service',
                    description='Air conditioning system check and service',
                    duration=90,
                    price=2499.00
                ),
                Service(
                    name='General Service',
                    description='Complete vehicle inspection and maintenance',
                    duration=180,
                    price=4999.00
                )
            ]
            
            for service in services:
                db.session.add(service)
            
            db.session.commit()
            print("Default services added successfully!")

if __name__ == '__main__':
    init_db()
    print("Database initialization completed!") 