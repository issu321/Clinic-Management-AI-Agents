"""
Main Routes - Developer Branding Page & Real-time Reference Data APIs
NO HARDCODED VALUES - All dynamic from standard libraries
"""
from flask import Blueprint, render_template, jsonify, url_for
import pytz
import pycountry

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing Page / Developer Branding Page
    PLACEHOLDER FOR FRONTEND: app/templates/index.html
    - Use {{ developer.name }} for "Mohammed Usman"
    - Use {{ developer.github }} for "issu321"
    - Use {{ developer.portfolio }} for "https://issu321.github.io/issu321"
    - Use {{ developer.email }} for "jaafreeusman@gmail.com"
    - Use {{ developer.tagline }} for "Made Easy for Doctors Worldwide"
    - Use {{ developer.software_name }} for "ClinicPro Management System"
    - Theme: Premium glassy blur effects, classy dark gradient
    - Buttons: "Login", "Register as Doctor", "Register as Patient"
    """
    developer_info = {
        'name': 'Mohammed Usman',
        'github': 'issu321',
        'portfolio': 'https://issu321.github.io/issu321',
        'email': 'jaafreeusman@gmail.com',
        'tagline': 'Made Easy for Doctors Worldwide',
        'software_name': 'ClinicPro Management System'
    }
    return render_template('index.html', developer=developer_info)


@main_bp.route('/api/timezones')
def get_timezones():
    """Return REAL timezones from pytz library - NO HARDCODING"""
    timezones = sorted(pytz.common_timezones)
    return jsonify({
        'success': True,
        'data': timezones,
        'count': len(timezones)
    })


@main_bp.route('/api/currencies')
def get_currencies():
    """Return REAL currencies from pycountry ISO 4217 standard - NO HARDCODING
    Returns: [{"code": "USD", "name": "US Dollar", "numeric": "840"}, ...]
    """
    currencies = []
    for currency in pycountry.currencies:
        currencies.append({
            'code': currency.alpha_3,
            'name': currency.name,
            'numeric': currency.numeric
        })
    currencies = sorted(currencies, key=lambda x: x['code'])
    return jsonify({
        'success': True,
        'data': currencies,
        'count': len(currencies)
    })


@main_bp.route('/api/countries')
def get_countries():
    """Return REAL countries from pycountry ISO 3166 standard - NO HARDCODING"""
    countries = []
    for country in pycountry.countries:
        countries.append({
            'code': country.alpha_2,
            'name': country.name,
            'alpha_3': country.alpha_3
        })
    countries = sorted(countries, key=lambda x: x['name'])
    return jsonify({
        'success': True,
        'data': countries,
        'count': len(countries)
    })
