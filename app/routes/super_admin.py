"""
Super Admin Routes - Complete Monitoring & Management
Handles: Monitor all companies, see admin passwords, manage users, change passwords
DELETE features added: Delete Company, Delete User with safety guards
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Company, Appointment, PatientProfile
from app.utils.decorators import super_admin_required
from app.utils.helpers import success_response, error_response

super_admin_bp = Blueprint('super_admin', __name__)


# ============================================================
# DASHBOARD (HTML PAGE)
# ============================================================

@super_admin_bp.route('/dashboard')
@login_required
@super_admin_required
def dashboard():
    """
    Super Admin Dashboard
    Template: app/templates/super_admin/dashboard.html
    """
    total_companies = Company.query.count()
    total_admins = User.query.filter_by(role='admin').count()
    total_patients = User.query.filter_by(role='patient').count()
    total_appointments = Appointment.query.count()

    recent_companies = Company.query.order_by(Company.created_at.desc()).limit(20).all()

    dashboard_data = {
        'stats': {
            'total_companies': total_companies,
            'total_admins': total_admins,
            'total_patients': total_patients,
            'total_appointments': total_appointments
        },
        'recent_companies': [c.to_dict(include_admin=True) for c in recent_companies]
    }

    return render_template('super_admin/dashboard.html', data=dashboard_data)


# ============================================================
# COMPANIES (HTML PAGE)
# ============================================================

@super_admin_bp.route('/companies')
@login_required
@super_admin_required
def get_all_companies():
    """
    All companies page with admin details including PASSWORDS
    Template: app/templates/super_admin/companies.html
    """
    companies = Company.query.order_by(Company.created_at.desc()).all()

    company_list = []
    for c in companies:
        company_data = c.to_dict(include_admin=True)
        company_data['patient_count'] = PatientProfile.query.filter_by(company_id=c.id).count()
        company_data['appointment_count'] = Appointment.query.filter_by(company_id=c.id).count()
        company_list.append(company_data)

    return render_template('super_admin/companies.html', companies=company_list)


@super_admin_bp.route('/company/<int:company_id>')
@login_required
@super_admin_required
def get_company_details(company_id):
    """Company detail page - passes unified data dict matching template expectations"""
    company = Company.query.get_or_404(company_id)
    admin = User.query.get(company.admin_id)

    # Build admin dict with plaintext password
    admin_dict = None
    if admin:
        admin_dict = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'phone': admin.phone,
            'password': admin.password,
            'profile_picture': admin.profile_picture,
            'is_active': admin.is_active,
            'role': admin.role
        }

    # Build patients list with profile fields at top level + nested user dict + appointments
    patients = []
    for p in PatientProfile.query.filter_by(company_id=company_id).all():
        user = User.query.get(p.user_id)
        patient_data = {
            'id': p.id,
            'full_name': p.full_name,
            'age': p.age,
            'gender': p.gender,
            'address': p.address,
            'emergency_contact': p.emergency_contact,
            'medical_history': p.medical_history,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'password': user.password,
                'profile_picture': user.profile_picture,
                'is_active': user.is_active
            } if user else {},
            'appointments': []
        }
        for a in Appointment.query.filter_by(patient_id=p.user_id, company_id=company_id).all():
            patient_data['appointments'].append({
                'id': a.id,
                'appointment_date': a.appointment_date,
                'time_slot': a.time_slot,
                'status': a.status,
                'amount': a.amount,
                'payment_method': a.payment_method,
                'payment_status': a.payment_status
            })
        patients.append(patient_data)

    # Build appointments list with patient profile + nested user dict
    appointments = []
    for a in Appointment.query.filter_by(company_id=company_id).order_by(Appointment.created_at.desc()).all():
        user = User.query.get(a.patient_id)
        profile = PatientProfile.query.filter_by(user_id=a.patient_id).first()

        appt_data = {
            'id': a.id,
            'appointment_date': a.appointment_date,
            'time_slot': a.time_slot,
            'status': a.status,
            'amount': a.amount,
            'payment_method': a.payment_method,
            'payment_status': a.payment_status,
            'notes': a.notes,
            'patient': {}
        }

        if profile:
            appt_data['patient'] = {
                'full_name': profile.full_name,
                'age': profile.age,
                'gender': profile.gender,
                'address': profile.address,
                'emergency_contact': profile.emergency_contact,
            }

        if user:
            appt_data['patient']['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'password': user.password,
                'profile_picture': user.profile_picture,
                'is_active': user.is_active
            }

        appointments.append(appt_data)

    data = {
        'company': {
            'id': company.id,
            'name': company.name,
            'country': company.country,
            'city': company.city,
            'currency': company.currency,
            'timezone': company.timezone,
            'address': company.address,
            'phone': company.phone,
            'email': company.email,
            'logo': company.logo,
            'description': company.description,
            'created_at': company.created_at
        },
        'admin': admin_dict,
        'patients': patients,
        'appointments': appointments
    }

    return render_template('super_admin/company_detail.html', data=data)


# ============================================================
# DELETE COMPANY (NEW FEATURE)
# ============================================================

@super_admin_bp.route('/company/<int:company_id>/delete', methods=['POST'])
@login_required
@super_admin_required
def delete_company(company_id):
    """
    Delete a company/clinic and all associated data.
    Cascades: patient profiles, appointments under this company.
    Does NOT delete the admin user - admin becomes orphaned but can create new company.
    """
    company = Company.query.get_or_404(company_id)

    company_name = company.name
    admin_id = company.admin_id

    # Delete all appointments for this company
    Appointment.query.filter_by(company_id=company_id).delete()

    # Delete all patient profiles for this company
    # But keep the user accounts - they can re-register elsewhere
    PatientProfile.query.filter_by(company_id=company_id).delete()

    # Delete the company itself
    db.session.delete(company)
    db.session.commit()

    return success_response(
        data={'company_id': company_id, 'company_name': company_name, 'admin_id': admin_id},
        message=f'Company "{company_name}" and all associated data deleted successfully'
    )


# ============================================================
# USERS (HTML PAGE)
# ============================================================

@super_admin_bp.route('/users')
@login_required
@super_admin_required
def get_all_users():
    """
    All users page with passwords visible
    Template: app/templates/super_admin/users.html
    """
    role_filter = request.args.get('role')
    search = request.args.get('search')

    query = User.query

    if role_filter:
        query = query.filter_by(role=role_filter)
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )

    users = query.order_by(User.created_at.desc()).all()

    return render_template('super_admin/users.html',
                         users=[u.to_dict(include_password=True) for u in users])


@super_admin_bp.route('/company/<int:company_id>/users')
@login_required
@super_admin_required
def get_company_users(company_id):
    """Company users page - uses same template and data structure as get_company_details"""
    company = Company.query.get_or_404(company_id)
    admin = User.query.get(company.admin_id)

    # Build admin dict with plaintext password
    admin_dict = None
    if admin:
        admin_dict = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'phone': admin.phone,
            'password': admin.password,
            'profile_picture': admin.profile_picture,
            'is_active': admin.is_active,
            'role': admin.role
        }

    # Build patients list with profile fields at top level + nested user dict + appointments
    patients = []
    for p in PatientProfile.query.filter_by(company_id=company_id).all():
        user = User.query.get(p.user_id)
        patient_data = {
            'id': p.id,
            'full_name': p.full_name,
            'age': p.age,
            'gender': p.gender,
            'address': p.address,
            'emergency_contact': p.emergency_contact,
            'medical_history': p.medical_history,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'password': user.password,
                'profile_picture': user.profile_picture,
                'is_active': user.is_active
            } if user else {},
            'appointments': []
        }
        for a in Appointment.query.filter_by(patient_id=p.user_id, company_id=company_id).all():
            patient_data['appointments'].append({
                'id': a.id,
                'appointment_date': a.appointment_date,
                'time_slot': a.time_slot,
                'status': a.status,
                'amount': a.amount,
                'payment_method': a.payment_method,
                'payment_status': a.payment_status
            })
        patients.append(patient_data)

    # Build appointments list with patient profile + nested user dict
    appointments = []
    for a in Appointment.query.filter_by(company_id=company_id).order_by(Appointment.created_at.desc()).all():
        user = User.query.get(a.patient_id)
        profile = PatientProfile.query.filter_by(user_id=a.patient_id).first()

        appt_data = {
            'id': a.id,
            'appointment_date': a.appointment_date,
            'time_slot': a.time_slot,
            'status': a.status,
            'amount': a.amount,
            'payment_method': a.payment_method,
            'payment_status': a.payment_status,
            'notes': a.notes,
            'patient': {}
        }

        if profile:
            appt_data['patient'] = {
                'full_name': profile.full_name,
                'age': profile.age,
                'gender': profile.gender,
                'address': profile.address,
                'emergency_contact': profile.emergency_contact,
            }

        if user:
            appt_data['patient']['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'password': user.password,
                'profile_picture': user.profile_picture,
                'is_active': user.is_active
            }

        appointments.append(appt_data)

    data = {
        'company': {
            'id': company.id,
            'name': company.name,
            'country': company.country,
            'city': company.city,
            'currency': company.currency,
            'timezone': company.timezone,
            'address': company.address,
            'phone': company.phone,
            'email': company.email,
            'logo': company.logo,
            'description': company.description,
            'created_at': company.created_at
        },
        'admin': admin_dict,
        'patients': patients,
        'appointments': appointments
    }

    return render_template('super_admin/company_detail.html', data=data)


# ============================================================
# DELETE USER (NEW FEATURE)
# ============================================================

@super_admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@super_admin_required
def delete_user(user_id):
    """
    Delete a user and all their associated data.
    Safety guards:
    - Cannot delete yourself
    - Cannot delete the last remaining super admin
    - If admin: delete their companies (which cascades patients + appointments)
    - If patient: delete their profile + appointments
    """
    user = User.query.get_or_404(user_id)

    # Guard 1: Cannot delete yourself
    if user.id == current_user.id:
        return error_response('You cannot delete your own account', 403)

    # Guard 2: Cannot delete the last super admin
    if user.role == 'super_admin':
        super_admin_count = User.query.filter_by(role='super_admin').count()
        if super_admin_count <= 1:
            return error_response('Cannot delete the last super admin account', 403)

    username = user.username
    role = user.role

    if user.role == 'admin':
        # Delete all companies owned by this admin (cascade deletes patients + appointments)
        companies = Company.query.filter_by(admin_id=user_id).all()
        for company in companies:
            Appointment.query.filter_by(company_id=company.id).delete()
            PatientProfile.query.filter_by(company_id=company.id).delete()
            db.session.delete(company)

    elif user.role == 'patient':
        # Delete patient profile
        PatientProfile.query.filter_by(user_id=user_id).delete()
        # Delete all their appointments
        Appointment.query.filter_by(patient_id=user_id).delete()

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return success_response(
        data={'user_id': user_id, 'username': username, 'role': role},
        message=f'User "{username}" ({role}) and all associated data deleted successfully'
    )


# ============================================================
# PASSWORD MANAGEMENT (JSON APIs for AJAX)
# ============================================================

@super_admin_bp.route('/user/<int:user_id>/change-password', methods=['POST'])
@login_required
@super_admin_required
def change_user_password(user_id):
    """Change any user's password"""
    user = User.query.get_or_404(user_id)

    data = request.get_json() or request.form.to_dict()
    new_password = data.get('new_password')

    if not new_password or len(new_password) < 4:
        return error_response('New password must be at least 4 characters')

    old_password = user.password
    user.password = new_password
    db.session.commit()

    return success_response(
        data={
            'user_id': user.id,
            'username': user.username,
            'old_password': old_password,
            'new_password': new_password,
            'role': user.role
        },
        message=f'Password changed successfully for {user.username}'
    )


