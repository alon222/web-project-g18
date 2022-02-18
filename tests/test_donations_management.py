import datetime
import pathlib

import pytest

import app_errors, settings
from utilities.db import initialize_db
from utilities.donations_management import DonationsManagement, Donation
from utilities.donations_management.donation import DonationAvailabilityStatus, DonationCategory


class TestDonationsManagement:
    DONATION_IMAGE_PATH = str(pathlib.Path(settings.UPLOAD_FOLDER, 'tomato.jpeg'))


    def test_available_donations(self):
        initialize_db.initialize_db()
        now = datetime.datetime.now()
        all_available_donations = DonationsManagement.get_all_available_donations()
        assert len(all_available_donations) == len(initialize_db.predefined_donations)

        some_donation = all_available_donations[0]
        assert some_donation.available_until > now
        assert some_donation.donating_id and some_donation.donating_user_id

        some_time_in_past = now - datetime.timedelta(hours=5)
        DonationsManagement.update_donation(donation_id=some_donation.donating_id,
                                            available_until_str=Donation.convert_available_until_date_to_str(some_time_in_past))

        all_available_donations = DonationsManagement.get_all_available_donations()
        assert not any(d for d in all_available_donations if d.donating_id == some_donation.donating_id), 'Donation should not be available'

    def test_crud_donation(self):
        initialize_db.initialize_db()

        new_description = 'new_description'
        new_address = 'new_address'
        new_available_until =  datetime.datetime.now() - datetime.timedelta(hours=5)
        new_category = DonationCategory.CLOTHS
        new_available_status = DonationAvailabilityStatus.DELIVERED

        some_donation = DonationsManagement.get_all_available_donations()[0]

        fetched_donation = DonationsManagement.get_donation(donation_id=some_donation.donating_id)
        assert some_donation.donating_id == fetched_donation.donating_id

        DonationsManagement.update_donation(donation_id=some_donation.donating_id,
                                            available_until_str=Donation.convert_available_until_date_to_str(new_available_until),
                                            availability_status_str=new_available_status.name,
                                            category_str=new_category.name,
                                            description=new_description,
                                            address=new_address)

        initial_user_donations = DonationsManagement.get_user_donations(user_id=some_donation.donating_user_id)

        updated_donation = next(iter([d for d in initial_user_donations if d.donating_id == some_donation.donating_id]))
        assert updated_donation is not None
        assert updated_donation.donating_user_id == some_donation.donating_user_id
        assert updated_donation.description == new_description
        assert updated_donation.address == new_address
        assert Donation.convert_available_until_date_to_str(updated_donation.available_until) == Donation.convert_available_until_date_to_str(new_available_until)
        assert updated_donation.category == new_category
        assert updated_donation.availability_status == new_available_status


        with pytest.raises(app_errors.AppError) as e:
            DonationsManagement.add_donation(category_str=new_category.name, address=new_address, description=new_description, available_until_str=Donation.convert_available_until_date_to_str(new_available_until), donating_user_id=some_donation.donating_user_id, donation_image_path=self.DONATION_IMAGE_PATH)
        assert e.value.message == 'Insufficient time to pickup donation', 'Cannot add donation in the past'


        new_available_until = datetime.datetime.now() + datetime.timedelta(hours=1000)
        DonationsManagement.add_donation(category_str=new_category.name, address=new_address, description=new_description, available_until_str=Donation.convert_available_until_date_to_str(new_available_until), donating_user_id=some_donation.donating_user_id, donation_image_path=self.DONATION_IMAGE_PATH)
        user_donations_after_insertion = DonationsManagement.get_user_donations(user_id=some_donation.donating_user_id)
        assert len(user_donations_after_insertion) == len(initial_user_donations) + 1

        DonationsManagement.delete_donation(donation_id=some_donation.donating_id, donating_user_id=some_donation.donating_user_id)
        user_donations_after_deletion = DonationsManagement.get_user_donations(user_id=some_donation.donating_user_id)
        assert len(user_donations_after_deletion) == len(user_donations_after_insertion) - 1
