from flask import Blueprint, render_template, request, jsonify, url_for
from werkzeug.utils import redirect

from project import app_errors
from project.utilities import api_utils
from project.utilities.donations_management import DonationsManagement
from project.utilities.session_helper import SessionHelper

# my_account blueprint definition
my_account = Blueprint('my_account', __name__, static_folder='static', static_url_path='/my-account', template_folder='templates')


# Routes
@my_account.route('/my-account/')
def index():
    return render_template('my_account.html')



@my_account.route('/my-account/donations')
def donations():
    user_id = api_utils.extract_from_args(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=user_id):
        raise app_errors.InvalidAPIUsage('User not logged-in', payload={'user_id': user_id})

    user_donations = DonationsManagement.get_user_donations(user_id=user_id)
    return jsonify([d.serialize() for d in user_donations])


@my_account.route('/my-account/donation', methods=['POST'])
def donation():
    user_id = api_utils.extract_from_args(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=user_id):
        raise app_errors.InvalidAPIUsage('User not logged-in', payload={'user_id': user_id})

    donation_id = api_utils.extract_from_args(request, 'donation_id')
    http_method = api_utils.extract_from_form(request, '_method')
    if http_method == 'DELETE':
        DonationsManagement.delete_donation(donation_id=donation_id, donating_user_id=user_id)
    elif http_method == 'PUT':
        availability_status = api_utils.extract_from_form(request, 'availability_status')
        DonationsManagement.update_donation(donation_id=donation_id, donating_user_id=user_id, availability_status_str=availability_status)

    return redirect(url_for('.donations'))