@super_admin_bp.route('/user/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@super_admin_required
def toggle_user_status(user_id):
    """Activate/Deactivate user account"""
    user = User.query.get_or_404(user_id)

    if user.role == 'super_admin':
        return error_response('Cannot deactivate super admin')

    user.is_active = not user.is_active
    db.session.commit()

    status = 'activated' if user.is_active else 'deactivated'
    return success_response(
        data=user.to_dict(include_password=True),
        message=f'User {status} successfully'
    )


# ============================================================
# SYSTEM STATS (JSON API for AJAX/dashboard widgets)
# ============================================================

@super_admin_bp.route('/stats')
@login_required
@super_admin_required
def get_system_stats():
    """Get complete system statistics (JSON for AJAX)"""
    stats = {
        'total_users': User.query.count(),
        'super_admins': User.query.filter_by(role='super_admin').count(),
        'admins': User.query.filter_by(role='admin').count(),
        'patients': User.query.filter_by(role='patient').count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'inactive_users': User.query.filter_by(is_active=False).count(),
        'total_companies': Company.query.count(),
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'completed_appointments': Appointment.query.filter_by(status='completed').count(),
        'cancelled_appointments': Appointment.query.filter_by(status='cancelled').count(),
        'completed_payments': Appointment.query.filter_by(payment_status='completed').count(),
        'pending_payments': Appointment.query.filter_by(payment_status='pending').count(),
        'companies_by_currency': {},
        'companies_by_country': {}
    }

    for company in Company.query.all():
        currency = company.currency
        country = company.country
        stats['companies_by_currency'][currency] = stats['companies_by_currency'].get(currency, 0) + 1
        stats['companies_by_country'][country] = stats['companies_by_country'].get(country, 0) + 1

    return success_response(data=stats)


# ============================================================
# CHARTS DATA API (NEW - For Real-time Graphs)
# ============================================================

@super_admin_bp.route('/charts-data')
@login_required
@super_admin_required
def get_charts_data():
    """
    Returns structured data for Chart.js visualizations.
    All data is computed dynamically from the database.
    """
    from sqlalchemy import func, extract
    from datetime import datetime, timedelta

    # --- User Growth Over Time (last 12 months) ---
    now = datetime.utcnow()
    months = []
    user_growth = {'admins': [], 'patients': [], 'super_admins': []}
    for i in range(11, -1, -1):
        month_start = now.replace(day=1) - timedelta(days=i*30)
        month_label = month_start.strftime('%b %Y')
        months.append(month_label)
        user_growth['admins'].append(
            User.query.filter_by(role='admin').filter(User.created_at < month_start + timedelta(days=30)).count()
        )
        user_growth['patients'].append(
            User.query.filter_by(role='patient').filter(User.created_at < month_start + timedelta(days=30)).count()
        )
        user_growth['super_admins'].append(
            User.query.filter_by(role='super_admin').filter(User.created_at < month_start + timedelta(days=30)).count()
        )

    # --- Appointments by Status ---
    appt_status = {
        'labels': ['Pending', 'Completed', 'Cancelled'],
        'data': [
            Appointment.query.filter_by(status='pending').count(),
            Appointment.query.filter_by(status='completed').count(),
            Appointment.query.filter_by(status='cancelled').count()
        ],
        'colors': ['#fbbf24', '#34d399', '#f87171']
    }

    # --- Payment Status ---
    payment_status = {
        'labels': ['Completed', 'Pending'],
        'data': [
            Appointment.query.filter_by(payment_status='completed').count(),
            Appointment.query.filter_by(payment_status='pending').count()
        ],
        'colors': ['#34d399', '#fbbf24']
    }

    # --- Companies by Country (top 10) ---
    country_counts = db.session.query(
        Company.country, func.count(Company.id)
    ).group_by(Company.country).order_by(func.count(Company.id).desc()).limit(10).all()
    companies_by_country = {
        'labels': [c[0] for c in country_counts],
        'data': [c[1] for c in country_counts]
    }

    # --- Companies by Currency ---
    currency_counts = db.session.query(
        Company.currency, func.count(Company.id)
    ).group_by(Company.currency).order_by(func.count(Company.id).desc()).all()
    companies_by_currency = {
        'labels': [c[0] for c in currency_counts],
        'data': [c[1] for c in currency_counts]
    }

    # --- Role Distribution ---
    role_dist = {
        'labels': ['Super Admins', 'Admins', 'Patients'],
        'data': [
            User.query.filter_by(role='super_admin').count(),
            User.query.filter_by(role='admin').count(),
            User.query.filter_by(role='patient').count()
        ],
        'colors': ['#818cf8', '#fbbf24', '#34d399']
    }

    # --- Weekly Appointments (last 7 days) ---
    week_labels = []
    week_data = []
    for i in range(6, -1, -1):
        day = now.date() - timedelta(days=i)
        week_labels.append(day.strftime('%a'))
        week_data.append(
            Appointment.query.filter(func.date(Appointment.appointment_date) == day).count()
        )
    weekly_appointments = {
        'labels': week_labels,
        'data': week_data
    }

    return success_response(data={
        'user_growth': {'labels': months, 'datasets': user_growth},
        'appointment_status': appt_status,
        'payment_status': payment_status,
        'companies_by_country': companies_by_country,
        'companies_by_currency': companies_by_currency,
        'role_distribution': role_dist,
        'weekly_appointments': weekly_appointments
    })