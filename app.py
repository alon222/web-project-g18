
from flask import Flask
import settings

#############
import http

from flask import  jsonify, url_for


from app_errors import AppError


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


@app.errorhandler(AppError)
def app_error(e: AppError):
    return jsonify(e.to_dict()), e.status_code


@app.errorhandler(Exception)
def unhandled_error(e: Exception):
    return jsonify(dict(error=e)), http.HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run(debug=True)