import http

from flask import Flask, jsonify

from project import settings
from project.app_errors import AppError


def create_app(config_filename='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
    register_blueprints(app)
    initialize_error_handlers(app)
    return app


def register_blueprints(app):
    ###### Pages

    ## About
    from project.pages.about.about import about
    app.register_blueprint(about)

    ## Contact
    from project.pages.contact.contact import contact
    app.register_blueprint(contact)

    ## EditAccount
    from project.pages.edit_account.edit_account import edit_account
    app.register_blueprint(edit_account)

    ## Homepage
    from project.pages.homepage.homepage import homepage
    app.register_blueprint(homepage)

    ## MyAccount
    from project.pages.my_account.my_account import my_account
    app.register_blueprint(my_account)



def initialize_error_handlers(app):
    @app.errorhandler(AppError)
    def app_error(e: AppError):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(Exception)
    def unhandled_error(e: Exception):
        return jsonify(dict(error=e)), http.HTTPStatus.INTERNAL_SERVER_ERROR


my_app = create_app()


if __name__ == '__main__':
    my_app.run(debug=True)