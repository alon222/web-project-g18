from flask import Blueprint, render_template, request

# about blueprint definition
from utilities import api_utils, mail_utils

contact = Blueprint('contact', __name__, static_folder='static', static_url_path='/contact', template_folder='templates')


@contact.route('/contact-us', methods=['POST','get'])
@contact.route('/contact', methods=['POST','get'])
def index():
    if request.method == 'GET':
        return render_template('contact.html')

    elif request.method == 'POST':
        email = api_utils.extract_from_form(request, 'email')
        subject = api_utils.extract_from_form(request, 'subject')
        message = api_utils.extract_from_form(request, 'message')
        mail_utils.send_mail(from_email=email, subject=subject, message=message)
        return render_template('contact.html', sent_email=True)