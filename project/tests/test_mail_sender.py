from project.utilities import mail_utils


class TestMailSender:

    def test_send_mail(self):
        # NOTE: in order to run locally in debug mode run the following command from the Terminal app:
        #  Linux / MAC: sudo python -m smtpd -c DebuggingServer -n
        #  other: https://www.dev2qa.com/python-built-in-local-smtp-server-example/
        #  and change in the env file the parameters to point to the TEST host + port
        mail_utils.send_mail(from_email="user@gmail.com", subject='test subject', message='blabla', use_ssl=False)

