"""
Clinic Management System - Database Models
NO PASSWORD HASHING - Plaintext passwords stored as per requirement
All currency, timezone, country, city are dynamic fields - NO HARDCODED VALUES
"""
from datetime import datetime, date
from app.extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """Base User Model - Super Admin, Admin (Doctor), Patient"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # PLAINTEXT - NO HASHING
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # For Call/WhatsApp - NO HARDCODING
    role = db.Column(db.String(20), nullable=False, default='patient')  # super_admin, admin, patient
    profile_picture = db.Column(db.String(255), default='uploads/default.jpg')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    companies = db.relationship('Company', backref='admin', lazy=True, foreign_keys='Company.admin_id', cascade='all, delete-orphan')
    doctor_appointments = db.relationship('Appointment', backref='doctor', lazy=True, foreign_keys='Appointment.doctor_id')
    patient_appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')
    patient_profile = db.relationship('PatientProfile', backref='user', lazy=True, uselist=False, cascade='all, delete-orphan')

    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'profile_picture': self.profile_picture,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_password:
            data['password'] = self.password
        return data

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Company(db.Model):
    """Company/Clinic Model - Created by Admin (Doctor)"""
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    timezone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(255), default='uploads/default_logo.jpg')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patients = db.relationship('PatientProfile', backref='company', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='company', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_admin=False):
        data = {
            'id': self.id,
            'name': self.name,
            'admin_id': self.admin_id,
            'country': self.country,
            'city': self.city,
            'currency': self.currency,
            'timezone': self.timezone,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'logo': self.logo,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_admin and self.admin:
            data['admin'] = self.admin.to_dict(include_password=True)
        return data

    def __repr__(self):
        return f'<Company {self.name}>'


class PatientProfile(db.Model):
    """Patient Profile - Linked to User and Company"""
    __tablename__ = 'patient_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'full_name': self.full_name,
            'age': self.age,
            'gender': self.gender,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<PatientProfile {self.full_name}>'


class Appointment(db.Model):
    """Appointment Model - Patient books slot with Doctor/Company"""
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    appointment_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20), default='pending')
    payment_status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_patient=False, include_doctor=False, include_company=False):
        data = {
            'id': self.id,
            'patient_id': self.patient_id,
            'company_id': self.company_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'time_slot': self.time_slot,
            'notes': self.notes,
            'status': self.status,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_patient and self.patient:
            data['patient'] = {
                'id': self.patient.id,
                'username': self.patient.username,
                'email': self.patient.email,
                'phone': self.patient.phone,
                'profile_picture': self.patient.profile_picture
            }
            if self.patient.patient_profile:
                data['patient']['full_name'] = self.patient.patient_profile.full_name
                data['patient']['age'] = self.patient.patient_profile.age
                data['patient']['gender'] = self.patient.patient_profile.gender

        if include_doctor and self.doctor:
            data['doctor'] = {
                'id': self.doctor.id,
                'username': self.doctor.username,
                'email': self.doctor.email,
                'phone': self.doctor.phone,
                'profile_picture': self.doctor.profile_picture
            }

        if include_company and self.company:
            data['company'] = self.company.to_dict()

        return data

    def __repr__(self):
        return f'<Appointment {self.id} - {self.status} - {self.payment_status}>'