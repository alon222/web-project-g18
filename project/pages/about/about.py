import http

from flask import Blueprint, render_template, request, jsonify, url_for
from werkzeug.utils import redirect

from project import app_errors
from project.utilities import api_utils
from project.utilities.session_helper import SessionHelper
from project.utilities.users_management import UsersManagement

about = Blueprint('about', __name__, static_folder='static', static_url_path='/about', template_folder='templates')


# Routes
@about.route('/about')
def index():
    return render_template('about.html')


@about.route('/register',  methods=['POST'])
def register():
    username = api_utils.extract_from_form(request, 'username')
    email = api_utils.extract_from_form(request, 'email')
    phone_number = api_utils.extract_from_form(request, 'phone_number')
    password = api_utils.extract_from_form(request, 'password')

    registered = UsersManagement.register_user(username=username, password=password, phone_number=phone_number, email=email)
    if not registered:
        raise app_errors.InvalidAPIUsage('Failed registering user', status_code=http.HTTPStatus.CONFLICT, payload={'email': email})

    return redirect(url_for('about.login', email=email, password=password), code=http.HTTPStatus.TEMPORARY_REDIRECT)  # TODO: check this works


@about.route('/login', methods=['POST'])
def login():
    email = api_utils.extract_from_form(request, 'email')
    password = api_utils.extract_from_form(request, 'password')

    user = UsersManagement.authenticate_user(email=email, password=password)
    if user is None:
        raise app_errors.InvalidAPIUsage('User credentials incorrect', status_code=http.HTTPStatus.UNAUTHORIZED, payload={'email': email})

    SessionHelper.login_user(user)
    return jsonify(user.serialize())


@about.route('/logout', methods=['POST'])
def logout():
    user_id = api_utils.extract_from_args(request, 'user_id')
    SessionHelper.logout_user(user_id)
    return jsonify()

