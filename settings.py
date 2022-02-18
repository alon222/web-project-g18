import os
import pathlib

from dotenv import load_dotenv
load_dotenv()

# Secret key setting from .env for Flask sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

# DB base configuration from .env for modularity and security reasons
DB = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}


# TODO: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
# Set up gmail account using this instructions
CONTACT_EMAIL = os.environ['CONTACT_EMAIL']
CONTACT_EMAIL_PASSWORD = os.environ['CONTACT_EMAIL_PASSWORD']

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']


UPLOAD_FOLDER = pathlib.Path(pathlib.Path(os.path.realpath(__file__)).parent, 'static', 'uploaded_donation_images')
assert UPLOAD_FOLDER.is_dir()

