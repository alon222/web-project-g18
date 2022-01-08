import pathlib
import uuid

from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask import send_from_directory

from project import app_errors, app, settings
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


@homepage.route('/donations/<donation_image_name>')
def download_donation_image(donation_image_path: str):
    as_pathlib = pathlib.Path(donation_image_path)
    return send_from_directory(directory=str(as_pathlib.parent), path=str(as_pathlib.name))


@homepage.route('/donation/<donating_user_id>', methods=['POST'])
def donation(donating_user_id: int):
    if not SessionHelper.is_user_logged_in(user_id=donating_user_id):
        raise app_errors.InvalidAPIUsage('Cannot add donation, user not logged-in',  payload={'user_id': donating_user_id})

    category_str = api_utils.extract_from_form(request, 'category')
    description = api_utils.extract_from_form(request, 'description')
    available_until_str = api_utils.extract_from_form(request, 'available_until_str')
    address = api_utils.extract_from_form(request, 'address')
    donation_image = api_utils.extract_from_files(request, 'donation_image')

    filename = pathlib.Path(donation_image.filename)
    if filename == '' or filename.suffix not in {'png', 'jpg', 'jpeg'}:
        raise app_errors.InvalidAPIUsage('Donation image is invalid', payload={'filename': filename})

    donation_file_path = pathlib.Path(settings.UPLOAD_FOLDER, f"{uuid.uuid4()}_donation_{category_str}").with_suffix(filename.suffix)
    donation_image.save(donation_file_path)

    DonationsManagement.add_donation(category_str=category_str, description=description, available_until_str=available_until_str, address=address, donating_user_id=donating_user_id, donation_image_path=str(donation_file_path))
    return redirect(url_for('.donations'))


@homepage.route('/request-donation', methods=['POST'])
def request_donation():
    user_id = api_utils.extract_from_form(request, 'user_id')
    if not SessionHelper.is_user_logged_in(user_id=user_id):
        raise app_errors.InvalidAPIUsage('Cannot request donation, user not logged-in',  payload={'user_id': user_id})

    donation_id = api_utils.extract_from_form(request, 'donation_id')
    success = UserDonationAssignment.assign_donation_to_user(user_id=user_id, donation_id=donation_id)
    return jsonify({'request_donation_successfully': success})