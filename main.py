import shlex
from typing import List, Tuple
from commands import commands
from entities import AddressBook


def main():
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
          "  close, exit                               - Exit the bot\n")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue
            result = handle_command(user_input, address_book)
            if result == "exit":
                print("Good bye!")
                break
            print(result)
        except KeyboardInterrupt:
            print("\nGood bye!")
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


if __name__ == "__main__":
    main()
