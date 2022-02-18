import pathlib
import uuid

from flask import jsonify, session, Blueprint, render_template, redirect, url_for,request

# homepage blueprint definition
import settings
from utilities import api_utils, datetime_utils
from utilities.donations_management import DonationsManagement
from utilities.donations_management.donation import DonationAvailabilityStatus
from utilities.session_helper import SessionHelper
from utilities.user_donation_assignment import UserDonationAssignment
from utilities.users_management import UsersManagement





homepage = Blueprint('homepage', __name__, static_folder='static', static_url_path='/homepage', template_folder='templates')


# Routes
@homepage.route('/')
def index():
    #get all avilable donations and display on home page
    all_available_donations = DonationsManagement.get_all_available_donations()
    res=[d.serialize() for d in all_available_donations]
    return render_template('homepage.html',res=res)


@homepage.route('/homepage')
@homepage.route('/home')
def redirect_homepage():
    return redirect(url_for('homepage.index'))


@homepage.route('/donation', methods=['POST'])
def donation():
    # if not SessionHelper.is_user_logged_in(user_id=donating_user_id):
    #     raise app_errors.InvalidAPIUsage('Cannot add donation, user not logged-in',  payload={'user_id': donating_user_id})
    user = session['user']
    donating_user_id = user['user_id']
    category_str = api_utils.extract_from_form(request, 'category')
    description = api_utils.extract_from_form(request, 'product')
    available_until_date_str = api_utils.extract_from_form(request, 'avail_date')
    available_until_time_str = api_utils.extract_from_form(request, 'avail_time')
    available_until_str="{} {}".format(available_until_date_str, available_until_time_str)

    street = api_utils.extract_from_form(request, 'street')
    number = api_utils.extract_from_form(request, 'number')
    city = api_utils.extract_from_form(request, 'city')
    #pass adress as string
    address = "{} {}, {}".format(street, number, city)
    donation_image = api_utils.extract_from_form(request, 'donation_image')
    print(donation_image)
    #filename = pathlib.Path(donation_image.filename)
    # # if filename == '' or filename.suffix not in {'png', 'jpg', 'jpeg'}:
    # #     raise app_errors.InvalidAPIUsage('Donation image is invalid', payload={'filename': filename})
    #
    #donation_file_path = pathlib.Path(settings.UPLOAD_FOLDER, f"{uuid.uuid4()}_donation_{category_str}").with_suffix(filename.suffix)
    #donation_image.save(donation_file_path)

    DonationsManagement.add_donation(category_str=category_str, description=description, available_until_str=available_until_str, address=address,donating_user_id=donating_user_id, donation_image_path=str(donation_image))
    return redirect(url_for('.donations'))


@homepage.route('/request-donation', methods=['POST','get'])
def request_donation():
    # requesting_user_id = api_utils.extract_from_args(request, 'requesting_user_id') # TODO:Alon delete if not using
    # if not SessionHelper.is_user_logged_in(user_id=requesting_user_id):
    #     raise app_errors.InvalidAPIUsage('Cannot request donation, user not logged-in',  payload={'user_id': requesting_user_id})
    user = session['user']
    requesting_user_id = user['user_id']
    user_name = user['username']
    donation_id = api_utils.extract_from_args(request, 'donation_id')
    res = DonationsManagement.get_donation(donation_id)
    UserDonationAssignment.assign_donation_to_user(user_id=requesting_user_id, donation_id=donation_id)
    return render_template('order.html', res=res.serialize(), user_name=user_name)

##### this is authantication section#######

@homepage.route('/register',  methods=['POST'])## aproved
def register():
    username = api_utils.extract_from_form(request, 'user_signup')
    email = api_utils.extract_from_form(request, 'Email')
    phone_number = api_utils.extract_from_form(request, 'phone')
    password = api_utils.extract_from_form(request, 'password_signup')

    registered = UsersManagement.register_user(username=username, password=password, phone_number=phone_number, email=email)
    # if not registered:
    #     raise app_errors.InvalidAPIUsage('Failed registering user', status_code=http.HTTPStatus.CONFLICT, payload={'email': email})
    user = UsersManagement.authenticate_user(email=email, password=password)
    # if user is None:
    #     raise app_errors.InvalidAPIUsage('User credentials incorrect', status_code=http.HTTPStatus.UNAUTHORIZED, payload={'email': email})
    #
    SessionHelper.login_user(user)
    return redirect('/')


@homepage.route('/login', methods=['POST'])##aproved
def login():
    email = api_utils.extract_from_form(request, 'email')
    password = api_utils.extract_from_form(request, 'password')

    user = UsersManagement.authenticate_user(email=email, password=password)
    # if user is None:
    #     raise app_errors.InvalidAPIUsage('User credentials incorrect', status_code=http.HTTPStatus.UNAUTHORIZED, payload={'email': email})

    SessionHelper.login_user(user)
    return redirect('/')


@homepage.route('/logout')##aproved
def logout():
    # user=session['user']
    # user_id=str(user["user_id"])
    # user_id = api_utils.extract_from_args(request, 'user_id')##check if we can fix session helpers
    # SessionHelper.logout_user(user_id=user_id)
    session.clear()
    return redirect('/')