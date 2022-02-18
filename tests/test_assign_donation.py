from utilities.db import initialize_db
from utilities.donations_management import DonationsManagement
from utilities.donations_management.donation import DonationAvailabilityStatus
from utilities.user_donation_assignment import UserDonationAssignment
from utilities.users_management import UsersManagement


class TestDonationAssignment:

    def test_assign_donation_to_user(self):
        initialize_db.initialize_db()

        user_a, user_b = UsersManagement.get_all_users()[:2]
        donation = DonationsManagement.get_all_available_donations()[0]

        assert UserDonationAssignment.assign_donation_to_user(user_id=user_a.user_id, donation_id=donation.donating_id)
        user_donations = DonationsManagement.get_user_donations(user_id=donation.donating_user_id)
        assert len(user_donations) == 1 and user_donations[0].availability_status == DonationAvailabilityStatus.RESERVED_FOR_USER

        # reassigning
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_a.user_id, donation_id=donation.donating_id)

        # assigning to different user
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_b.user_id, donation_id=donation.donating_id)

        # non existing user / donation
        assert not UserDonationAssignment.assign_donation_to_user(user_id=100, donation_id=donation.donating_id)
        assert not UserDonationAssignment.assign_donation_to_user(user_id=user_b.user_id, donation_id=100)
