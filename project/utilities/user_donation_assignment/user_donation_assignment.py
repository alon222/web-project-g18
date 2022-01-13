from project import app_errors
from project.utilities.db.db_manager import dbManager

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

        return num_rows_inserted == 1

    @classmethod
    def delete_table(cls):
        result = dbManager.execute(cls._DELETE_TABLE_SQL)
        if not result:
            raise Exception('Failed deleting donation_assignment table')


