from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Import routes after db initialization to avoid circular imports
from app.routes import auth, main, admin, vehicle, service

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(main.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(vehicle.bp)
app.register_blueprint(service.bp)

if __name__ == '__main__':
    app.run(debug=True) 