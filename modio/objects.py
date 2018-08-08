from .errors import modioException
import hashlib
import enum

class Message:
    """A simple representation of a modio Message, used when modio returns
    a status message for the query that was accomplished.

    Attributes
    -----------
    code : int
        An http response code
    message : str
        The server response to the request

    """
    def __init__(self, **attrs):
        self.code = attrs.pop("code")
        self.message =attrs.pop("message")

    def __str__(self):
        return f"{self.code} : {self.message}"

class Image:
    """A representation of a modio image, which stand for the Logo, Icon
    and Header of a game/mod or the Avatar of a user.Can also be a regular
    image.

    Attributes
    -----------
    filename : str
        Name of the file
    original : str
        Link to the original file
    small : str
        A link to a smaller version of the image, processed by modio. Size varies based
        on the object being processed. Can be None.
    medium : str
        A link to a medium version of the image, processed by modio. Size varies based
        on the object being processed. Can be None.
    large : str
        A link to a large version of the image, processed by modio. Size varies based
        on the object being processed. Can be None.

    """
    def __init__(self, **attrs):
        self.filename = attrs.pop("filename")
        self.original = attrs.pop("original")

        self.small = list(attrs.values())[2] if len(attrs) > 2 else None
        self.medium = list(attrs.values())[3] if len(attrs) > 3 else None
        self.large = list(attrs.values())[4] if len(attrs) > 4 else None    

class EventType(enum.Enum):
    0 = file_changed
    1 = available
    2 = unavailable
    3 = edited
    4 = deleted
    5 = team_changed
    6 = other    

class Event:
    """Represents a mod event. 

    Attributes
    -----------
    id : int
        Unique ID of the event
    mod : int
        ID of the mod this event is from
    user : int
        ID of the user that made the change
    data : int
        UNIX timestamp of the event occurrence
    type : enum.EventType
        Type of the event.

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.date = attrs.pop("date_added")
        self._raw_type = attrs.pop("event_type")
        self.mod = attrs.pop("mod_id")
        self.user = attrs.pop("user_id")

    @property
    def type(self):
        if self._raw_type == "MODFILE_CHANGED":
            return EventType.file_changed
        elif self._raw_type == "MOD_AVAILABLE":
            return EventType.available
        elif self._raw_type == "MOD_UNAVAILABLE":
            return EventType.unavailable
        elif self._raw_type == "MOD_EDITED":
            return EventType.edited
        elif self._raw_type == "MOD_DELETED":
            return EventType.deleted
        elif self._raw_type == "MOD_TEAM_CHANGED":
            return EventType.team_changed
        else:
            return EventType.other

class Comment:
    """Represents a comment on a mod page.

    Attributes
    -----------
    id : int
        ID of the comment
    mod : id
        ID of the mod this comment is from
    author : modio.User
        Istance of the user that submitted the comment
    date : int
        Unix timestamp of date the comment was posted.
    parent : int
        ID of the parent this comment is replying to. 0 if comment
        is not a reply
    position : str
        Level of nesting. How it works:
        - The first comment will have the position '01'.
        - The second comment will have the position '02'.
        - If someone responds to the second comment the position will be '02.01'.
        - A maximum of 3 levels is supported.
    karma : int
        Total karma received for the comment.
    karma_guest : int
        Total karma received from guests for this comment
    content : str
        Content of the comment
    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.mod = attrs.pop("mod_id")
        self.author = User(**attrs.pop("submitter"))
        self.date = attrs.pop("date_added")
        self.parent = attrs.pop("reply_id")
        self.position = attrs.pop("reply_position")
        self.karma = attrs.pop("karma")
        self.karma_guest = attrs.pop("karma_guest")
        self.content = attrs.pop("content")

