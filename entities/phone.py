import re
from entities.field import Field
from exceptions.invalid_phone import InvalidPhone


class Phone(Field):
    def __init__(self, raw_phone: str):
        phone = self.normalize(raw_phone)
        if not self.validate(phone):
            raise InvalidPhone(
                f"Invalid phone number: '{raw_phone}'. Should consist of 10 digits."
            )
        super().__init__(phone)

    @staticmethod
    def validate(phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10

    @staticmethod
    def normalize(raw: str) -> str:
        return re.sub(r"\D+", "", raw)
