"""
Authentication Routes - Complete Registration & Login System
Handles: Super Admin, Admin (Doctor), Patient Registration & Login
Company Selection at Login - NO HARDCODING
"""
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, Company, PatientProfile
from app.utils.helpers import save_file, success_response, error_response, is_ajax_request
import os

auth_bp = Blueprint('auth', __name__)


# ============================================================
# REGISTRATION ROUTES
# ============================================================

@auth_bp.route('/register/super-admin', methods=['POST'])
def register_super_admin():
    """
    Super Admin Registration
    Body: {username, password, email, phone, profile_picture(file)}
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    required = ['username', 'password', 'email', 'phone']
    for field in required:
        if not data.get(field):
            if is_ajax_request():
                return error_response(f'{field} is required')
            flash(f'{field} is required', 'error')
            return redirect(url_for('auth.register_page', role='super_admin'))

    if User.query.filter_by(username=data['username']).first():
        if is_ajax_request():
            return error_response('Username already exists')
        flash('Username already exists', 'error')
        return redirect(url_for('auth.register_page', role='super_admin'))
    if User.query.filter_by(email=data['email']).first():
        if is_ajax_request():
            return error_response('Email already exists')
        flash('Email already exists', 'error')
        return redirect(url_for('auth.register_page', role='super_admin'))

    profile_pic = 'uploads/default.jpg'
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file.filename:
            saved = save_file(file, 'profiles')
            if saved:
                profile_pic = saved

    user = User(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        phone=data['phone'],
        role='super_admin',
        profile_picture=profile_pic
    )
    db.session.add(user)
    db.session.commit()

    if is_ajax_request():
        return success_response(
            data=user.to_dict(),
            message='Super Admin registered successfully'
        )
    flash('Super Admin registered successfully', 'success')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/register/admin', methods=['POST'])
def register_admin():
    """
    Admin (Doctor) Registration with Company Creation
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    user_required = ['username', 'password', 'email', 'phone']
    for field in user_required:
        if not data.get(field):
            if is_ajax_request():
                return error_response(f'{field} is required for doctor')
            flash(f'{field} is required for doctor', 'error')
            return redirect(url_for('auth.register_page', role='admin'))

    company_required = ['company_name', 'country', 'city', 'currency', 'timezone', 'address', 'company_phone', 'company_email']
    for field in company_required:
        if not data.get(field):
            if is_ajax_request():
                return error_response(f'{field} is required for company')
            flash(f'{field} is required for company', 'error')
            return redirect(url_for('auth.register_page', role='admin'))

    if User.query.filter_by(username=data['username']).first():
        if is_ajax_request():
            return error_response('Username already exists')
        flash('Username already exists', 'error')
        return redirect(url_for('auth.register_page', role='admin'))
    if User.query.filter_by(email=data['email']).first():
        if is_ajax_request():
            return error_response('Email already exists')
        flash('Email already exists', 'error')
        return redirect(url_for('auth.register_page', role='admin'))

    profile_pic = 'uploads/default.jpg'
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file.filename:
            saved = save_file(file, 'profiles')
            if saved:
                profile_pic = saved

    admin = User(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        phone=data['phone'],
        role='admin',
        profile_picture=profile_pic
    )
    db.session.add(admin)
    db.session.flush()

    logo = 'uploads/default_logo.jpg'
    if 'logo' in request.files:
        file = request.files['logo']
        if file.filename:
            saved = save_file(file, 'logos')
            if saved:
                logo = saved

    company = Company(
        name=data['company_name'],
        admin_id=admin.id,
        country=data['country'],
        city=data['city'],
        currency=data['currency'],
        timezone=data['timezone'],
        address=data['address'],
        phone=data['company_phone'],
        email=data['company_email'],
        logo=logo,
        description=data.get('description', '')
    )
    db.session.add(company)
    db.session.commit()

    if is_ajax_request():
        return success_response(
            data={
                'admin': admin.to_dict(),
                'company': company.to_dict()
            },
            message='Doctor and Clinic registered successfully'
        )
    flash('Doctor and Clinic registered successfully', 'success')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/register/patient', methods=['POST'])
