import pytest

import app_errors
from utilities.db import initialize_db
from utilities.users_management import UsersManagement, User


class TestUsersManagement:

    def test_crud_user(self):
        initialize_db.initialize_db()

        all_users = UsersManagement.get_all_users()
        assert len(all_users) == len(initialize_db.predefined_user_details)

        username = 'test'
        password = 'test'
        email = 'blabla@gmail.com'
        phone_number = '0542298956'

        assert UsersManagement.register_user(username=username, password=password, email=email, phone_number=phone_number)
        assert len(UsersManagement.get_all_users()) == len(all_users) + 1

        user = UsersManagement.get_user_from_email(email)
        assert user and user.username == username and user.password_hashed == User.hash_user_password(password) and user.phone_number == phone_number and user.email == email


        with pytest.raises(app_errors.AppError) as e:
            UsersManagement.register_user(username=username, password=password, email='fake', phone_number=phone_number)
        assert e.value.message == 'Email is not in the correct format'

        with pytest.raises(app_errors.AppError) as e:
            UsersManagement.register_user(username=username, password=password, email=email, phone_number='not a phone number')
        assert e.value.message == 'Invalid phone number'

        with pytest.raises(app_errors.AppError) as e:
            UsersManagement.register_user(username='c', password=password, email=email, phone_number=phone_number)
        assert e.value.message == 'Username too short'


        new_username = 'new'
        new_password = 'new'
        new_email = 'new@gmail.com'
        new_phone_number = '0542298959'

        UsersManagement.update_user_info(user_id=user.user_id, username=new_username, email=new_email, password=new_password, phone_number=new_phone_number)
        updated_user = UsersManagement.get_user_from_email(new_email)
        assert updated_user and updated_user.user_id == user.user_id and updated_user.username == new_username and updated_user.password_hashed == User.hash_user_password(new_password) and updated_user.email == new_email and updated_user.phone_number == new_phone_number

        UsersManagement.delete_user(user_id=updated_user.user_id)
        assert len(UsersManagement.get_all_users()) == len(all_users)
        assert UsersManagement.get_user_from_email(new_email) is None

    def test_authenticate_user(self):
        initialize_db.initialize_db()

        password = 'test'
        email = f'blabla@gmail.com'

        assert UsersManagement.register_user(username='test', password=password, email=email, phone_number='0542298956')

        assert UsersManagement.authenticate_user(email=email, password=password) is not None
        assert UsersManagement.authenticate_user(email=email, password='wrong_password') is None