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
        self.message = attrs.pop("message")

    def __repr__(self):
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
    file_changed  = 0
    available     = 1
    unavailable   = 2
    edited        = 3
    deleted       = 4
    team_changed  = 5
    other         = 6    

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
        self.date = attrs.pop("date_addedy")

class ModFile:
    """A object to represents modfiles. If the modfile has been returned for the me/modfile endpoint
    then edit() and delete() cannot be called as a game_id is lacking.

    Attributes
    -----------
    id : int
        ID of the modfile
    mod : int
        ID of the mod it was added for
    date : int
        UNIX timestamp of the date the modfile was submitted
    scanned : int
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
    game : int
        ID of the game of the mod this file belongs to. Can be None if this file
        was returned from the me/modfiles endpoint.
    """
    def __init__(self,**attrs):
        self.id = attrs.pop("id")
        self.mod = attrs.pop("mod_id")
        self.date = attrs.pop("date_added")
        self.scanned = attrs.pop("date_scanned")
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
        self.game = attrs.pop("game_id", None)
        self.client = attrs.pop("client", None)

    def edit(self, **fields):
        """Edit the file's details

        Parameters
        -----------
        version : str
            Change the release version of the file
        changelog : str
            Change the changelog of this release
        active : bool
            Change whether or not this is the active version.
        metadata_blob : str
            Metadata stored by the game developer which may include 
            properties such as what version of the game this file is compatible with.
        """
        if not self.game:
            raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")

        file_json = self.client._put_request(f'/games/{self.game_id}/mods/{self.mod_id}/files/{self.id}', data = fields)
        self.__init__(client=self.client, game_id=self.game, **file_json)

    def delete(self):
        """Deletes the modfile, this will raise an error if the
        file is the active release for the mod

        Raises
        -------
        Forbidden
            You cannot delete the active release of a mod
        """
        if not self.game:
            raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")
            
        r = requests.delete(f'/games/{self.game_id}/mods/{self.mod_id}/files/{self.id}')
        return r

    def url_expired(self):
        """Check if the url is still valid for this modfile

        Returns
        -------
        bool
            True if it's still valid, else False
        """
        return self.download["binary_url"] <= time.time()

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

class Tag:
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

    def __repr__(self):
        return self.name    

class TagOption:
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

    def __repr__(self):
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

class Stats:
    """Represents a summary of stats for a mod

    Attributes
    -----------
    id : int
        Mod ID of the stats
    rank : int
        Current rank of the mod
    rank_total : int
        Number of ranking spots the current rank is measured against
    downloads : int
        Amount of times the mod was downloaded
    subscribers : int
        Amount of subscribers
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
    date : int
        Unix timestamp until this mods's statistics are considered stale. Endpoint
        should be polled again when this expires.
    """
    def __init__(self, **attrs):
        self.id = kwargs.pop("mod_id")
        self.rank = kwargs.pop("popularity_rank_position")
        self.rank_total = kwargs.pop("popularity_rank_total_mods")
        self.downloads = kwargs.pop("downloads_total")
        self.subscribers = kwargs.pop("subscribers_total")
        self.date = kwargs.pop("date_expires")
        self.total = attrs.pop("ratings_total")
        self.positive = attrs.pop("ratings_positive")
        self.negative = attrs.pop("ratings_negative")
        self.percentage = attrs.pop("ratings_percentage_positive")
        self.weighted = attrs.pop("ratings_weighted_aggregate")
        self.text = attrs.pop("ratings_display_text")

    def is_stale(self):
        """Returns a bool depending on whether or not the stats are considered stale.

        Returns
        --------
        bool
            True if stats are expired, False else.
        """
        return time.time() <= self.date

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
        self.profile = attrs.pop("profile_url")

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

class NewModFile:
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
    filters : Optional[dict]
        A dict which contains modio filter keyword and the appropriate value.

    """
    def __init__(self, filter={}):
        for key, value in filters.items():
            self.__setattr__(key, value)

        self._lib_to_api = {
            "date" : "date_added",
            "metadata" : "metadata_blob",
            "key" : "metakey",
            "value" : "metavalue",
            "maturity": "maturity_option",
            "type" : "event_type",
            "presentation" : "presentation_option",
            "curation" : "curation_option",
            "community" : "community_options",
            "submission" : "submission_option",
            "revenue" : "revenue_options",
            "api" : "api_access_options",
            "ugc" : "ugc_name",
            "profile" : "profile_url",
            "homepage" : "homepage_url",
            "submitter" : "submitted_by",
            "game" : "game_id"


        }

    def _set(self, key, value):
        try:
            key = self._lib_to_api[key]
        except KeyError:
            pass

        if key == "event_type":
            value = f"MOD{'_' if value != EventType.file_changed else ''}{value.name.upper()}"

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
        for key, value in kwargs.items():
            self._set(key, value)
        return self

    def not_equals(self, **kwargs):
        """Where the preceding column value does not equal the value specified. There are not set parameters, 
        this methods takes any named keywords and transforms them into arguments that will be passed to 
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-not", value)
        return self

    def like(self, **kwargs):
        """Where the string supplied matches the preceding column value. This is equivalent to SQL's LIKE. 
        Consider using wildcard's * for the best chance of results as described below. There are not set parameters, 
        this methods takes any named keywords and transforms them into arguments that will be passed to 
        the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-lk", value)
        return self

    def not_like(self, **kwargs):
        """Where the string supplied does not match the preceding column value. This is equivalent to SQL's 
        NOT LIKE. This is equivalent to SQL's LIKE. Consider using wildcard's * for the best chance of results 
        as described below. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-not-lk", value)
        return self

    def in_text(self, **kwargs):
        """Where the supplied list of values appears in the preceding column value. This is equivalent 
        to SQL's IN. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"
        """
        for key, value in kwargs.items():
            self._set(f"{key}-in", value)
        return self

    def not_in_text(self, **kwargs):
        """Where the supplied list of values does not equal the preceding column value. This is equivalent 
        to SQL's NOT IN. There are not set parameters, this methods takes any named keywords and transforms 
        them into arguments that will be passed to the request. E.g. 'id=10' or 'name="Best Mod"
        """
        for key, value in kwargs.items():
            self._set(f"{key}-not-in", value)
        return self

    def max(self, **kwargs):
        """Where the preceding column value is smaller than or equal to the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-max", value)
        return self

    def min(self, **kwargs):
        """Where the preceding column value is greater than or equal to the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-min", value)
        return self

    def smaller_than(self, **kwargs):
        """Where the preceding column value is smaller than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-st", value)
        return self

    def greater_than(self, **kwargs):
        """Where the preceding column value is greater than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(f"{key}-gt", value)
        return self

    def bitwise(self, **kwargs):
        """Some columns are stored as bits within an integer. You can combine any number of options for the column
        of the object you are querying. This is dependent on which item is being queried. These can be added together
        to check for multiple options at once. E.g if Option A: 1 and Option B: 2 then submitting 3 will return items
        that have both option A and B enabled.
        """
        for key, value in kwargs.items():
            self._set(f"{key}-bitwise-and", value)
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

    def __repr__(self):
        return str(self.__dict__)

