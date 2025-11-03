from typing import Dict, List, Callable
from entities import AddressBook, Record
from exceptions import NotFoundError
from helpers import input_error


@input_error
def add_contact(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("add command requires 2 arguments: username and phone")

    name, phone = args[0], args[1]

    try:
        record = address_book.find(name)
        record.add_phone(phone)
        return f"Added phone to contact: {name}."
    except NotFoundError:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."


@input_error
def change_contact(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("change command requires 3 arguments: username, old phone, new phone")

    name, old_phone, new_phone = args[0], args[1], args[2]

    record = address_book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact phone has been updated."


@input_error
def show_phone(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("phone command requires 1 argument: username")

    name = args[0]
    record = address_book.find(name)

    if not record.phones:
        return f"{name} has no phone numbers."

    return str(record)


@input_error
def show_all(address_book: AddressBook) -> str:
    if not address_book:
        return "No contacts found."

    rows = [str(record) for record in address_book.values()]
    return "All contacts:\n" + "\n".join(rows)


@input_error
def add_birthday(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("add-birthday command requires 2 arguments: username and birthday (DD.MM.YYYY)")

    name, birthday = args[0], args[1]

    record = address_book.find(name)
    record.add_birthday(birthday)
    return f"Added birthday to contact: {name}."


@input_error
def show_birthday(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("show-birthday command requires 1 argument: username")

    name = args[0]
    record = address_book.find(name)

    if record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    else:
        return f"No birthday defined for {name}."


@input_error
def save(args: List[str], address_book: AddressBook) -> str:
    if not args:
        raise ValueError("Save command requires a filename argument")
    filename = args[0]
    address_book.save(filename)
    return f"Data saved to {address_book.get_filename()}."


@input_error
def load(args: List[str], address_book: AddressBook) -> str:
    if not args:
        raise ValueError("Load command requires a filename argument")
    filename = args[0]
    loaded_book = AddressBook.load(filename)
    count = len(loaded_book.data)
    address_book.data.clear()
    address_book.data.update(loaded_book.data)
    address_book.set_filename(filename)
    print(AddressBook.record_counter)
    return f"Address book loaded from {address_book.get_filename()}. {count} contact(s) found."


@input_error
def birthdays(address_book: AddressBook) -> str:
    upcoming_birthdays = address_book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 7 days."

    rows = [f"{user['name']}: {user['congratulation_date']}" for user in upcoming_birthdays]
    return "Upcoming birthdays:\n" + "\n".join(rows)


commands: Dict[str, Callable[[List[str], AddressBook], str]] = {
    "hello": lambda args, address_book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": lambda args, address_book: show_all(address_book),
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": lambda args, address_book: birthdays(address_book),
    "save": save,
    "load": load,
}
