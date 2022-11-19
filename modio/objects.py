"""Module for user instanced classes."""

import datetime
import enum
import hashlib
import typing
import typing_extensions

from .enums import EventType, Maturity, Visibility
from .utils import _lib_to_api


class NewMod:
    """This class is unique to the library, it represents a mod to be submitted. The class
    must be instantiated with the appropriate parameters and then passed to game.add_mod().

    Parameters
    -----------
    name : str
        Name of the mod.
    name_id : Optional[str]
        Subdomain name for the mod. Optional, if not specified the name will be use. Cannot
        exceed 80 characters
    summary : str
        Brief overview of the mod, cannot exceed 250 characters.
    description : Optional[str]
        Detailed description of the mod, supports HTML.
    homepage : Optional[str]
        Official homepage for your mod. Must be a valid URL. Optional
    stock : Optional[int]
        Maximium number of subscribers for this mod. Optional, if not included disables
    metadata : Optional[str]
        Metadata stored by developers which may include properties on how information
        required. Optional. E.g. `"rogue,hd,high-res,4k,hd textures"`
    maturity : Optional[Maturity]
        Choose if the mod contains mature content.
    visible : Optional[Visibility]
        Visibility status of the mod
    logo : str
        Path to the file. If on windows, must have \\ escaped.
    """

    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id", None)
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description", None)
        self.homepage = attrs.pop("homepage", None)
        self.metadata_blob = attrs.pop("metadata", None)
        self.stock = attrs.pop("stock", 0)
        self.maturity_option = attrs.pop("maturity", Maturity.none).value
        self.visible = attrs.pop("visible", Visibility.public).value
        self.logo = attrs.pop("logo")
        self.tags = set()

    def add_tags(self, *tags):
        """Used to add tags to the mod, returns self for fluid chaining.

        Parameters
        -----------
        tags : List[str]
            List of tags, duplicate tags will be ignord.
        """
        self.tags = self.tags | set(tags)

        return self


