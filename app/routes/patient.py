"""
Patient Routes - Complete Patient Functionality
Handles: Company Selection, Booking Slots, Viewing Doctor Details, Call/WhatsApp
"""
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from app.extensions import db
from app.models import User, Company, Appointment, PatientProfile
from app.utils.decorators import patient_required
from app.utils.helpers import success_response, error_response, is_ajax_request

patient_bp = Blueprint('patient', __name__)


# ============================================================
# COMPANY DISCOVERY (Public - No login required)
# ============================================================

@patient_bp.route('/companies')
def get_all_companies():
    """
    Get all registered companies for patient selection
    Template: app/templates/patient/companies.html
    FIX: Now also returns JSON for AJAX requests (registration page clinic loader)
    """
    companies = Company.query.all()
    companies_data = [c.to_dict(include_admin=True) for c in companies]

    # If AJAX request, return JSON (for dynamic clinic loaders on registration pages)
    if is_ajax_request():
        return success_response(data=companies_data)

    return render_template('patient/companies.html', companies=companies_data)


@patient_bp.route('/company/<int:company_id>')
def get_company_public(company_id):
    """
    Public company details page
    Template: app/templates/patient/company_detail.html
    """
    company = Company.query.get_or_404(company_id)
    company_data = company.to_dict(include_admin=True)

    doctor = User.query.get(company.admin_id)
    if doctor:
        company_data['doctor'] = {
            'name': doctor.username,
            'email': doctor.email,
            'phone': doctor.phone,
            'profile_picture': doctor.profile_picture
        }

    return render_template('patient/company_detail.html', company=company_data)


# ============================================================
# PATIENT DASHBOARD
# ============================================================

@patient_bp.route('/dashboard')
@login_required
@patient_required
def dashboard():
    """
    Patient Dashboard
    Template: app/templates/patient/dashboard.html
    """
    profile = PatientProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return error_response('Patient profile not found')

    company = Company.query.get(profile.company_id)
    doctor = User.query.get(company.admin_id)

    upcoming = Appointment.query.filter(
        Appointment.patient_id == current_user.id,
        Appointment.appointment_date >= date.today(),
        Appointment.status != 'cancelled'
    ).order_by(Appointment.appointment_date).all()

    past = Appointment.query.filter(
        Appointment.patient_id == current_user.id,
        Appointment.appointment_date < date.today()
    ).order_by(Appointment.appointment_date.desc()).all()

    dashboard_data = {
        'patient': current_user.to_dict(),
        'profile': profile.to_dict(),
        'company': company.to_dict(),
        'doctor': {
            'name': doctor.username,
            'email': doctor.email,
            'phone': doctor.phone,
            'profile_picture': doctor.profile_picture
        },
        'upcoming_appointments': [a.to_dict(include_company=True) for a in upcoming],
        'past_appointments': [a.to_dict(include_company=True) for a in past]
    }

    return render_template('patient/dashboard.html', data=dashboard_data)


# ============================================================
# APPOINTMENT BOOKING
# ============================================================

