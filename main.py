from database.source import Database
from database.exceptions import FieldNotFoundError

# entities
USER = 'user'
TICKET = 'ticket'
ORGANIZATION = 'organization'

# path of all entities
entities = {
    USER: 'data/users.json',
    TICKET: 'data/tickets.json',
    ORGANIZATION: 'data/organizations.json'
}

MAIN_OPTIONS = """
 -----------------------------------
|       Select one option           |
|-----------------------------------|
| 1. Search Zendesk                 |
| 2. View list of searchable fields | 
| 3. Quit                           |
 -----------------------------------
"""

ENTITY_OPTIONS = """
 -----------------------------------
|       Select one option           |
|-----------------------------------|
| 1. Users                          |
| 2. Tickets                        | 
| 3. Organizations                  |
| 4. Quit                           |
 -----------------------------------
"""


def show_searchable_fields_result(user_fields, ticket_fields, organization_fields):
    print('=====================================')
    print('============ USERS ==================')
    print("\n".join(user_fields.fields()))
    print('============ TICKETS ================')
    print("\n".join(user_fields.fields()))
    print('============ ORGANIZATIONS ==========')
    print("\n".join(user_fields.fields()))
    print('=====================================')


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
                    if result is not None:
                        assert isinstance(result, dict)
                        print("===================== RESULT ===============")
                        for key in result.keys():
                            print(f"{key}:  {result[key]}")
                        print("============================================")
                    else:
                        print("No result was found")

                    continue

                else:
                    raise ()

            except FieldNotFoundError as e:
                print("ERROR: ", str(e))
                continue

            except:
                print('option can only be 1 or 2 or 3')
                continue

        if option == 2:
            show_searchable_fields_result(user_db, ticked_db, organization_db)
        if option == 3:
            execute = False
