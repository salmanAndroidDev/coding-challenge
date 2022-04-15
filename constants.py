"""
    CONSTANT variables are stored in this file
"""

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
