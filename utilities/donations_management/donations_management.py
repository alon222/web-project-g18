from typing import List
from utilities.db.db_manager import dbManager
from utilities import datetime_utils
import app_errors

from .donation import Donation, DonationCategory, DonationAvailabilityStatus


class DonationsManagement:
    _statues = ','.join([f"'{s.name}'" for s in DonationAvailabilityStatus])
    _CREATE_TABLE_SQL = "CREATE TABLE if not exists donations" \
                        " (`id` INT AUTO_INCREMENT PRIMARY KEY," \
                        " `category` varchar(255) NOT NULL," \
                        " `description` varchar(255) NOT NULL," \
                        " `available_until` TIMESTAMP NOT NULL," \
                        " `address` varchar(255) NOT NULL," \
                        "`donating_user` INT NOT NULL," \
                        "`donation_image_path` varchar(255) NOT NULL," \
                        f"`availability_status` ENUM({_statues}) NOT NULL DEFAULT '{DonationAvailabilityStatus.AVAILABLE.name}'," \
                        " FOREIGN KEY (donating_user) REFERENCES users(id) )"

    _DELETE_TABLE_SQL = "DROP TABLE donations;"

    _INSERT_DONATION_SQL = "INSERT INTO donations (category, description, available_until, address, donating_user, donation_image_path) VALUES (%s, %s, %s, %s, %s, %s)"
    _GET_ALL_AVAILABLE_DONATIONS_SQL = f"SELECT * FROM donations WHERE availability_status = %s AND available_until > now()"
    _GET_ALL_USER_DONATIONS_SQL = "SELECT * FROM donations WHERE donating_user = %s;"
    _GET_DONATION_SQL = "SELECT * FROM donations WHERE id = %s;"
    _DELETE_DONATION_SQL = "DELETE FROM donations WHERE id = %s AND donating_user = %s;"

    @classmethod
    def create_table(cls):
        result = dbManager.execute(cls._CREATE_TABLE_SQL)
        if not result:
            raise Exception('Failed creating users table', result)

    @classmethod
    def delete_table(cls):
        result = dbManager.execute(cls._DELETE_TABLE_SQL)
        if not result:
            raise Exception('Failed deleting donations table')

    @classmethod
    def get_all_available_donations(cls) -> List[Donation]:
        raw_donations_details = dbManager.fetch(cls._GET_ALL_AVAILABLE_DONATIONS_SQL, (DonationAvailabilityStatus.AVAILABLE.name, ))
        return cls._get_from_raw_donations(raw_donations_details)

    @classmethod
    def get_user_donations(cls, user_id: int) -> List[Donation]:
        raw_donations_details = dbManager.fetch(cls._GET_ALL_USER_DONATIONS_SQL, (user_id, ))
        return cls._get_from_raw_donations(raw_donations_details)

    @classmethod
    def get_donation(cls, donation_id: int) -> Donation:
        raw_donations_details = dbManager.fetch(cls._GET_DONATION_SQL, (donation_id, ))
        donations = cls._get_from_raw_donations(raw_donations_details)
        if len(donations) == 0:
            raise app_errors.AppError('Donation not found', payload={'donation_id': donation_id})
        return donations[0]

    @classmethod
    def _get_from_raw_donations(cls, raw_donations_details) -> List[Donation]:
        if isinstance(raw_donations_details, bool) and not raw_donations_details:
            raise app_errors.AppError('Failed fetching donations')

        if not raw_donations_details:
            return []

        return [
            Donation(
                donation_id=d.id, category=DonationCategory.get_from_str(d.category), description=d.description,
                available_until=d.available_until, address=d.address, donating_user_id=d.donating_user,
                availability_status=DonationAvailabilityStatus.get_from_str(d.availability_status),
                donation_image_path=d.donation_image_path,
            ) for d in raw_donations_details
        ]

    @classmethod
    def add_donation(cls, category_str: str, description: str, available_until_str: str, address: str, donating_user_id: int, donation_image_path: str):
        category = cls._parse_or_raise_category(category_str)
        available_until = cls._parse_or_raise_available_until_str(available_until_str)
        donation = Donation(category=category, description=description, available_until=available_until, address=address, donating_user_id=donating_user_id, donation_image_path=donation_image_path)
        cls._insert_donation_to_db(donation)

    @classmethod
    def _insert_donation_to_db(cls, donation: Donation):
        donation.validate_donation_details()
        num_rows_inserted = dbManager.commit(cls._INSERT_DONATION_SQL,
                                             (donation.category.name, donation.description,
                                              donation.available_until_str, donation.address,
                                              donation.donating_user_id,
                                              donation.donation_image_path))
        if num_rows_inserted == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed inserting donation', payload={'category': donation.category.name})

    @staticmethod
    def _parse_or_raise_available_until_str(available_until_str: str):
        try:
            return datetime_utils.from_datetime_str_to_datetime(available_until_str)
        except Exception as e:
            raise app_errors.InvalidAPIUsage('Failed parsing available_until date', available_until_str) from e

    @staticmethod
    def _parse_or_raise_category(category_str: str) -> DonationCategory:
        category = DonationCategory.get_from_str(category_str)
        if not category:
            raise app_errors.InvalidAPIUsage('Did not find category', payload={'category_str': category_str})
        return category

    @staticmethod
    def _parse_or_raise_availability_status(availability_status_str: str) -> DonationAvailabilityStatus:
        status = DonationAvailabilityStatus.get_from_str(availability_status_str)
        if not status:
            raise app_errors.InvalidAPIUsage('Invalid availability_status', payload={'availability_status_str': availability_status_str})
        return status

    @classmethod
    def delete_donation(cls, donation_id: int, donating_user_id: int):
        rows_affected = dbManager.commit(cls._DELETE_DONATION_SQL, (donation_id, donating_user_id))
        if rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed deleting donation', payload={'donation_id': donation_id})

    @classmethod
    def update_donation(cls, donation_id: int, availability_status_str: str = None, category_str: str = None, description: str = None, address: str = None, available_until_str: str = None):
        update_sql = "UPDATE donations SET "

        args = []
        if availability_status_str is not None:
            status = cls._parse_or_raise_availability_status(availability_status_str)
            update_sql += " availability_status = %s,"
            args.append(status.name)

        if category_str is not None:
            category = cls._parse_or_raise_category(category_str)
            update_sql += " category = %s,"
            args.append(category.name)

        if description is not None:
            update_sql += " description = %s,"
            args.append(description)

        if address is not None:
            update_sql += " address = %s,"
            args.append(address)

        if available_until_str is not None:
            available_until = cls._parse_or_raise_available_until_str(available_until_str)
            update_sql += " available_until = %s,"
            args.append(Donation.convert_available_until_date_to_str(available_until))

        update_sql = update_sql.rstrip(',')
        update_sql += "  WHERE id = %s;"
        args.extend([donation_id])

        num_rows_affected = dbManager.commit(update_sql, args)
        if num_rows_affected == dbManager.ERROR_CODE:
            raise app_errors.AppError('Failed updating donation', payload={'donation_id': donation_id})

