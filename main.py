from database.source import Database

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

OPTIONS = """
------------------------
| 1. 
|
|
|
------------------------
"""






if __name__ == "__main__":
    db = Database()

    db.connect('data/users.json')
    field = '_id'
    value = 4
    print(db.filter(field, value))
#     json_data = convert_file_path_to_JSON()
#     json_search = JSONSearch()
#     json_search.add_data(json_data)
#     print(json_search.get_fields())