class ModDependencies:
    """Represents a mod dependency, a mod that this mod relies on to be installed correctly

    Attributes
    -----------
    id : int
        ID of the dependency mod
    date : int
        UNIX timestamp of the moment the dependency was added

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("mod_id")
        self.date = attrs.pop("date")

class MeModFile:
    """A object to represent modfiles that are returned from the me/modfiles endpoint.
    Equivalent to the regular ModFile object except that you cannot call the delete or
    edit function from it as it lacks a game_id.

    Attributes
    -----------
    id : int
        ID of the modfile
    mod : int
        ID of the mod it was added for
    date_added : int
        UNIX timestamp of the date the modfile was submitted
    date_scanned : int
        UNIX timestamp of the date the file was virus scanned
    status : int
        Current status of the virus scan for the file. 
        0 : Not scanned
        1 : Scan complete
        2 : In progress
        3 : Too large to scan
        4 : File not found
        5 : Error Scanning
    virus : bool
        True if a virus was detected, False if it wasn't.
    virus_hash : str
        VirusTotal proprietary hash to view the scan results.
    size : int
        Size of the file in bytes
    hash : str
        MD5 hash of the file.
    name : str
        Name of the file
    version : str
        Version of the file
    changelog : str
        Changelog for the file
    metadata : str
        Metadata stored by the game developer for this file.
    download : dict
        Contains download data
        'binary_url' : url to download file
        'date_expires' : UNIX timestamp of when the url expires
    """
    def __init__(self,**attrs):
        self.id = attrs.pop("id")
        self.mod = attrs.pop("mod_id")
        self.date_added = attrs.pop("date_added")
        self.date_scanned = attrs.pop("date_scanned")
        self.status = attrs.pop("virus_status")
        self.virus = bool(attrs.pop("virus_positive"))
        self.virus_hash = attrs.pop("virustotal_hash")
        self.size = attrs.pop("filesize")
        self.hash = attrs.pop("filehash")["md5"]
        self.name = attrs.pop("filename")
        self.version = attrs.pop("version")
        self.changelog = attrs.pop("changelog")
        self.metadata = attrs.pop("metadata_blob")
        self.download = attrs.pop("download")

    def edit(self, **fields):
        raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")

    def delete(self):
        raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")

class ModFile(MeModFile):
    """Inherits from MeModFile

    Attributes
    -----------
    game : int
        ID of the game of the mod this file belongs to.
    
    """
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.game = attrs.pop("game_id")
        self.client = attrs.pop("client")

    def edit(self, **fields):
        
        file_json = self.client._put_request(f'/games/{self.game_id}/mods/{self.mod_id}/files/{self.id}', h_type = 0, data = fields)
        self.__init__(client=self.client, game_id=self.game, **file_json)

    def delete(self):
        r = requests.delete(f'/games/{self.game_id}/mods/{self.mod_id}/files/{self.id}', h_type = 0)
        return r

class ModMedia:
    """Represents all the media for a mod.

    Attributes
    -----------
    youtube : list[str]
        A list of youtube links
    sketchfab : list[str]
        A list of SketchFab links
    images : list[modio.Image]
        A list of image objects (gallery)

    """
    def __init__(self, **attrs):
        self.youtube = attrs.pop("youtube")
        self.sketchfab = attrs.pop("sketchfab")
        self.images = [Image(**image) for image in attrs.pop("images", [])]

class ModTag:
    """Represents a tag
    
    Attributes
    -----------
    name : str
        Name fo the tag
    date : int
        UNIX timestamp of when the tag was added

    """
    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.date = attrs.pop("date_added")
        self.__dict__ = {self.name : self.date_added}

    def __str__(self):
        return self.name    

class GameTag:
    """Represents a game tag gropup, a category of tags from which a 
    mod may pick one or more.

    Attributes
    -----------
    name : str
        Name of the tag group
    type : str
        Can be either "checkbox" where users can chose multiple tags
        from the list or "dropdown" in which case only one tag can be
        chosen from the group
    hidden : bool
        Whether or not the tag is only accessible to game admins, used
        for internal mod filtering.
    tags : list[str]
        Array of tags for this group

    """
    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.type = attrs.pop("type")
        self.hidden = attrs.pop("hidden")
        self.tags = attrs.pop("tags", [])

    def __str__(self):
        return self.name

class MetaData:
    """Represents the data left by the devs on the game. Can be retrieved
    as a dict {key : value}
    
    Attributes
    -----------
    key : str
        The key of the key-value pair.
    value : str
        The value of the key-value pair.
    """
    def __init__(self, **attrs):
        self.key = attrs.pop("metakey")
        self.value = attrs.pop("metavalue")
        self.__dict__ = {self.key : self.value}

class RatingSummary:
    """Represents a summary of all the ratings by the users on the mod

    Attributes
    -----------
    total : int
        Number of times this item has been rated
    positive : int
        Number of positive ratings
    negative : int
        Number of negative ratings
    percentage : int
        Percentage of positive rating (positive/total)
    weighted : int
        Overall rating of this item calculated using the Wilson score confidence 
        interval. This column is good to sort on, as it will order items based 
        on number of ratings and will place items with many positive ratings above 
        those with a higher score but fewer ratings.
    text : str
        Textual representation of the rating in format. This is currently not updated
        by the lib so you'll have to poll the resource's endpoint again.
    """
    def __init__(self, **attrs):
        self.total = attrs.pop("total_ratings")
        self.positive = attrs.pop("positive_ratings")
        self.negative = attrs.pop("negative_ratings")
        self.percentage = attrs.pop("percentage_positive")
        self.weighted = attrs.pop("weighted_aggregate")
        self.text = attrs.pop("display_text")

class User:
    """Represents a modio user.

    Attributes
    ----------
    id : int
        ID of the user
    name_id : str
        Subdomain name of the user. For example: https://mod.io/members/username-id-here
    name : str
        Name of the user
    last_online : int
        Unix timestamp of date the user was last online.
    avatar : modio.Image
        Contains avatar data
    tz : str
        Timezone of the user, format is country/city.
    lang : str
        Users language preference. See localization for the supported languages.
    url : str
        URL to the user's mod.io profile.

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.name_id = attrs.pop("name_id")
        self.name = attrs.pop("username")
        self.last_online = attrs.pop("date_online")

        avatar = attrs.pop("avatar")

        if len(avatar.keys()) > 0:
            self.avatar = Image(**avatar)
        else:
            self.avatar = None

        self.tz = attrs.pop("timezone")
        self.lang = attrs.pop("language")
        self.url = attrs.pop("profile_url")

