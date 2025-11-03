import shlex
from typing import List, Tuple
from commands import commands
from entities import AddressBook


def main():
    try:
        address_book = AddressBook.load()
        print(f"Address book loaded.\n")
    except Exception as e:
        print(f"Failed to load address book: {e}. Bot started with an empty book.")
        address_book = AddressBook()

    print("Welcome to the assistant bot!\n"
          "Available commands:\n"
          "  hello                                     - Show greeting\n"
          "  add <username> <phone>                    - Add new contact with phone or add phone to existing contact\n"
          "  change <username> <old_phone> <new_phone> - Update contact's phone\n"
          "  phone <username>                          - Show contact's phone number(s)\n"
          "  all                                       - Show all contacts\n"
          "  add-birthday <username> <DD.MM.YYYY>      - Add birthday to contact\n"
          "  show-birthday <username>                  - Show contact's birthday\n"
          "  birthdays                                 - Show upcoming birthdays within next week\n"
          "  save <filename>                           - Save data to file\n"
          "  load <filename>                           - Load data from the file\n"
          "  close, exit                               - Exit the bot\n")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue
            result = handle_command(user_input, address_book)
            if result == "exit":
                save_and_exit(address_book)
                break
            print(result)
        except KeyboardInterrupt:
            save_and_exit(address_book)
            break


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    args = shlex.split(user_input)
    if not args:
        return "", []
    command = args[0].lower()
    return command, args[1:]


def handle_command(user_input: str, address_book: AddressBook) -> str:
    command, args = parse_input(user_input)

    match command:
        case "close" | "exit":
            return "exit"
        case cmd if cmd in commands:
            return commands[cmd](args, address_book)
        case _:
            available = ', '.join(sorted(commands.keys()) + ['close', 'exit'])
            return f"Invalid command. Available commands: {available}"


def save_and_exit(address_book: AddressBook) -> None:
    print("Saving data...")
    try:
        address_book.save()
        print(f"Data successfully to file: {address_book.get_filename()}")
    except Exception as e:
        print(f"Failed to save data: {e}")
    print("Good bye!")


if __name__ == "__main__":
    main()