@patient_bp.route('/book-appointment', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment():
    """
    Book appointment page + handler
    Template: app/templates/patient/book_appointment.html
    FIX: request.get_json() throws 415 on form submissions. Use request.form first.
    """
    profile = PatientProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        if is_ajax_request():
            return error_response('Patient profile not found')
        flash('Patient profile not found', 'error')
        return redirect(url_for('patient.dashboard'))

    company = Company.query.get(profile.company_id)

    if request.method == 'POST':
        # FIX: request.get_json() fails with 415 when Content-Type is form data.
        # Only call get_json() when request.is_json is True.
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        required = ['appointment_date', 'time_slot']
        for field in required:
            if not data.get(field):
                if is_ajax_request():
                    return error_response(f'{field} is required')
                flash(f'{field} is required', 'error')
                return redirect(url_for('patient.book_appointment'))

        try:
            app_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
            if app_date < date.today():
                if is_ajax_request():
                    return error_response('Cannot book appointments in the past')
                flash('Cannot book appointments in the past', 'error')
                return redirect(url_for('patient.book_appointment'))
        except ValueError:
            if is_ajax_request():
                return error_response('Invalid date format. Use YYYY-MM-DD')
            flash('Invalid date format. Use YYYY-MM-DD', 'error')
            return redirect(url_for('patient.book_appointment'))

        existing = Appointment.query.filter_by(
            company_id=company.id,
            appointment_date=app_date,
            time_slot=data['time_slot'],
            status='pending'
        ).first()

        if existing:
            if is_ajax_request():
                return error_response('This time slot is already booked')
            flash('This time slot is already booked', 'error')
            return redirect(url_for('patient.book_appointment'))

        appointment = Appointment(
            patient_id=current_user.id,
            company_id=company.id,
            doctor_id=company.admin_id,
            appointment_date=app_date,
            time_slot=data['time_slot'],
            notes=data.get('notes', ''),
            status='pending',
            amount=0.0,
            payment_method='pending',
            payment_status='pending'
        )
        db.session.add(appointment)
        db.session.commit()

        if is_ajax_request():
            return success_response(
                data=appointment.to_dict(include_company=True),
                message='Appointment booked successfully'
            )
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('patient.my_appointments'))

    # GET request - show booking form
    return render_template('patient/book_appointment.html', company=company.to_dict())


@patient_bp.route('/my-appointments')
@login_required
@patient_required
def my_appointments():
    """
    My appointments page
    Template: app/templates/patient/my_appointments.html
    """
    appointments = Appointment.query.filter_by(patient_id=current_user.id)\
        .order_by(Appointment.appointment_date.desc()).all()

    return render_template('patient/my_appointments.html',
                         appointments=[a.to_dict(include_company=True, include_doctor=True) for a in appointments])


@patient_bp.route('/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@patient_required
def cancel_my_appointment(appointment_id):
    """Patient cancels their own appointment"""
    appointment = Appointment.query.filter_by(id=appointment_id, patient_id=current_user.id).first()
    if not appointment:
        if is_ajax_request():
            return error_response('Appointment not found', 404)
        flash('Appointment not found', 'error')
        return redirect(url_for('patient.my_appointments'))

    if appointment.status == 'completed':
        if is_ajax_request():
            return error_response('Cannot cancel completed appointment')
        flash('Cannot cancel completed appointment', 'error')
        return redirect(url_for('patient.my_appointments'))

    appointment.status = 'cancelled'
    db.session.commit()

    if is_ajax_request():
        return success_response(message='Appointment cancelled successfully')
    flash('Appointment cancelled successfully', 'success')
    return redirect(url_for('patient.my_appointments'))


# ============================================================
# AVAILABLE SLOTS (JSON API for AJAX)
# ============================================================

@patient_bp.route('/available-slots')
def get_available_slots():
    """Get available time slots for a company on a specific date (JSON for AJAX)"""
    company_id = request.args.get('company_id', type=int)
    date_str = request.args.get('date')

    if not company_id or not date_str:
        return error_response('company_id and date are required')

    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return error_response('Invalid date format. Use YYYY-MM-DD')

    all_slots = []
    for hour in range(9, 18):
        all_slots.append(f"{hour:02d}:00 - {hour:02d}:30")
        all_slots.append(f"{hour:02d}:30 - {hour+1:02d}:00")

    booked = Appointment.query.filter_by(
        company_id=company_id,
        appointment_date=query_date,
        status='pending'
    ).all()

    booked_slots = [a.time_slot for a in booked]
    available = [slot for slot in all_slots if slot not in booked_slots]

    return success_response(data={
        'date': date_str,
        'company_id': company_id,
        'all_slots': all_slots,
        'booked_slots': booked_slots,
        'available_slots': available
    })