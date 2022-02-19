from typing import List, Optional

import app_errors
from utilities.db.db_manager import dbManager
from .user import User

class UsersManagement:
    _CREATE_TABLE_SQL = "CREATE TABLE if not exists users" \
                        " (`id` INT AUTO_INCREMENT PRIMARY KEY," \
                        " `username` varchar(255) NOT NULL," \
                        " `email` varchar(255) UNIQUE KEY NOT NULL," \
                        " `phone_number` varchar(255) UNIQUE KEY NOT NULL," \
                        "`password` varchar(255) NOT NULL)"
    _DELETE_TABLE_SQL = "DROP TABLE users;"
    _INSERT_USER_SQL = "INSERT IGNORE INTO users (username, email, phone_number, password) VALUES (%s, %s, %s, %s)"
    _GET_ALL_USERS_SQL = "SELECT * FROM users"
    _GET_USERS_BY_EMAIL_SQL = """SELECT * FROM users WHERE email IN (%s);"""
    _GET_USERS_BY_EMAIL_AND_PASSWORD_SQL = """SELECT * FROM users WHERE email = %s AND password = %s ;"""
    _DELETE_USER_SQL = "DELETE FROM users WHERE id = %s; "
    _UPDATE_USER_SQL = """UPDATE users SET username = %s , email = %s, phone_number = %s , password = %s WHERE id = %s; """
    _UPDATE_USER_SQL_without = """UPDATE users SET username = %s , email = %s, phone_number = %s WHERE id = %s; """
    _GET_USERS_BY_USERID = """SELECT * FROM users WHERE id = %s;"""

    @classmethod
    def create_table(cls):
        result = dbManager.execute(cls._CREATE_TABLE_SQL)
        if not result:
            raise Exception('Failed creating users table')

    @classmethod
    def delete_table(cls):
        result = dbManager.execute(cls._DELETE_TABLE_SQL)
        if not result:
            raise Exception('Failed deleting users table')

    @classmethod
    def register_user(cls, username: str, email: str, password: str, phone_number: str) -> bool:
        user = User(username=username, email=email, password_plaintext=password, phone_number=phone_number)
        user.validate_user_details()
        num_rows_inserted = dbManager.commit(
            cls._INSERT_USER_SQL,
            (user.username, user.email, user.phone_number, user.password_hashed)
        )
        if num_rows_inserted == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed registering user', payload={'email': email})

        if num_rows_inserted == 0:
            raise app_errors.InvalidAPIUsage('User with this info already exists')

        return True

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        rows_affected = dbManager.commit(cls._DELETE_USER_SQL, (user_id, ))
        if rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed deleting user', payload={'user_id': user_id})
        return True

    @classmethod
    def get_all_users(cls) -> List[User]:
        raw_users_details = dbManager.fetch(cls._GET_ALL_USERS_SQL)
        return cls._get_users_from_raw_details(raw_users_details)

    @classmethod
    def get_users_from_email(cls, users_emails: List[str]) -> List[User]:
        emails_to_search = ','.join({f"'{email}'" for email in users_emails})
        raw_users_details = dbManager.fetch(cls._GET_USERS_BY_EMAIL_SQL % emails_to_search)
        return cls._get_users_from_raw_details(raw_users_details)

    @classmethod
    def get_user_from_email(cls, email: str) -> Optional[User]:
        users = cls.get_users_from_email([email])
        return users[0] if users else None

    @classmethod
    def _get_users_from_raw_details(cls, raw_users_details) -> List[User]:
        if isinstance(raw_users_details, bool) and not raw_users_details:
            raise app_errors.AppError('Failed fetching users')

        if not raw_users_details:
            return []

        return [
            User(user_id=d.id, username=d.username, email=d.email, phone_number=d.phone_number, password_hashed=d.password)
            for d in raw_users_details
        ]

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> Optional[User]:
        raw_users_details = dbManager.fetch(
            cls._GET_USERS_BY_EMAIL_AND_PASSWORD_SQL,
            (email, User.hash_user_password(password))
        )
        users = cls._get_users_from_raw_details(raw_users_details)
        return users[0] if users else None

    @classmethod
    def update_user_info(cls, user_id: int, username: str, password: str, phone_number: str, email: str):
        user = User(user_id=user_id, username=username, email=email, password_plaintext=password, phone_number=phone_number)
        user.validate_user_details()

        num_rows_affected = dbManager.commit(
            cls._UPDATE_USER_SQL,
            (user.username, user.email, user.phone_number, user.password_hashed, user.user_id)
        )

        if num_rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed updating user info', payload={'user_id': user_id})


    @classmethod
    def update_user_info_without(cls, user_id: int, username: str, phone_number: str, email: str):
        num_rows_affected = dbManager.commit(
            cls._UPDATE_USER_SQL_without,
            (username, email, phone_number, user_id)
        )

        if num_rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed updating user info', payload={'user_id': user_id})


    @classmethod
    def get_user_by_id(cls, user_id: int):
        raw_user_details = dbManager.fetch(cls._GET_USERS_BY_USERID, (user_id, ))
        users = cls._get_users_from_raw_details(raw_user_details)
        if len(users) == 0:
            raise app_errors.AppError('donating user not found')
        return users[0]