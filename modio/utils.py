def find(iterable, attr, value):
    """Finds the first item in the :attrs: iterable that has the :attrs: attr equal to :attrs: value. For
    example:

        game = find(client.get_all_games(), 'id', 2)

    would find the first :class: Game whose id is 2 and return it. If no entry is found then
    None is returned.  """

    for e in iterable:
        if attr in e.__dict__:
            if e.__dict__[attr] == value:
                return e

    return None

def get(iterable, attr, value):
    """Returns a list of items in the :attrs: iterable that have the :attrs: attr equal to :attrs: value. For
    example:

        game = get(client.get_all_games(), 'id', 2)

    would find the all :class: Game whose id is 2 and return them as a list. If no entry is found then
    the empty list is returned.  """

    e_list = list()
    for e in iterable:
        if attr in e.__dict__:
            if e.__dict__[attr] == value:
                e_list.append(e)

    return e_list
