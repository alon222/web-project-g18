import http

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from project import app_errors
from project.utilities import api_utils
from project.utilities.session_helper import SessionHelper

from project.utilities.users_management import UsersManagement


# edit_account blueprint definition
edit_account = Blueprint('edit_account', __name__, static_folder='static', static_url_path='/edit-account', template_folder='templates')


# Routes
@edit_account.route('/edit-account', methods=['GET', 'POST'])
def edit_account():
    user_id = api_utils.extract_from_args(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=user_id):
        raise app_errors.InvalidAPIUsage('User not logged-in', payload={'user_id': user_id})

    if request.method == 'GET':
        return render_template('edit-account.html')

    elif request.method == 'POST':
        email = api_utils.extract_from_form(request, 'email')
        username = api_utils.extract_from_form(request, 'username')
        password = api_utils.extract_from_form(request, 'password')
        phone_number = api_utils.extract_from_form(request, 'phone_number')
        UsersManagement.update_user_info(user_id=user_id, username=username, password=password, phone_number=phone_number, email=email)
        return redirect(url_for('about.login', email=email, password=password), code=http.HTTPStatus.TEMPORARY_REDIRECT)  # TODO: check this works

