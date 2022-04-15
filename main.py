import os
from database.source import Database
from database.exceptions import FieldNotFoundError
from constants import *


def show_searchable_fields_result(user_fields, ticket_fields, organization_fields):
    dbs = {
        "USERS": user_fields.fields(),
        "TICKETS": ticket_fields.fields(),
        "ORGANIZATIONS": organization_fields.fields()
    }
    print('=====================================')
    for db_key in dbs.keys():
        print(f'{db_key} Fields'.center(50, "="))
        for field in dbs[db_key]:
            print(f"* {field}".ljust(49, ' ') + "|")
    print(''.center(50, '='))


def show_search_result(result):
    if result is not None:
        assert isinstance(result, dict)
        print(" RESULT ".center(80, "="))
        for key in result.keys():
            # key_string = f"| * {key}:".ljust('30', ' ')
            print(f"| * {key}:".ljust(30, " ") + f" {result[key]}".ljust(49, " ") + "|")
            # value_string = f"{result[key]}".ljust(49, " ") + " |"
            # print(key_string + value_string)
        print("".center(80, "="))
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("***** No result was found *******")


if __name__ == "__main__":

    # connecting to users, tickets, and organizations datasets
    user_db = Database().connect(entities[USER])
    ticked_db = Database().connect(entities[TICKET])
    organization_db = Database().connect(entities[ORGANIZATION])

    execute = True

    dbs_options_dict = {
        1: user_db,
        2: ticked_db,
        3: organization_db
    }

    while execute:

        print(MAIN_OPTIONS)
        try:
            option = int(input('select your option:'))
        except:
            print('option can only be 1 or 2 or 3')
            continue

        if option == 1:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(ENTITY_OPTIONS)
                option = int(input('select your option:'))

                if option in {1, 2, 3}:
                    field = str(input("Enter search term: "))
                    value = str(input("Enter searched_value: "))

                    if value.isdigit():
                        value = int(value)
                    if value in {'true', 'false'}:
                        value = True if value == 'true' else False

                    result = dbs_options_dict[option].get(field, value)
                    show_search_result(result)
                    continue

                elif option == 4:
                    break
                else:
                    raise ()

            except FieldNotFoundError as e:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("****ERROR: ", str(e), '****')
                continue

            except:
                print('option can only be 1 or 2 or 3')
                continue

        if option == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            show_searchable_fields_result(user_db, ticked_db, organization_db)
        if option == 3:
            execute = False
