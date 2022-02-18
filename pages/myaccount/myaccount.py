from flask import Blueprint, render_template, request, redirect, url_for,session

# catalog blueprint definition
import app_errors
from utilities import api_utils
from utilities.donations_management import DonationsManagement
from utilities.session_helper import SessionHelper
from utilities.user_donation_assignment import UserDonationAssignment
from utilities.users_management import UsersManagement

myaccount = Blueprint('myaccount', __name__, static_folder='static', static_url_path='/myaccount', template_folder='templates')

@myaccount.route('/my-account')
@myaccount.route('/myaccount')
def donations():
    if session.get('user') is None:
        raise app_errors.InvalidAPIUsage('User not logged-in')

    user = session['user']
    user_id = user['user_id']
    user_donations = DonationsManagement.get_user_donations(user_id=user_id)
    donations = [d.serialize() for d in user_donations]
    return render_template('myaccount.html',res=donations)




@myaccount.route('/my-account/donation', methods=['POST'])
def donation():
    user = session['user']
    user_id = user['user_id']
    donation_id = api_utils.extract_from_form(request, 'donation_id')
    http_method = api_utils.extract_from_form(request, '_method')
    if http_method == 'DELETE':
        DonationsManagement.delete_donation(donation_id=donation_id, donating_user_id=user_id)
    elif http_method == 'PUT':
        availability_status = api_utils.extract_from_form(request, 'status')
        if availability_status == 'AVAILABLE': ## remove assignment
            print(donation_id)
            UserDonationAssignment.delete_assign(donation_id=donation_id)
        DonationsManagement.update_donation(donation_id=donation_id, availability_status_str=availability_status)

    return redirect(url_for('.donations'))



@myaccount.route('/my-account/edit', methods=['GET', 'POST'])
@myaccount.route('/myaccount/edit', methods=['GET', 'POST'])
def edit_account():

    if session.get('user') is None:
        raise app_errors.InvalidAPIUsage('User not logged-in')
    user = session['user']
    if request.method == 'GET':
        return render_template('my-account-edit.html', user=user)

    elif request.method == 'POST':
        email = api_utils.extract_from_form(request, 'edit_email')
        username = api_utils.extract_from_form(request, 'edit_username')
        phone_number = api_utils.extract_from_form(request, 'edit_phone_number')
        ### if user dont want to edit password just the personal data we will create diffrent path
        if request.form['edit_password'] != '':
            password = api_utils.extract_from_form(request, 'edit_password')
            UsersManagement.update_user_info(user_id=user['user_id'], username=username, password=password, phone_number=phone_number, email=email)
        UsersManagement.update_user_info_without(user_id = user['user_id'], username=username, phone_number = phone_number, email=email)
        ## update user session to new data without loging in again
        user = UsersManagement.get_user_from_email(email)
        SessionHelper.login_user(user)
        return redirect('/')