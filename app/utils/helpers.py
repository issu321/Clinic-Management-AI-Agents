"""
Helper Functions - File Uploads, JSON Responses, Validations
NO HARDCODED VALUES - All dynamic
"""
import os
import secrets
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from flask import current_app, jsonify, request


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file, folder=''):
    """Save uploaded file with secure random filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        random_name = secrets.token_hex(8) + '.' + ext
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, random_name)
        file.save(file_path)
        return os.path.join('uploads', folder, random_name).replace('\\', '/')
    return None


def is_ajax_request():
    """Detect if request is an AJAX/fetch call (not a regular form submission)"""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def success_response(data=None, message='Success'):
    """Standard success JSON response"""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response)


def error_response(message='Error occurred', status_code=400):
    """Standard error JSON response"""
    response = {'success': False, 'message': message}
    return jsonify(response), status_code


def format_currency_amount(amount, currency_code):
    """Format amount with selected currency - NO HARDCODED SYMBOLS
    Uses the currency code stored during company registration
    """
    if amount is None:
        amount = 0.0
    return f"{currency_code} {amount:,.2f}"