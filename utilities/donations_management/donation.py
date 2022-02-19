import datetime
import enum
import pathlib
from typing import Optional
import app_errors
import settings
from utilities import datetime_utils


class DonationCategory(enum.Enum):
    FRUITS = enum.auto()
    VEGETABLES = enum.auto()
    GRAINS = enum.auto()
    DAIRY = enum.auto()
    CLOTHS = enum.auto()
    FURNITURE = enum.auto()
    OTHER = enum.auto()

    @classmethod
    def get_from_str(cls, category_str) -> Optional['DonationCategory']:
        try:
            return DonationCategory[category_str.upper()]
        except Exception:
            return None


class DonationAvailabilityStatus(enum.Enum):
    AVAILABLE = enum.auto()
    RESERVED_FOR_USER = enum.auto()
    DELIVERED = enum.auto()

    @classmethod
    def get_from_str(cls, availability_status_str) -> Optional['DonationAvailabilityStatus']:
        try:
            return DonationAvailabilityStatus[availability_status_str.upper()]
        except Exception:
            return None



class Donation:

    _MIN_MINUTES_TO_PICK_UP_PRODUCT = 24 * 60  # 24 hours

    def __init__(self, category: DonationCategory, description: str, available_until: datetime.datetime, address: str, donation_image_path: str, availability_status: Optional[DonationAvailabilityStatus] = None, donation_id: Optional[int] = None, donating_user_id: Optional[int] = None):
        self._category = category
        self._description = description
        self._available_until = available_until
        self._address = address
        self._donation_id = donation_id
        self._donating_user_id = donating_user_id
        self._availability_status = availability_status
        self._donation_image_path = donation_image_path

    def __str__(self):
        return f'{self.category}__{self.description}__{self.donating_user_id}__{self._availability_status}'

    @property
    def donating_id(self) -> int:
        return self._donation_id

    @property
    def donating_user_id(self) -> int:
        return self._donating_user_id

    @property
    def category(self) -> DonationCategory:
        return self._category

    @property
    def donation_image_path(self) -> str:
        return self._donation_image_path

    @property
    def description(self) -> str:
        return self._description

    @property
    def available_until(self) -> datetime.datetime:
        return self._available_until

    @property
    def available_until_str(self) -> str:
        return self.convert_available_until_date_to_str(self.available_until)

    @staticmethod
    def convert_available_until_date_to_str(available_until) -> str:
        return datetime_utils.convert_datetime_to_timestamp(available_until)

    @property
    def address(self) -> Optional[str]:
        return self._address

    @property
    def availability_status(self) -> Optional[DonationAvailabilityStatus]:
        return self._availability_status

    def validate_donation_details(self):
        return self._validate_availability_date()# and self._validate_donation_image()

    def _validate_availability_date(self) -> bool:
        min_time_for_pickup = datetime.datetime.utcnow() + datetime.timedelta(minutes=self._MIN_MINUTES_TO_PICK_UP_PRODUCT)
        if self.available_until < min_time_for_pickup:
            raise app_errors.InvalidAPIUsage('Insufficient time to pickup donation')
        return True

    def serialize(self) -> dict:
        return {
            'donation_id': self._donation_id,
            'category': self.category.name,
            'description': self.description,
            'available_until': self.convert_available_until_date_to_str(self.available_until),
            'address': self.address,
            'donating_user_id': self.donating_user_id,
            'availability_status': self.availability_status and self.availability_status.name,
            'donation_image_path': self.donation_image_path
        }

    # def _validate_donation_image(self):
    #     path = pathlib.Path(settings.UPLOAD_FOLDER, self.donation_image_path)
    #     if not path.is_file():
    #         raise app_errors.InvalidAPIUsage('Did not find donation image', payload={'image': self.donation_image_path})
