from datetime import datetime, timedelta
from typing import Optional
from collections import UserDict
from entities.record import Record
from exceptions import ConflictError, NotFoundError, InvalidFilename
import os
import re
from pathlib import Path
import tempfile
import pickle


class AddressBook(UserDict):
    DEFAULT_FILENAME = "addressbook.pkl"
    DATA_DIR = Path("data")
    record_counter: int = 0

    def __init__(self, dict=None, /, **kwargs):
        super().__init__(dict, **kwargs)
        self.__filename: str = AddressBook.DEFAULT_FILENAME
        AddressBook.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def add_record(self, record: Record) -> None:
        if any(str(existing) == str(record) for existing in self.data.values()):
            raise ConflictError("Record")
        AddressBook.record_counter += 1
        self.data[AddressBook.record_counter] = record

    def find(self, contact_name: str) -> Record:
        key = self._find_key(contact_name)
        return self.data[key]

    def delete(self, contact_name: str) -> None:
        key = self._find_key(contact_name)
        del self.data[key]

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Generate a list of users whose birthdays occur within the next 7 days. Returns congratulation dates
        :param users: List of users with (name and birthday)
        :return: List of users whose birthday withing next 7 days with congratulation date
        """
        date_format = "%d.%m.%Y"
        today = datetime.today().date()
        upcoming_birthdays = []
        shift_days = {5: 2, 6: 1}  # Saturday - +2 days, Sunday - +1 day

        def get_next_birthday(bday: datetime.date) -> datetime.date:
            """
            Return the next birthday date for a given birthday

            :param bday: user's birthday
            :return: next birthday date
            """
            start_year = today.year
            while True:
                try:
                    bday_this_year = bday.replace(year=start_year)
                except ValueError:
                    # Handle Feb 29 in non-leap years by celebrating on March 1
                    bday_this_year = datetime(today.year, 3, 1).date()

                if bday_this_year >= today:
                    return bday_this_year

                start_year += 1

        for user in self.data.values():
            if user.birthday is None:
                continue

            try:
                birthday = datetime.strptime(user.birthday.value, date_format).date()
            except ValueError:
                print(f"User {user['name']} has invalid birthday")
                continue

            # change year
            birthday = get_next_birthday(birthday)

            # Calculate days until the next birthday
            days_until_birthday = (birthday - today).days

            if days_until_birthday is None or days_until_birthday > 7:
                continue

            # shift congratulation day to Monday if birthday on Saturday and Sunday
            congratulation_date = birthday + timedelta(days=shift_days.get(birthday.weekday(), 0))

            upcoming_birthdays.append({
                "name": str(user.name),
                "congratulation_date": congratulation_date.strftime(date_format)
            })

        return upcoming_birthdays

    def _find_key(self, contact_name: str) -> int:
        key = next((k for k, r in self.data.items() if r.name.value == contact_name), None)
        if not key:
            raise NotFoundError("Contact")
        return key

    def set_filename(self, filename: str) -> None:
        self.__filename = self.set_file_extension(filename)

    def get_filename(self) -> str:
        return self.__filename or self.DEFAULT_FILENAME

    def save(self, filename: Optional[str] = None) -> None:
        name = filename if filename is not None else self.get_filename()
        self.validate_filename(name)
        name = self.set_file_extension(name)
        filepath = AddressBook.DATA_DIR / name

        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="wb", delete=False, dir=str(AddressBook.DATA_DIR), prefix=Path(name).stem + "_", suffix=".tmp"
            ) as tmp:
                tmp_file = Path(tmp.name)
                pickle.dump(self, tmp)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(tmp_file, filepath)
            self.set_filename(name)
        except (OSError, pickle.PicklingError) as e:
            if tmp_file and tmp_file.exists():
                try:
                    tmp_file.unlink()
                except OSError:
                    pass
            raise IOError(f"Failed to save address book: {e}") from e

    @classmethod
    def load(cls, filename: Optional[str] = None) -> "AddressBook":
        name = filename if filename is not None else AddressBook.DEFAULT_FILENAME
        cls.validate_filename(name)
        name = cls.set_file_extension(name)
        filepath = AddressBook.DATA_DIR / name

        is_empty = False
        if not filepath.exists():
            is_empty = True

        try:
            if filepath.stat().st_size == 0:
                is_empty = True
        except OSError:
            is_empty = True

        if is_empty:
            address_book = cls()
            address_book.set_filename(name)
            return address_book

        try:
            with open(filepath, "rb") as f:
                address_book = pickle.load(f)
            if not isinstance(address_book, cls):
                raise ValueError("Invalid data")
            address_book.set_filename(name)
            AddressBook.record_counter = max(address_book.data, default=None)
            return address_book
        except (OSError, pickle.UnpicklingError, EOFError, AttributeError, ValueError) as e:
            raise IOError(f"Failed to load the address book: {e}") from e

    @staticmethod
    def set_file_extension(name: str):
        return name if name.endswith(".pkl") else f"{name}.pkl"

    @staticmethod
    def validate_filename(filename: str):
        if not isinstance(filename, str) or not filename:
            raise InvalidFilename("Filename cannot be empty")

        if os.path.basename(filename) != filename:
            raise InvalidFilename("Filename must not contain directories")

        if re.search(r"(^\.)|(\.\.)", filename):
            raise InvalidFilename("Filename cannot be relative")

        if not re.fullmatch(r'[A-Za-z0-9_.-]+', filename):
            raise InvalidFilename("Invalid filename")

        if '.' in filename and not filename.endswith('.pkl'):
            raise InvalidFilename("Only files with .pkl extension are allowed")

        if len(filename) > 80:
            raise InvalidFilename("Filename too long (max 80 characters)")

        return True
