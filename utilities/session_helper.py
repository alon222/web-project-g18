from typing import Optional

from flask import session

from utilities.users_management import User


class SessionHelper:
    _USER_SESSION_KEY = 'user'

    @classmethod
    def login_user(cls, user: User):
        session[cls._USER_SESSION_KEY] = user.serialize()

    @classmethod
    def logout_user(cls, user_id: str):
        if cls.is_user_logged_in(user_id):
            session.pop(cls._USER_SESSION_KEY, None)

    @classmethod
    def is_user_logged_in(cls, user_id) -> bool:
        user = cls._get_user_from_session()
        if user is not None and str(user.user_id) == user_id:
            return True
        return False

    @classmethod
    def _get_user_from_session(cls) -> Optional[User]:
        serialized_user: dict = session.get(cls._USER_SESSION_KEY)
        if serialized_user is None:
            return None

        user = User(**serialized_user)
        return user