class TeamMember(User):
    """Inherits from modio.User. Represents a user as part of a team.
    
    Attributes
    -----------
    member_id : int
        The id of the user in the context of their team, not the same as
        user id
    level : int
        Level of permissions the user has
        1 : Moderator
        4 : Creator
        8 : Administrator
    date : int
        Unix timestamp of the date the user was added to the team.
    position : str
        Custom title given to the user in this team.

    """
    def __init__(self, **attrs):
        super().__init__(**attrs.pop("user"))
        self.team_id = attrs.pop("id")
        self.level = attrs.pop("level")
        self.date = attrs.pop("date_added")
        self.position = attrs.pop("position")

class NewMod:
    """This class is unique to the library, it represents a mod to be submitted. The class
    must be instantiated with the appropriate parameters and then passed to game.add_mod().

    Parameters
    -----------
    name : str
        Name of the mod
    name_id : str
        Subdomain name for the mod. Optional, if not specified the name will be use. Cannot
        exceed 80 characters
    summary : str
        Brief overview of the mod, cannot exceed 250 characters.
    description :str
        Detailed description of the mod, supports HTML.
    homepage : str
        Official homepage for your mod. Must be a valid URL. Optional
    stock : int
        Maximium number of subscribers for this mod. A value of 0 disables this limit.
    metadata : str
        Metadata stored by developers which may include properties on how information 
        required. Optional.
    stock : int
        Maximum number of subscribers for this mod. Optional, if not included disables it
    maturity : int
        Choose if the mod contains mature content. 
        0 : None
        1 : Alcohol
        2 : Drugs
        4 : Violence
        8 : Explicit
        ? : Above options can be added together to create custom settings (e.g 3 : 
        alcohol and drugs present)
    """
    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id", None)
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description")
        self.homepage = attrs.pop("homepage", None)
        self.metadata_blob = attrs.pop("metadata", None)
        self.stock = attrs.pop("stock", 0)
        self.maturity_option = attrs.pop("maturity", 0)
        self.tags = []

    def add_tags(self, tags):
        """Used to add tags to the mod, returns self for fluid chaining.

        Parameters
        -----------
        tags : list[str]
            List of tags, duplicate tags will be ignord.
        """
        self.tags += [tag for tag in tags if tag not in self.tags]

        return self

    def add_logo(self, path):
        """Used to add a logo to the new mod, returns self for fluid chaining.

        Parameters
        -----------
        path : str
            Path to the file. If on windows, must have \\ escaped.
        """
        self.logo = open(path, "rb")

        return self

