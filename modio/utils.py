def find(iterable, **fields):
    """Finds the first item in the :attrs: iterable that has the :attrs: attr equal to :attrs: value. For
    example:

        game = find(client.get_all_games(), id=2)

    would find the first :class: Game whose id is 2 and return it. If no entry is found then
    None is returned.  
    
        game = find(client.get_all_games(), name="John")

    would find the first :class: `Game` whose name is 'John'. If not entry is found then None
    is returned

    """

    for e in iterable:
        if all(key in e.__dict__ for key in fields.keys()):
            if all(e.__dict__[key] == fields[key] for key in fields.keys()):
                return e

    return None

def get(iterable, **fields):
    """Returns a list of items in the :attrs: iterable that have the :attrs: attr equal to :attrs: value. For
    example:

        game = get(client.get_all_games(), id=2)

    would find the all :class: Game whose id is 2 and return them as a list. If no entry is found then
    the empty list is returned. 

        game = find(client.get_all_games(), name="John")

    would find all :class: `Game` whose name is 'John'. If not entry is found then an empty list
    is returned
    """

    e_list = list()
    for e in iterable:
        if all(key in e.__dict__ for key in fields.keys()):
            if all(e.__dict__[key] == fields[key] for key in fields.keys()):
                e_list.append(e)

    return e_list
