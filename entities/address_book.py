from datetime import datetime, timedelta
from collections import UserDict
from entities.record import Record
from exceptions.conflict_error import ConflictError
from exceptions.not_found_error import NotFoundError


class AddressBook(UserDict):
    record_counter: int = 0

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

