from flask import Blueprint, render_template, redirect, url_for, jsonify, request

from project import app_errors
from project.utilities import api_utils
from project.utilities.donations_management import DonationsManagement
from project.utilities.session_helper import SessionHelper
from project.utilities.user_donation_assignment import UserDonationAssignment

# homepage blueprint definition
homepage = Blueprint('homepage', __name__, static_folder='static', static_url_path='/homepage', template_folder='templates')


# Routes
@homepage.route('/')
def index():
    return render_template('homepage.html')


@homepage.route('/homepage')
@homepage.route('/home')
def redirect_homepage():
    return redirect(url_for('.index'))


@homepage.route('/donations')
def donations():
    all_available_donations = DonationsManagement.get_all_available_donations()
    return jsonify([d.serialize() for d in all_available_donations])

@homepage.route('/donation', methods=['POST'])
def donation():
    donating_user_id = api_utils.extract_from_args(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=donating_user_id):
        raise app_errors.InvalidAPIUsage('Cannot add donation, user not logged-in',  payload={'user_id': donating_user_id})

    category_str = api_utils.extract_from_form(request, 'category')
    description = api_utils.extract_from_form(request, 'description')
    available_until_str = api_utils.extract_from_form(request, 'available_until_str')
    address = api_utils.extract_from_form(request, 'address')

    DonationsManagement.add_donation(category_str=category_str, description=description, available_until_str=available_until_str, address=address, donating_user_id=donating_user_id)
    return redirect(url_for('.donations'))


@homepage.route('/request-donation', methods=['POST'])
def request_donation():
    user_id = api_utils.extract_from_args(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=user_id):
        raise app_errors.InvalidAPIUsage('Cannot request donation, user not logged-in',  payload={'user_id': user_id})

    donation_id = api_utils.extract_from_args(request, 'donation_id')
    success = UserDonationAssignment.assign_donation_to_user(user_id=user_id, donation_id=donation_id)
    return jsonify({'request_donation_successfully': success})