class NewModFile:
    """This class is unique to the library and represents a file to be submitted. The class
    must be instantiated and then passed to mod.add_file().

    Parameters
    -----------
    version : str
        Version of the mod that this file represents
    changelog : str
        Changelog for the release
    active : Optional[bool]
        Label this upload as the current release. Optional, if not included defaults to True.
    metadata : str
        Metadata stored by the game developer which may include properties such as what version
        of the game this file is compatible with.

    """

    def __init__(self, **attrs):
        self.version = attrs.pop("version")
        self.changelog = attrs.pop("changelog")
        self.active = attrs.pop("active", True)
        self.metadata_blob = attrs.pop("metadata", None)

        self.file = None
        self.filehash = None

    def _file_hash(self, file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def add_file(self, path):
        """Used to add a file.

        The binary file for the release. For compatibility you should
        ZIP the base folder of your mod, or if it is a collection of files
        which live in a pre-existing game folder, you should ZIP those files.
        Your file must meet the following conditions:

            - File must be zipped and cannot exceed 10GB in filesize
            - Mods which span multiple game directories are not supported
                unless the game manages this
            - Mods which overwrite files are not supported unless the game manages this

        Parameters
        -----------
        path : str
            Path to file, if on windows must be \\ escaped.

        """
        self.file = path
        self.filehash = self._file_hash(path)

        return self


class Filter:
    """.. _filter:

    This class is unique to the library and is an attempt to make filtering
    modio data easier. Instead of passing filter keywords directly you can pass
    an instance of this class which you have previously fine tuned through the
    various methods. For advanced users it is also possible to pass filtering
    arguments directly to the class given that they are already in modio format.
    If you don't know the modio format simply use the methods, all method return
    self for fluid chaining. This is also used for sorting and pagination. These
    instances can be save and reused at will. Attributes which can be used as filters
    will be marked as "Filter attributes" in the docs for the class the endpoint
    returns an array of. E.g. ID is marked as a filter argument for in the class Game
    and therefore in get_games() it can be used a filter.

    Parameters
    ----------
    filters : Optional[dict]
        A dict which contains modio filter keyword and the appropriate value.

    """

    def __init__(self, filters=None):
        if filters is None:
            filters = {}

        self._q = None
        self._sort = None
        self._limit = None
        self._offset = None

        for key, value in filters.items():
            self._set(key, value)

    def __repr__(self):
        return f"< Filter filters={self.__dict__}>"

    def _set(self, key, value, text="{}"):
        try:
            key = _lib_to_api[key]
        except KeyError:
            pass

        if key == "event_type":
            if value.value < 8:
                value = f"MOD{'_' if value != EventType.file_changed else ''}{value.name.upper()}"
            else:
                value = f"USER_{value.name.upper()}"

        if isinstance(value, datetime.datetime):
            value = int(value.timestamp())

        if isinstance(value, enum.Enum):
            value = value.value

        setattr(self, text.format(key), value)

    def text(self, query):
        """Full-text search is a lenient search filter that is only available if
        the endpoint you are querying contains a name column.

        Parameters
        -----------
        query : str
            The words to identify. filter.text("The Lord of the Rings") - This will return every
            result where the name column contains any of the following words: 'The',
            'Lord', 'of', 'the', 'Rings'.

        """
        self._q = query
        return self

    def equals(self, **kwargs):
        """The simpliest filter you can apply is columnname equals. This will return all rows which
        contain a column matching the value provided. There are not set parameters, this methods takes
        any named keywords and transforms them into arguments that will be passed to the request. E.g.
        'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(key, value)
        return self

    def not_equals(self, **kwargs):
        """Where the preceding column value does not equal the value specified. There are not set parameters,
        this methods takes any named keywords and transforms them into arguments that will be passed to
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-not")
        return self

    def like(self, **kwargs):
        """Where the string supplied matches the preceding column value. This is equivalent to SQL's LIKE.
        Consider using wildcard's * for the best chance of results as described below. There are not set parameters,
        this methods takes any named keywords and transforms them into arguments that will be passed to
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-lk")
        return self

    def not_like(self, **kwargs):
        """Where the string supplied does not match the preceding column value. This is equivalent to SQL's
        NOT LIKE. This is equivalent to SQL's LIKE. Consider using wildcard's * for the best chance of results
        as described below. There are not set parameters, this methods takes any named keywords and transforms
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-not-lk")
        return self

    def values_in(self, **kwargs):
        """Where the supplied list of values appears in the preceding column value. This is equivalent
        to SQL's IN. There are not set parameters, this methods takes any named keywords and values as lists
        and transforms them into arguments that will be passed to the request.
        E.g. 'id=[10, 3, 4]' or 'name=["Best","Mod"]'
        """
        for key, value in kwargs.items():
            self._set(key, ",".join(str(x) for x in value), "{}-in")
        return self

    def values_not_in(self, **kwargs):
        """Where the supplied list of values does NOT appears in the preceding column value. This is equivalent
        to SQL's NOT IN. There are not set parameters, this methods takes any named keywords and values as lists
        and transforms them into arguments that will be passed to the request.
        E.g. 'id=[10, 3, 4]' or 'name=["Best","Mod"]'
        """
        for key, value in kwargs.items():
            self._set(key, ",".join(str(x) for x in value), "{}-not-in")
        return self

    def max(self, **kwargs):
        """Where the preceding column value is smaller than or equal to the value specified. There are not set
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed
        to the request. E.g. 'game_id=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-max")
        return self

    def min(self, **kwargs):
        """Where the preceding column value is greater than or equal to the value specified. There are not set
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed
        to the request. E.g. 'game_id=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-min")
        return self

    def smaller_than(self, **kwargs):
        """Where the preceding column value is smaller than the value specified. There are not set
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed
        to the request. E.g. 'game_id=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-st")
        return self

    def greater_than(self, **kwargs):
        """Where the preceding column value is greater than the value specified. There are not set
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed
        to the request. E.g. 'game_id=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-gt")
        return self

    def bitwise(self, **kwargs):
        """Some columns are stored as bits within an integer. You can combine any number of options for the column
        of the object you are querying. This is dependent on which item is being queried. These can be added together
        to check for multiple options at once. E.g if Option A: 1 and Option B: 2 then submitting 3 will return items
        that have both option A and B enabled.
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-bitwise-and")
        return self

    def sort(self, key, *, reverse=False):
        """Allows you to sort the results by the value of a top level column with a single value.

        Parameters
        ----------
        key : str
            The column by which to sort the results
        reverse : Optional[bool]
            Optional, defaults to False. Whether to sort by ascending (False) or descending (True)
            order.

        """
        self._sort = key if not reverse else f"-{key}"
        return self

    def limit(self, limit):
        """Allows to limit the amount of results returned per query.

        Parameters
        -----------
        limit : int
            Limit of returned results for the query
        """
        self._limit = limit
        return self

    def offset(self, offset):
        """Allows to offset the first result by a certain amount.

        Parameters
        ----------
        offset : int
            The number of results to skip.
        """
        self._offset = offset
        return self

    def get_dict(self):
        """Utility methods to get all filters while omitting None values

        Returns
        ---------
        Dict[str, Union[str, int]]
            The dict of filters
        """
        return {key: value for key, value in self.__dict__.items() if value is not None}


class Pagination:
    """This class is unique to the library and represents the pagination
    data that some of the endpoints return.

    Attributes
    -----------
    count : int
        Number of results returned by the request.
    limit : int
        Maximum number of results returned.
    offset : int
        Number of results skipped over
    total : int
        Total number of results avalaible for that endpoint with those filters.
    """

    def __init__(self, **attrs):
        self.count = attrs.pop("result_count")
        self.limit = attrs.pop("result_limit")
        self.offset = attrs.pop("result_offset")
        self.total = attrs.pop("result_total")

    def __repr__(self):
        return f"<Pagination count={self.count} limit={self.limit} offset={self.offset} total={self.total}>"

    def max(self):
        """Returns True if there are no additional results after this set."""
        return (self.offset + self.count) >= self.total

    def min(self):
        """Returns True if there are no additional results before this set."""
        return self.offset == 0

    def next(self):
        """Returns the offset required for the next set of results. If the max results have been reached this returns the
        current offset."""
        return self.offset + self.limit if not self.max() else self.offset

    def previous(self):
        """Returns the offset required for the previous set of results. If the min results have been reached this returns the
        current offset."""
        return self.offset - self.limit if not self.min() else self.offset

    def page(self):
        """Returns the current page number. Page numbers start at 0"""
        return self.offset // self.limit


Result = typing.TypeVar("Result")


class Returned(typing_extensions.NamedTuple, typing.Generic[Result]):
    """A named tuple returned by certain methods which return multiple results
    and need to return pagination data along with it.

    Attributes
    ----------
    results : List[Result]
        The list of results returned. This is typed accordingly to
        the method that returns it.
    pagination : Pagination
        Pagination metadata attached to the results
    """

    results: typing.List[Result]
    pagination: Pagination


class Object:
    """A dud class that can be used to replace other classes, keyword arguments
    passed will become attributes.

    """

    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __repr__(self):
        return str(self.__dict__)
