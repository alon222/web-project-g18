import hashlib
import re
from typing import Optional
## pip install phonenumbers
import phonenumbers

from app_errors import InvalidAPIUsage


class User:
    _MIN_USERNAME_LENGTH = 3
    _EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    def __init__(self, username: str, email: str, phone_number: str,  user_id: Optional[int] = None, password_plaintext: Optional[str] = None, password_hashed: Optional[str] = None):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._phone_number = phone_number
        assert bool(password_hashed) ^ bool(password_plaintext), 'Must provide either plain text password or already hashed password'
        self._password_hashed = self.hash_user_password(password_plaintext) if password_plaintext else password_hashed

    def __str__(self):
        return f'{self.username}__{self.email}'

    @staticmethod
    def hash_user_password(password_plaintext: str) -> str:
        return hashlib.sha1(password_plaintext.encode('utf-8')).hexdigest()

    @property
    def username(self) -> str:
        return self._username

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @property
    def password_hashed(self) -> Optional[str]:
        return self._password_hashed

    def validate_user_details(self):
        return self._validate_phone_number() and self._validate_username() and self._validate_email()

    def _validate_phone_number(self) -> bool:
        try:
            number = phonenumbers.parse(self.phone_number, "IL")
            if not phonenumbers.is_valid_number(number):
                raise InvalidAPIUsage(f'Invalid phone number', payload={'phone_number': self.phone_number})
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidAPIUsage(f'Invalid phone number', payload={'phone_number': self.phone_number})
        return True

    def _validate_username(self) -> bool:
        if len(self.username) < self._MIN_USERNAME_LENGTH:
            raise InvalidAPIUsage(f'Username too short', payload={'username': self.username, 'min_length': self._MIN_USERNAME_LENGTH})
        return True

    def _validate_email(self) -> bool:
        if not re.fullmatch(self._EMAIL_REGEX, self.email):
            raise InvalidAPIUsage('Email is not in the correct format', payload={'email': self.email})
        return True


    def serialize(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number
        }
