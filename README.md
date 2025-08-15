# Vehicle Service Booking System

A Flask-based web application for managing vehicle service bookings.

## Features

- User registration and authentication
- Vehicle management
- Service appointment booking
- Admin dashboard for managing services and appointments
- Secure password handling

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
- Create a new database named 'vehicle_service_db'
- Update the database configuration in `.env` file

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

## Environment Variables

Create a `.env` file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=vehicle_service_db
```

## Project Structure

```
vehicle_service_booking/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── .env
├── app.py
├── init_db.py
└── requirements.txt
``` 
