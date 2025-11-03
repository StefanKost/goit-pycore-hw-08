from entities.name import Name
from entities.phone import Phone
from entities.birthday import Birthday
from exceptions.conflict_error import ConflictError
from exceptions.not_found_error import NotFoundError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        if any(p.value == phone_obj.value for p in self.phones):
            raise ConflictError("Phone number")
        self.phones.append(phone_obj)

    def find_phone(self, phone: str) -> Phone:
        normalized_phone = Phone.normalize(phone)
        phone_obj = next((p for p in self.phones if p.value == normalized_phone), None)
        if phone_obj:
            return phone_obj
        raise NotFoundError("Phone number")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        current = self.find_phone(old_phone)
        new_phone = Phone(new_phone)

        if any(p.value == new_phone.value and p != current for p in self.phones):
            raise ConflictError("New phone number")

        idx = self.phones.index(current)
        self.phones[idx] = new_phone

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        self.phones.remove(phone_obj)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)
