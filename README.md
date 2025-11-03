# CLI Assistant Bot
Assistant tool for managing contacts

## Start
```bash
python main.py
```

## Available Commands
| Command         | Usage                                       | Description                                          |
|-----------------|---------------------------------------------|------------------------------------------------------|
| `add`           | `add <username> <phone>`                    | Add new contact or add new phone to existing contact |
| `change`        | `change <username> <old_phone> <new_phone>` | Update contact's phone number                        |
| `phone`         | `phone <username>`                          | Show contact's phone number(s)                       |
| `add-birthday`  | `add-birthday <username> <DD.MM.YYYY>`      | Add birthday to existing contact                     |
| `show-birthday` | `show-birthday <username>`                  | Show contact's birthday                              |
| `birthdays`     | `birthdays`                                 | Show upcoming (next week) birthdays                  |
| `all`           | `all`                                       | Show all contacts and their phones                   |
| `save`          | `save <filename>`                           | Save data to the custom file                         |
| `load`          | `load <filename>`                           | Load data from the custom file                       |
| `hello`         | `hello`                                     | Show greeting                                        |
| `exit`          | `exit` or `close`                           | Exit the bot                                         |