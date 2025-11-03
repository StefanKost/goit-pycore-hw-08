import re
from datetime import datetime
from entities.field import Field
from exceptions.invalid_birthday import InvalidBirthday


class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(birthday: str) -> None:
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", birthday):
            raise InvalidBirthday('Invalid birthday format. Should be (DD.MM.YYYY)')

        try:
            date = datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise InvalidBirthday(f"Invalid birthday date: {birthday}")

        if date > datetime.now():
            raise InvalidBirthday('Birthday cannot be in future')