def register_patient():
    """
    Patient Registration under selected Company
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    required = ['username', 'password', 'email', 'phone', 'company_id', 'full_name']
    for field in required:
        if not data.get(field):
            if is_ajax_request():
                return error_response(f'{field} is required')
            flash(f'{field} is required', 'error')
            return redirect(url_for('auth.register_page', role='patient'))

    company = Company.query.get(data['company_id'])
    if not company:
        if is_ajax_request():
            return error_response('Invalid company selected')
        flash('Invalid company selected', 'error')
        return redirect(url_for('patient.get_all_companies'))

    if User.query.filter_by(username=data['username']).first():
        if is_ajax_request():
            return error_response('Username already exists')
        flash('Username already exists', 'error')
        return redirect(url_for('auth.register_page', role='patient'))
    if User.query.filter_by(email=data['email']).first():
        if is_ajax_request():
            return error_response('Email already exists')
        flash('Email already exists', 'error')
        return redirect(url_for('auth.register_page', role='patient'))

    patient = User(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        phone=data['phone'],
        role='patient',
        profile_picture='uploads/default.jpg'
    )
    db.session.add(patient)
    db.session.flush()

    profile = PatientProfile(
        user_id=patient.id,
        company_id=data['company_id'],
        full_name=data['full_name'],
        age=data.get('age'),
        gender=data.get('gender'),
        address=data.get('address'),
        emergency_contact=data.get('emergency_contact'),
        medical_history=data.get('medical_history', '')
    )
    db.session.add(profile)
    db.session.commit()

    if is_ajax_request():
        return success_response(
            data={
                'patient': patient.to_dict(),
                'profile': profile.to_dict(),
                'company': company.to_dict()
            },
            message='Patient registered successfully'
        )
    flash('Patient registered successfully', 'success')
    return redirect(url_for('auth.login_page'))


# ============================================================
# LOGIN ROUTES
# ============================================================

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Universal Login with Role Detection
    Body: {username, password, company_id}
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    username = data.get('username')
    password = data.get('password')
    company_id = data.get('company_id')

    if not username or not password:
        if is_ajax_request():
            return error_response('Username and password are required')
        flash('Username and password are required', 'error')
        return redirect(url_for('auth.login_page'))

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        if is_ajax_request():
            return error_response('Invalid username or password')
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login_page'))

    if not user.is_active:
        if is_ajax_request():
            return error_response('Account is deactivated')
        flash('Account is deactivated', 'error')
        return redirect(url_for('auth.login_page'))

    if user.role == 'super_admin':
        login_user(user)
        session['role'] = 'super_admin'
        if is_ajax_request():
            return success_response(
                data={'user': user.to_dict(), 'role': 'super_admin'},
                message='Super Admin logged in successfully'
            )
        return redirect(url_for('super_admin.dashboard'))

    elif user.role == 'admin':
        companies = Company.query.filter_by(admin_id=user.id).all()
        if not companies:
            if is_ajax_request():
                return error_response('No companies found for this admin')
            flash('No companies found for this admin', 'error')
            return redirect(url_for('auth.login_page'))

        if len(companies) == 1:
            selected_company = companies[0]
            login_user(user)
            session['role'] = 'admin'
            session['company_id'] = selected_company.id
            if is_ajax_request():
                return success_response(
                    data={
                        'user': user.to_dict(),
                        'role': 'admin',
                        'company': selected_company.to_dict(),
                        'companies_count': 1
                    },
                    message='Admin logged in successfully'
                )
            return redirect(url_for('admin.dashboard'))
        else:
            if not company_id:
                login_user(user)
                session['role'] = 'admin'
                if is_ajax_request():
                    return success_response(
                        data={
                            'user': user.to_dict(),
                            'role': 'admin',
                            'companies': [c.to_dict() for c in companies],
                            'require_company_selection': True
                        },
                        message='Please select a company to continue'
                    )
                return redirect(url_for('admin.select_company'))

            selected_company = Company.query.filter_by(id=company_id, admin_id=user.id).first()
            if not selected_company:
                if is_ajax_request():
                    return error_response('Invalid company selected')
                flash('Invalid company selected', 'error')
                return redirect(url_for('auth.login_page'))

            login_user(user)
            session['role'] = 'admin'
            session['company_id'] = selected_company.id
            if is_ajax_request():
                return success_response(
                    data={
                        'user': user.to_dict(),
                        'role': 'admin',
                        'company': selected_company.to_dict(),
                        'companies_count': len(companies)
                    },
                    message='Admin logged in successfully'
                )
            return redirect(url_for('admin.dashboard'))

    elif user.role == 'patient':
        if not company_id:
            profile = PatientProfile.query.filter_by(user_id=user.id).first()
            if profile:
                company = Company.query.get(profile.company_id)
                login_user(user)
                session['role'] = 'patient'
                session['company_id'] = company.id
                if is_ajax_request():
                    return success_response(
                        data={
                            'user': user.to_dict(),
                            'role': 'patient',
                            'company': company.to_dict()
                        },
                        message='Patient logged in successfully'
                    )
                return redirect(url_for('patient.dashboard'))
            else:
                if is_ajax_request():
                    return error_response('No company association found')
                flash('No company association found', 'error')
                return redirect(url_for('auth.login_page'))

        profile = PatientProfile.query.filter_by(user_id=user.id, company_id=company_id).first()
        if not profile:
            if is_ajax_request():
                return error_response('You are not registered with this company')
            flash('You are not registered with this company', 'error')
            return redirect(url_for('auth.login_page'))

        company = Company.query.get(company_id)
        login_user(user)
        session['role'] = 'patient'
        session['company_id'] = company_id
        if is_ajax_request():
            return success_response(
                data={
                    'user': user.to_dict(),
                    'role': 'patient',
                    'company': company.to_dict()
                },
                message='Patient logged in successfully'
            )
        return redirect(url_for('patient.dashboard'))

    return error_response('Invalid user role')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout and clear session - FIXED: No more JSON black screen"""
    logout_user()
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/login-page')
def login_page():
    """Redirect authenticated users to their dashboard - NEVER show login to logged-in users"""
    if current_user.is_authenticated:
        if current_user.role == 'super_admin':
            return redirect(url_for('super_admin.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient.dashboard'))
    return render_template('auth/login.html')


@auth_bp.route('/register-page')
def register_page():
    """
    PLACEHOLDER: app/templates/auth/register.html
    Super admins can still access registration to create other super admins.
    All other authenticated users get redirected to their dashboard.
    """
    if current_user.is_authenticated and current_user.role != 'super_admin':
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient.dashboard'))
    role = request.args.get('role', 'patient')
    return render_template('auth/register.html', role=role)