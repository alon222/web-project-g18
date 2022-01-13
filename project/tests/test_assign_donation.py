from project.utilities.db import initialize_db
from project.utilities.donations_management import DonationsManagement
from project.utilities.user_donation_assignment import UserDonationAssignment
from project.utilities.users_management import UsersManagement


class TestDonationAssignment:

    def test_assign_donation_to_user(self):
        initialize_db.initialize_db()

        user_a, user_b = UsersManagement.get_all_users()[:2]
        donation = DonationsManagement.get_all_available_donations()[0]

        assert UserDonationAssignment.assign_donation_to_user(user_id=user_a.user_id, donation_id=donation.donating_id)

        # reassigning
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_a.user_id, donation_id=donation.donating_id)

        # assigning to different user
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_b.user_id, donation_id=donation.donating_id)

        # non existing user / donation
        assert not UserDonationAssignment.assign_donation_to_user(user_id=100, donation_id=donation.donating_id)
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_b.user_id, donation_id=100)
