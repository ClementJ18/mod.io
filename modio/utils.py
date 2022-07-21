"""Utility functions for the library"""
import inspect
import enum
import datetime


def concat_docs(cls):
    """Does it look like I'm enjoying this?"""
    attributes = []

    def get_docs(parent):
        nonlocal attributes
        if parent.__name__ == "object":
            return

        docs = parent.__doc__.splitlines() if parent.__doc__ else ""
        if "    Attributes" in docs:
            attributes = docs[docs.index("    Attributes") + 2 :] + attributes

        source = inspect.getsource(parent.__init__)
        source = source[source.index("):") :]

        if "super().__init__" in source:
            get_docs(parent.__base__)
        elif "__init__" in source:
            get_docs(parent.__base__.__base__)

    get_docs(cls)
    original = cls.__doc__.splitlines()
    if "    Attributes" not in original:
        original.append("    Attributes")
        original.append("    -----------")

    final = original[: original.index("    Attributes") + 2]
    final.extend([x for x in attributes if x.strip()])
    cls.__doc__ = "\n".join(final)

    return cls


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
        if all(key in e.__dict__ for key in fields):
            if all(e.__dict__[key] == fields[key] for key in fields):
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

    e_list = []
    for e in iterable:
        if all(key in e.__dict__ for key in fields):
            if all(e.__dict__[key] == fields[key] for key in fields):
                e_list.append(e)

    return e_list


_lib_to_api = {
    "maturity": "maturity_option",
    "date": "date_added",
    "metadata": "metadata_blob",
    "key": "metakey",
    "value": "metavalue",
    "type": "event_type",
    "presentation": "presentation_option",
    "curation": "curation_option",
    "community": "community_options",
    "submission": "submission_option",
    "revenue": "revenue_options",
    "api": "api_access_options",
    "ugc": "ugc_name",
    "profile": "profile_url",
    "homepage": "homepage_url",
    "submitter": "submitted_by",
    "live": "date_live",
    "updated": "date_updated",
    "team_id": "id",
    "kvp": "metadata_kvp",
    "expires": "date_expires",
    "mod": "mod_id",
    "game": "game_id",
    "file": "modfile",
    "virus": "virus_positive",
    "size": "filesize",
    "hash": "filehash",
    "rank": "popularity_rank_position",
    "rank_total": "popularity_rank_position",
    "downloads": "downloads_total",
    "subscribers": "subscribers_total",
    "positive": "ratings_positive",
    "negative": "ratings_negative",
    "sort_downloads": "downloads",
    "sort_popular": "popular",
    "sort_subscribers": "subscribers",
    "sort_rating": "rating",
    "member_id": "id",
    "parent": "reply_id",
    "position": "thread_position",
    "tz": "timezone",
    "lang": "language",
}


def _clean_and_convert(fields):
    new_fields = {}
    for key, value in fields.items():
        try:
            key = _lib_to_api[key]
        except KeyError:
            pass

        if isinstance(value, enum.Enum):
            value = value.value
        elif isinstance(value, datetime.datetime):
            value = value.total_seconds()
        elif hasattr(value, "id"):
            value = value.id

        new_fields[key] = value

    return new_fields


def _convert_date(time):
    return datetime.datetime.utcfromtimestamp(time)
