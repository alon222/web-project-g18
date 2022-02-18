import sys

from flask import Flask, session
import settings

#############
import http

from flask import Blueprint, render_template, request, jsonify, url_for
from werkzeug.utils import redirect

from utilities import api_utils
from utilities.donations_management import DonationsManagement
from utilities.session_helper import SessionHelper
from utilities.user_donation_assignment import UserDonationAssignment
from utilities.users_management import UsersManagement

###### App setup

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

# ###### Pages
 ## Homepage
from pages.homepage.homepage import homepage
app.register_blueprint(homepage)

# ## About
from pages.about.about import about
app.register_blueprint(about)

# contact page
from pages.contact.contact import contact
app.register_blueprint(contact)
#
# ## Catalog
from pages.myaccount.myaccount import myaccount
app.register_blueprint(myaccount)
#
# ## Page error handlers
from pages.page_error_handlers.page_error_handlers import page_error_handlers
app.register_blueprint(page_error_handlers)
#
#
# ###### Components
# ## Main menu
from components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)


# #### project routes####
#
# @app.route('/register',  methods=['POST'])## aproved
# def register():
#     username = api_utils.extract_from_form(request, 'username')
#     email = api_utils.extract_from_form(request, 'email')
#     phone_number = api_utils.extract_from_form(request, 'phone_number')
#     password = api_utils.extract_from_form(request, 'password')
#
#     registered = UsersManagement.register_user(username=username, password=password, phone_number=phone_number, email=email)
#     # if not registered:
#     #     raise app_errors.InvalidAPIUsage('Failed registering user', status_code=http.HTTPStatus.CONFLICT, payload={'email': email})
#     user = UsersManagement.authenticate_user(email=email, password=password)
#     # if user is None:
#     #     raise app_errors.InvalidAPIUsage('User credentials incorrect', status_code=http.HTTPStatus.UNAUTHORIZED, payload={'email': email})
#     #
#     SessionHelper.login_user(user)
#     return redirect('/')
#
# @app.route('/login', methods=['POST'])##aproved
# def login():
#     email = api_utils.extract_from_form(request, 'email')
#     password = api_utils.extract_from_form(request, 'password')
#
#     user = UsersManagement.authenticate_user(email=email, password=password)
#     # if user is None:
#     #     raise app_errors.InvalidAPIUsage('User credentials incorrect', status_code=http.HTTPStatus.UNAUTHORIZED, payload={'email': email})
#
#     SessionHelper.login_user(user)
#     return jsonify(user.serialize())
#
# @app.route('/')
# def home():
#     # user=SessionHelper._get_user_from_session()
#     # userid=user.user_id
#     # userid=SessionHelper.is_user_logged_in('7')
#     if session.get("user")==None:
#         return render_template("test.html")
#     user=session['user']
#     return render_template("test.html", user=user)
#
# @app.route('/logout')##aproved
# def logout():
#     user=session['user']
#     user_id=str(user["user_id"])
#     # user_id = api_utils.extract_from_args(request, 'user_id')##check if we can fix session helpers
#     # SessionHelper.logout_user(user_id=user_id)
#     session.clear()
#     return redirect('/')
#
# ## homepage
# @app.route('/donations')##aproved
# def donations():
#     all_available_donations = DonationsManagement.get_all_available_donations()
#     return jsonify([d.serialize() for d in all_available_donations])
#
# @app.route('/request-donation/<requesting_user_id>', methods=['POST'])## APROVED
# def request_donation(requesting_user_id: int):
#     # if not SessionHelper.is_user_logged_in(user_id=requesting_user_id):
#     #     raise app_errors.InvalidAPIUsage('Cannot request donation, user not logged-in',  payload={'user_id': requesting_user_id})
#
#     donation_id = api_utils.extract_from_form(request, 'donation_id')
#     success = UserDonationAssignment.assign_donation_to_user(user_id=requesting_user_id, donation_id=donation_id)
#     ## change status to reserved TODO: add GET DONATION BY DONATION ID
#     DonationsManagement.update_donation(donation_id=donation_id, donating_user_id=7, availability_status_str="RESERVED_FOR_USER")
#     return jsonify({'request_donation_successfully': success})
#
# ### my account ##
# @app.route('/my-account/donations')
# def userdonations():
#     user_id = api_utils.extract_from_args(request, 'user_id')
#     # if not SessionHelper.is_user_logged_in(user_id=user_id):
#     #     raise app_errors.InvalidAPIUsage('User not logged-in', payload={'user_id': user_id})
#
#     user_donations = DonationsManagement.get_user_donations(user_id=user_id)
#     return jsonify([d.serialize() for d in user_donations])
#
# # methods=['POST']
# @app.route('/my-account/donation')
# def donation():
#     user_id = api_utils.extract_from_args(request, 'user_id')
#     # if not SessionHelper.is_user_logged_in(user_id=user_id):
#     #     raise app_errors.InvalidAPIUsage('User not logged-in', payload={'user_id': user_id})
#
#     donation_id = api_utils.extract_from_args(request, 'donation_id')
#     http_method = api_utils.extract_from_args(request, '_method')
#     if http_method == 'DELETE':## this case is not working!!!
#         DonationsManagement.delete_donation(donation_id=donation_id, donating_user_id=user_id)
#     elif http_method == 'PUT':
#         availability_status = api_utils.extract_from_args(request, 'availability_status')
#         DonationsManagement.update_donation(donation_id=donation_id, donating_user_id=user_id, availability_status_str=availability_status)
#
#     return redirect(url_for('.donations'))


#######
if __name__ == '__main__':
    app.run(debug=True)