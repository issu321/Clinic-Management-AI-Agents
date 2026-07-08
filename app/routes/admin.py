"""
Admin (Doctor) Routes - Complete Business Logic
Handles: Company Management, Appointments, Payments, Patient Records, Call/WhatsApp
"""
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date
from app.extensions import db
from app.models import User, Company, Appointment, PatientProfile
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response, format_currency_amount, is_ajax_request

admin_bp = Blueprint('admin', __name__)


# ============================================================
# DASHBOARD & COMPANY MANAGEMENT
# ============================================================

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Admin Dashboard
    Template: app/templates/admin/dashboard.html
    """
    company_id = session.get('company_id')
    if not company_id:
        companies = Company.query.filter_by(admin_id=current_user.id).all()
        if len(companies) == 1:
            session['company_id'] = companies[0].id
            company_id = companies[0].id
        else:
            return redirect(url_for('admin.select_company'))

    company = Company.query.get_or_404(company_id)
    if company.admin_id != current_user.id:
        return error_response('Unauthorized access to this company', 403)

    # Get all companies for this admin (for companies_count)
    all_companies = Company.query.filter_by(admin_id=current_user.id).all()

    # Stats
    total_appointments = Appointment.query.filter_by(company_id=company_id).count()
    pending_appointments = Appointment.query.filter_by(company_id=company_id, status='pending').count()
    completed_appointments = Appointment.query.filter_by(company_id=company_id, status='completed').count()
    total_patients = PatientProfile.query.filter_by(company_id=company_id).count()

    # Recent appointments with patient details
    recent_appointments = Appointment.query.filter_by(company_id=company_id)\
        .order_by(Appointment.created_at.desc()).limit(10).all()

    dashboard_data = {
        'company': company.to_dict(),
        'stats': {
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
            'completed_appointments': completed_appointments,
            'total_patients': total_patients
        },
        'recent_appointments': [a.to_dict(include_patient=True) for a in recent_appointments],
        'currency': company.currency,
        'companies_count': len(all_companies)
    }

    return render_template('admin/dashboard.html', data=dashboard_data)


@admin_bp.route('/select-company')
@login_required
@admin_required
def select_company():
    """
    Company Selection Page (when admin has multiple companies)
    Template: app/templates/admin/select_company.html
    """
    companies = Company.query.filter_by(admin_id=current_user.id).all()
    return render_template('admin/select_company.html', companies=[c.to_dict() for c in companies])


@admin_bp.route('/set-company/<int:company_id>', methods=['POST'])
@login_required
@admin_required
def set_company(company_id):
    """Set active company in session"""
    company = Company.query.filter_by(id=company_id, admin_id=current_user.id).first()
    if not company:
        return error_response('Company not found or unauthorized')
    session['company_id'] = company_id
    return success_response(message='Company selected successfully')


# ============================================================
# APPOINTMENTS (HTML PAGE + JSON API)
# ============================================================

@admin_bp.route('/appointments')
@login_required
@admin_required
def get_appointments():
    """
    Appointments page - Renders HTML template with data
    Template: app/templates/admin/appointments.html
    """
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('admin.select_company'))

    company = Company.query.get(company_id)
    status_filter = request.args.get('status')
    date_filter = request.args.get('date')

    query = Appointment.query.filter_by(company_id=company_id)

    if status_filter:
        query = query.filter_by(status=status_filter)
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=filter_date)
        except ValueError:
            pass

    appointments = query.order_by(Appointment.appointment_date.desc(), Appointment.created_at.desc()).all()

    return render_template('admin/appointments.html', 
                         appointments=[a.to_dict(include_patient=True, include_company=True) for a in appointments],
                         company=company.to_dict(),
                         currency=company.currency)


@admin_bp.route('/appointment/<int:appointment_id>')
@login_required
@admin_required
def get_appointment(appointment_id):
    """Get single appointment details (JSON for AJAX)"""
    company_id = session.get('company_id')
    appointment = Appointment.query.filter_by(id=appointment_id, company_id=company_id).first()
    if not appointment:
        return error_response('Appointment not found', 404)
    return success_response(
        data=appointment.to_dict(include_patient=True, include_company=True)
    )


@admin_bp.route('/appointment/<int:appointment_id>/complete', methods=['POST'])
@login_required
@admin_required
def mark_appointment_complete(appointment_id):
    """Mark appointment as completed after surgery"""
    company_id = session.get('company_id')
    appointment = Appointment.query.filter_by(id=appointment_id, company_id=company_id).first()
    if not appointment:
        if is_ajax_request():
            return error_response('Appointment not found', 404)
        flash('Appointment not found', 'error')
        return redirect(url_for('admin.get_appointments'))

    if appointment.status == 'completed':
        if is_ajax_request():
            return error_response('Appointment already completed')
        flash('Appointment already completed', 'warning')
        return redirect(url_for('admin.get_appointments'))

    # FIX: request.get_json() throws 415 on form submissions. Use request.form first.
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    amount = data.get('amount', 0)

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        amount = 0.0

    appointment.status = 'completed'
    appointment.amount = amount
    appointment.doctor_id = current_user.id
    db.session.commit()

    if is_ajax_request():
        return success_response(
            data=appointment.to_dict(include_patient=True),
            message='Appointment marked as completed'
        )
    flash('Appointment marked as completed', 'success')
    return redirect(url_for('admin.get_appointments'))


@admin_bp.route('/appointment/<int:appointment_id>/payment', methods=['POST'])
@login_required
@admin_required
def mark_payment_complete(appointment_id):
    """Mark payment as received (cash or online)"""
    company_id = session.get('company_id')
    appointment = Appointment.query.filter_by(id=appointment_id, company_id=company_id).first()
    if not appointment:
        if is_ajax_request():
            return error_response('Appointment not found', 404)
        flash('Appointment not found', 'error')
        return redirect(url_for('admin.get_appointments'))

    if appointment.status != 'completed':
        if is_ajax_request():
            return error_response('Appointment must be completed first')
        flash('Appointment must be completed first', 'warning')
        return redirect(url_for('admin.get_appointments'))

    if appointment.payment_status == 'completed':
        if is_ajax_request():
            return error_response('Payment already marked as completed')
        flash('Payment already marked as completed', 'warning')
        return redirect(url_for('admin.get_appointments'))

    # FIX: request.get_json() throws 415 on form submissions. Use request.form first.
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    payment_method = data.get('payment_method')

    if payment_method not in ['online', 'cash']:
        if is_ajax_request():
            return error_response('Payment method must be online or cash')
        flash('Payment method must be online or cash', 'error')
        return redirect(url_for('admin.get_appointments'))

    appointment.payment_method = payment_method
    appointment.payment_status = 'completed'
    db.session.commit()

    if is_ajax_request():
        return success_response(
            data=appointment.to_dict(include_patient=True),
            message=f'Payment marked as completed via {payment_method}'
        )
    flash(f'Payment marked as completed via {payment_method}', 'success')
    return redirect(url_for('admin.get_appointments'))


@admin_bp.route('/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    company_id = session.get('company_id')
    appointment = Appointment.query.filter_by(id=appointment_id, company_id=company_id).first()
    if not appointment:
        if is_ajax_request():
            return error_response('Appointment not found', 404)
        flash('Appointment not found', 'error')
        return redirect(url_for('admin.get_appointments'))

    appointment.status = 'cancelled'
    db.session.commit()

    if is_ajax_request():
        return success_response(message='Appointment cancelled successfully')
    flash('Appointment cancelled successfully', 'success')
    return redirect(url_for('admin.get_appointments'))


# ============================================================
# PATIENTS (HTML PAGE)
# ============================================================

@admin_bp.route('/patients')
@login_required
@admin_required
def get_patients():
    """
    Patients page - Renders HTML template
    Template: app/templates/admin/patients.html
    """
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('admin.select_company'))

    company = Company.query.get(company_id)
    patients = PatientProfile.query.filter_by(company_id=company_id).all()

    patient_list = []
    for p in patients:
        patient_data = p.to_dict()
        patient_data['user'] = p.user.to_dict()
        patient_data['appointments'] = [
            a.to_dict() for a in Appointment.query.filter_by(patient_id=p.user_id, company_id=company_id).all()
        ]
        patient_data['appointment_count'] = len(patient_data['appointments'])
        patient_list.append(patient_data)

    return render_template('admin/patients.html', 
                         patients=patient_list, 
                         company=company.to_dict())


@admin_bp.route('/patient/<int:patient_id>')
@login_required
@admin_required
def get_patient(patient_id):
    """Get specific patient details (JSON for AJAX/modal)"""
    company_id = session.get('company_id')
    profile = PatientProfile.query.filter_by(id=patient_id, company_id=company_id).first()
    if not profile:
        return error_response('Patient not found', 404)

    patient_data = profile.to_dict()
    patient_data['user'] = profile.user.to_dict()
    patient_data['appointments'] = [
        a.to_dict(include_company=True) for a in 
        Appointment.query.filter_by(patient_id=profile.user_id, company_id=company_id).order_by(Appointment.created_at.desc()).all()
    ]

    return success_response(data=patient_data)


# ============================================================
# FINANCIAL RECORDS (HTML PAGE - NO MORE JSON BLACK SCREEN!)
# ============================================================

@admin_bp.route('/records')
@login_required
@admin_required
def get_records():
    """
    Records page - Renders HTML template with data
    Template: app/templates/admin/records.html
    """
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('admin.select_company'))

    company = Company.query.get(company_id)

    appointments = Appointment.query.filter_by(company_id=company_id, status='completed')\
        .order_by(Appointment.appointment_date.desc()).all()

    records = []
    total_revenue = 0
    for a in appointments:
        record = a.to_dict(include_patient=True)
        record['formatted_amount'] = format_currency_amount(a.amount, company.currency)
        records.append(record)
        if a.payment_status == 'completed':
            total_revenue += (a.amount or 0)

    return render_template('admin/records.html',
                         records=records,
                         total_revenue=format_currency_amount(total_revenue, company.currency),
                         currency=company.currency,
                         company=company.to_dict())