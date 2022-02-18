import app_errors
from utilities.db.db_manager import dbManager
from utilities.donations_management import DonationsManagement
from utilities.donations_management.donation import DonationAvailabilityStatus


class UserDonationAssignment:

    _CREATE_TABLE_SQL = "CREATE TABLE if not exists donation_assignment" \
                        " (`id` INT AUTO_INCREMENT PRIMARY KEY," \
                        " `requested_user` INT NOT NULL," \
                        " `donation` INT NOT NULL," \
                        " FOREIGN KEY (requested_user) REFERENCES users(id), " \
                        " FOREIGN KEY (donation) REFERENCES donations(id)," \
                        " UNIQUE (donation) )"
    _DELETE_TABLE_SQL = "DROP TABLE donation_assignment"

    _INSERT_ASSIGNMENT_SQL = "INSERT IGNORE INTO donation_assignment (requested_user, donation) VALUES (%s, %s)"

    _DELETE_ASSIGNMENT_SQL = "DELETE FROM donation_assignment WHERE donation = %s"

    @classmethod
    def create_table(cls):
        result = dbManager.execute(cls._CREATE_TABLE_SQL)
        if not result:
            raise Exception('Failed creating donation_assignment table')

    @classmethod
    def assign_donation_to_user(cls, user_id: int, donation_id: int) -> bool:
        num_rows_inserted = dbManager.commit(cls._INSERT_ASSIGNMENT_SQL, (user_id, donation_id))
        if num_rows_inserted == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed assigning donation to user', payload={'user_id': user_id, 'donation_id': donation_id})

        was_assigned = num_rows_inserted == 1
        if was_assigned:
            DonationsManagement.update_donation(donation_id=donation_id, availability_status_str=DonationAvailabilityStatus.RESERVED_FOR_USER.name)

        return was_assigned

    @classmethod
    def delete_assign(cls, donation_id: int):
        rows_affected = dbManager.commit(cls._DELETE_ASSIGNMENT_SQL, args=(donation_id,))
        if rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed deleting assignment', payload={'donation_id': donation_id})

    @classmethod
    def delete_table(cls):
        result = dbManager.execute(cls._DELETE_TABLE_SQL)
        if not result:
            raise Exception('Failed deleting donation_assignment table')


