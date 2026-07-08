"""
Role-Based Access Control Decorators
NO HARDCODED ROLES - Uses dynamic role checking from User model
"""
from functools import wraps
from flask import jsonify, redirect, url_for, flash, request
from flask_login import current_user, login_required


def super_admin_required(f):
    """Restrict access to Super Admin only"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'super_admin':
            if request.is_json:
                return jsonify({'success': False, 'message': 'Super Admin access required'}), 403
            flash('Super Admin access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Restrict access to Admin (Doctor) only"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            if request.is_json:
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            flash('Admin access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def patient_required(f):
    """Restrict access to Patient only"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'patient':
            if request.is_json:
                return jsonify({'success': False, 'message': 'Patient access required'}), 403
            flash('Patient access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def admin_or_super_admin_required(f):
    """Restrict access to Admin or Super Admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['admin', 'super_admin']:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            flash('Admin access required', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