class NewFile:
    """This class is unique to the library and represents a file to be submitted. The class
    must be instantiated and then passed to mod.add_file().

    Parameters
    -----------
    version : str
        Version of the mod that this file represents
    changelog : str
        Changelog for the release
    active : bool
        Label this upload as the current release. Optional, if not included defaults to true.
    metadata : str
        Metadata stored by the game developer which may include properties such as what version 
        of the game this file is compatible with.

    """
    def __init__(self, **attrs):
        self.version = attrs.pop("version")
        self.changelog = attrs.pop("changelog")
        self.active = attrs.pop("active", True)
        self.metadata_blob = attrs.pop("metadata")

    def _file_hash(self, file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def add_file(self, path):
        """Used to add a file.

        Parameters
        -----------
        path : str
            Path to file, if on windows must be \\ escaped.

        """
        self.file = open(path, "rb")
        self.filehash = self._file_hash(path)

        return self

class Filter:
    """This class is unique to the library and is an attempt to make filtering
    modio data easier. Instead of passing filter keywords directly you can pass
    an instance of this class which you have previously fine tuned through the
    various methods. For advanced users it is also possible to pass filtering
    arguments directly to the class given that they are already in modio format.
    If you don't know the modio format simply use the methods, all method return
    self for fluid chaining. This is also used for sorting and pagination.

    Parameters
    ----------
    filter : dict
        A dict which contains modio filter keyword and the appropriate value.

    """
    def __init__(self, filter={}):
        for key, value in filter:
            self.__setattr__(key, value)

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
        for key, value in kwargs:
            self.__setattr__(key, value)
        return self

    def not_equals(self, **kwargs):
        """Where the preceding column value does not equal the value specified. There are not set parameters, 
        this methods takes any named keywords and transforms them into arguments that will be passed to 
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-not", value)
        return self

    def like(self, **kwargs):
        """Where the string supplied matches the preceding column value. This is equivalent to SQL's LIKE. 
        Consider using wildcard's * for the best chance of results as described below. There are not set parameters, 
        this methods takes any named keywords and transforms them into arguments that will be passed to 
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-lk", value)
        return self

    def not_like(self, **kwargs):
        """Where the string supplied does not match the preceding column value. This is equivalent to SQL's 
        NOT LIKE. This is equivalent to SQL's LIKE. Consider using wildcard's * for the best chance of results 
        as described below. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-not-lk", value)
        return self

    def in_text(self, **kwargs):
        """Where the supplied list of values appears in the preceding column value. This is equivalent 
        to SQL's IN. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-in", value)
        return self

    def not_in_text(self, **kwargs):
        """Where the supplied list of values does not equal the preceding column value. This is equivalent 
        to SQL's NOT IN. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-not-in", value)
        return self

    def max(self, **kwargs):
        """Where the preceding column value is smaller than or equal to the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-max", value)
        return self

    def min(self, **kwargs):
        """Where the preceding column value is greater than or equal to the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-min", value)
        return self

    def smaller_than(self, **kwargs):
        """Where the preceding column value is smaller than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-st", value)
        return self

    def greater_than(self, **kwargs):
        """Where the preceding column value is greater than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-gt", value)
        return self

    def bitwise(self, **kwargs):
        """Some columns are stored as bits within an integer. You can combine any number of options for the column
        of the object you are querying. This is dependent on which item is being queried. These can be added together
        to check for multiple options at once. E.g if Option A: 1 and Option B: 2 then submitting 3 will return items
        that have both option A and B enabled.
        """
        for key, value in kwargs:
            self.__setattr__(f"{key}-bitwise-and", value)
        return self

    def sort(self, key, reverse=False):
        """Allows you to sort the results by the value of a top level column with a single value.

        Paramters
        ----------
        key : str
            The column by which to sort the results
        reverse : bool
            Optional, defaults to False. Whether to sort by ascending (False) or descending (True)
            order.

        """
        self._sort = text if not reverse else f"-{text}"
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

        Paramters
        ----------
        offset : int
            The number of results to skip.
        """
        self._offset = offset
        return self



class Object:
    """A dud class that can be used to replace other classes, keyword arguments
    passed will become attributes.

    """
    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __str__(self):
        return str(self.__dict__)

