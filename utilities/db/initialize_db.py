import datetime
import pathlib

import settings
from utilities import datetime_utils
from utilities.donations_management import DonationsManagement
from utilities.donations_management.donation import DonationCategory
from utilities.user_donation_assignment.user_donation_assignment import UserDonationAssignment
from utilities.users_management import UsersManagement




predefined_user_details = [
    {"username": "Yossi", "email": "yossi@gmail.com", "password": "111", "phone_number": "0542298381"},
    {"username": "Yaniv", "email": "yaniv@gmail.com", "password": "222", "phone_number": "0542298382"},
    {"username": "Gil", "email": "gil@gmail.com", "password": "333", "phone_number": "0542298383"},
    {"username": "Yaron", "email": "yaron@gmail.com", "password": "444", "phone_number": "0542298384"},
    {"username": "Galit", "email": "galit@gmail.com", "password": "555", "phone_number": "0542298385"}
]

available_until = datetime.datetime.now() + datetime.timedelta(hours=50)
predefined_donations = [
    {
        "category": DonationCategory.VEGETABLES.name,
        "description": "2 kilos of Tomato",
        "available_until": datetime_utils.convert_datetime_to_timestamp(available_until),
        "address": "some street",
        "donating_user_email": "yaniv@gmail.com",
        "donation_image_path":"tomato.jpeg"
    },
    {
        "category": DonationCategory.GRAINS.name,
        "description": "2 kilos of grains",
        "available_until": datetime_utils.convert_datetime_to_timestamp(available_until),
        "address": "some street",
        "donating_user_email": "yaniv@gmail.com",
        "donation_image_path":"grains.jpg"
    },
    {
        "category": DonationCategory.FURNITURE.name,
        "description": "2 tables",
        "available_until": datetime_utils.convert_datetime_to_timestamp(available_until),
        "address": "some street",
        "donating_user_email": "yaniv@gmail.com",
        "donation_image_path":"table.webp"
    },
    {
        "category": DonationCategory.CLOTHS.name,
        "description": "2 T-shirts",
        "available_until": datetime_utils.convert_datetime_to_timestamp(available_until),
        "address": "some street",
        "donating_user_email": "yaniv@gmail.com",
        "donation_image_path":"tshirt.jpg"
    },
]



def populate_donations():
    users = UsersManagement.get_users_from_email([d['donating_user_email'] for d in predefined_donations])
    user_id_by_email = {u.email: u.user_id for u in users}
    # donation_image_path = pathlib.Path('tomato.jpeg')

    for donation_details in predefined_donations:
        user_id = user_id_by_email[donation_details['donating_user_email']]
        DonationsManagement.add_donation(
            category_str=donation_details['category'],
            description=donation_details['description'],
            available_until_str=donation_details['available_until'],
            address=donation_details['address'],
            donating_user_id=user_id,
            donation_image_path=donation_details['donation_image_path']
        )


def populate_users():
    for user_details in predefined_user_details:
        UsersManagement.register_user(**user_details)


def delete_tables():
    UserDonationAssignment.delete_table()
    DonationsManagement.delete_table()
    UsersManagement.delete_table()

def create_tables():
    UsersManagement.create_table()
    DonationsManagement.create_table()
    UserDonationAssignment.create_table()


def populate_tables_data():
    populate_users()
    populate_donations()


def initialize_db(should_delete_tables=False):
    if should_delete_tables:
        delete_tables()
    create_tables()
    populate_tables_data()


if __name__ == '__main__':
    initialize_db()