"""
Clinic Management System - Flask Application Factory
Production-Ready Backend Architecture
"""
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # CSRF PROTECTION: Makes csrf_token() available in ALL templates
    # This fixes the Jinja2 UndefinedError for {{ csrf_token() }}
    csrf = CSRFProtect(app)

    login_manager.login_view = 'auth.login_page'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # User Loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # CONTEXT PROCESSOR: Makes 'developer' available in EVERY template automatically
    @app.context_processor
    def inject_developer():
        return {
            'developer': {
                'name': 'Mohammed Usman',
                'github': 'issu321',
                'portfolio': 'https://issu321.github.io/issu321',
                'email': 'jaafreeusman@gmail.com',
                'tagline': 'Made Easy for Doctors Worldwide',
                'software_name': 'ClinicPro Management System'
            }
        }

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.patient import patient_bp
    from app.routes.super_admin import super_admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(super_admin_bp, url_prefix='/super-admin')

    # Create database tables and default super admin
    with app.app_context():
        db.create_all()
        create_default_super_admin()

    return app


def create_default_super_admin():
    """Create default super admin if none exists
    WARNING: Password is stored in PLAINTEXT as per requirement
    Change immediately after first login
    """
    from app.models import User

    super_admin = User.query.filter_by(role='super_admin').first()
    if not super_admin:
        super_admin = User(
            username='superadmin',
            password='superadmin123',  # PLAINTEXT - CHANGE IMMEDIATELY
            email='superadmin@clinicpro.com',
            phone='+000000000000',
            role='super_admin',
            profile_picture='default.jpg'
        )
        db.session.add(super_admin)
        db.session.commit()
        print("=" * 60)
        print("DEFAULT SUPER ADMIN CREATED")
        print("Username: superadmin")
        print("Password: superadmin123")
        print("Email: superadmin@clinicpro.com")
        print("=" * 60)
