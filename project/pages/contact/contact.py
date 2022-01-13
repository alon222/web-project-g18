from flask import Blueprint, render_template, request

from project.utilities import api_utils, mail_utils

# contact blueprint definition
contact = Blueprint('contact', __name__, url_prefix='contact', static_folder='static', static_url_path='/contact', template_folder='templates')


# Routes
@contact.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')

    elif request.method == 'POST':
        email = api_utils.extract_from_form(request, 'email')
        subject = api_utils.extract_from_form(request, 'subject')
        message = api_utils.extract_from_form(request, 'message')
        mail_utils.send_mail(from_email=email, subject=subject, message=message)
        return render_template('contact.html', sent_email=True)

