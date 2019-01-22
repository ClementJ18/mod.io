from .errors import modioException

import hashlib
import enum
from collections import namedtuple
import time


Returned = namedtuple("Returned", "results pagination")

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

    def __str__(self):
        return f"{self.code} : {self.message}"

    def __repr__(self):
        return f"<modio.Message code={self.code}>"

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

    def __repr__(self):
        return f"<modio.Image filename={self.filename} original={self.original}>"    

class EventType(enum.Enum):
    """An enum to render all event types easy to compare."""
    file_changed  = 0
    available     = 1
    unavailable   = 2
    edited        = 3
    deleted       = 4
    team_changed  = 5
    team_join     = 6
    team_leave    = 7
    subscribe     = 8
    unsubscribe   = 9
    other         = 10    

class Event:
    """Represents a mod event. 

    Attributes
    -----------
    id : int
        Unique ID of the event. Filter attribute.
    mod : int
        ID of the mod this event is from. Filter attribute.
    user : int
        ID of the user that made the change. Filter attribute.
    date : int
        UNIX timestamp of the event occurrence. Filter attribute.
    type : enum.EventType
        Type of the event. Filter attribute.

    Filter-Only Attributes
    -----------------------
    These attributes can only be used at endpoints which return instances
    of this class and takes filter arguments. They are not attached to the
    object itself and trying to access them will cause an AttributeError

    latest : bool
        Returns only the latest unique events, which is useful for checking 
        if the primary modfile has changed.
    subscribed : bool
        Returns only events connected to mods the authenticated user is 
        subscribed to, which is useful for keeping the users mods up-to-date.

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.date = attrs.pop("date_added")
        self._raw_type = attrs.pop("event_type")
        self.mod = attrs.pop("mod_id")
        self.user = attrs.pop("user_id")

    @property
    def type(self):
        if self._raw_type.startswith("MOD"):
            return EventType[self._raw_type.replace("MOD_", "").replace("MOD", "").lower()]
        else:
            return EventType[self._raw_type.replace("USER_", "").lower()]

    def __repr__(self):
        return f"<modio.Event id={self.id} type={self.type.name} mod={self.mod}>"

class Comment:
    """Represents a comment on a mod page.

    Attributes
    -----------
    id : int
        ID of the comment. Filter attribute.
    mod : id
        ID of the mod this comment is from. Filter attribute.
    submitter : modio.User
        Istance of the user that submitted the comment. Filter attribute.
    date : int
        Unix timestamp of date the comment was posted. Filter attribute.
    parent : int
        ID of the parent this comment is replying to. 0 if comment
        is not a reply. Filter attribute.
    position : str
        Level of nesting. Filter attribute. How it works:
        - The first comment will have the position '01'.
        - The second comment will have the position '02'.
        - If someone responds to the second comment the position will be '02.01'.
        - A maximum of 3 levels is supported.
    karma : int
        Total karma received for the comment. Filter attribute.
    karma_guest : int
        Total karma received from guests for this comment
    content : str
        Content of the comment. Filter attribute.
    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.mod = attrs.pop("mod_id")
        self.submitter = User(**attrs.pop("submitter"))
        self.date = attrs.pop("date_added")
        self.parent = attrs.pop("reply_id")
        self.position = attrs.pop("thread_position")
        self.karma = attrs.pop("karma")
        self.karma_guest = attrs.pop("karma_guest")
        self.content = attrs.pop("content")
        self._client = attrs.pop("client")
        self._mod = attrs.pop("mod")

    def __repr__(self):
        return f"<modio.Comment id={self.id} mod={self.mod}>"

    async def delete(self):
        """Remove the comment

        This function is a coroutine"""
        r = self._client._delete_request(f'/games/{self._mod.game}/mods/{self._mod.id}/comments/{self.id}')
        return r

class ModFile:
    """A object to represents modfiles. If the modfile has been returned for the me/modfile endpoint
    then edit() and delete() cannot be called as a game is lacking.

    Attributes
    -----------
    id : int
        ID of the modfile. Filter attribute.
    mod : int
        ID of the mod it was added for. Filter attribute.
    date : int
        UNIX timestamp of the date the modfile was submitted. Filter attribute.
    scanned : int
        UNIX timestamp of the date the file was virus scanned. Filter attribute.
    virus_status : int
        Current status of the virus scan for the file. Filter attribute.
        0 : Not scanned
        1 : Scan complete
        2 : In progress
        3 : Too large to scan
        4 : File not found
        5 : Error Scanning
    virus : bool
        True if a virus was detected, False if it wasn't. Filter attribute.
    virus_hash : str
        VirusTotal proprietary hash to view the scan results.
    size : int
        Size of the file in bytes. Filter attribute.
    hash : str
        MD5 hash of the file. Filter attribute.
    filename : str
        Name of the file. Filter attribute.
    version : str
        Version of the file. Filter attribute.
    changelog : str
        Changelog for the file. Filter attribute.
    metadata : str
        Metadata stored by the game developer for this file. Filter attribute.
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
        self.virus_status = attrs.pop("virus_status")
        self.virus = bool(attrs.pop("virus_positive"))
        self.virus_hash = attrs.pop("virustotal_hash")
        self.size = attrs.pop("filesize")
        self.hash = attrs.pop("filehash")["md5"]
        self.filename = attrs.pop("filename")
        self.version = attrs.pop("version")
        self.changelog = attrs.pop("changelog")
        self.metadata = attrs.pop("metadata_blob")
        self.download = attrs.pop("download")
        self._game_id = attrs.pop("game_id", None)
        self._client = attrs.pop("client")

    def __repr__(self):
        return f"<modio.ModFile id={self.id} name={self.filename} version={self.version}>"

    async def get_owner(self):
        """Returns the original submitter of the resource.

        This function is a coroutine

        Returns
        --------
        User
            User that submitted the resource
        """
        user_json = self._client._post_request(f"/general/ownership", data={"resource_type" : "files", "resource_id" : self.id})
        return User(**user_json)

    async def edit(self, **fields):
        """Edit the file's details.

        This function is a coroutine

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
        if not self._game_id:
            raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")

        file_json = self._client._put_request(f'/games/{self._game_id}/mods/{self.mod}/files/{self.id}', data = fields)
        self.__init__(client=self._client, game_id=self._game_id, **file_json)

    async def delete(self):
        """Deletes the modfile, this will raise an error if the
        file is the active release for the mod.

        This function is a coroutine

        Raises
        -------
        Forbidden
            You cannot delete the active release of a mod
        """
        if not self._game_id:
            raise modioException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")
            
        r = await self._client._delete_request(f'/games/{self._game_id}/mods/{self.mod}/files/{self.id}')
        return r

    def url_expired(self):
        """Check if the url is still valid for this modfile

        Returns
        -------
        bool
            True if it's still valid, else False
        """
        return self.download["date_expires"] <= time.time()

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
        self.type = attrs.pop("type", "dropdown")
        self.hidden = attrs.pop("hidden", False)
        self.tags = attrs.pop("tags", [])

    def __repr__(self):
        return f"<modio.TagOption name={self.name} hidden={self.hidden}>"

class RatingType(enum.Enum):
    good    = 1
    neutral = 0
    bad     = -1

class Rating:
    """Represents a rating, objects obtained from the get_my_ratings endpoint

    Attributes
    -----------
    game : int
        The ID of the game the rated mod is for.
    mod : int
        The ID of the mod that was rated
    rating : RatingType
        The rating type
    date : int
        UNIX timestamp of whe the rating was added

    """
    def __init__(self, **attrs):
        self.game = attrs.pop("game_id")
        self.mod = attrs.pop("mod_id")
        self.rating = RatingType(attrs.pop("rating"))
        self.date = attrs.pop("date_added")
        self._client = attrs.pop("client")

    async def delete(self):
        """Sets the rating to neutral."""
        raise NotImplementedError("WIP")

    async def _add_rating(self, rating : RatingType):
        try:
            checked = await self._client._post_request(f'/games/{self.game}/mods/{self.mod}/ratings', data={"rating":rating.value})
        except BadRequest:
            return False

        await self.get_stats()
        return True

    async def add_positive_rating(self):
        """Changes the mod rating to positive, the author of the rating will be the authenticated user.
        If the mod has already been positevely rated by the user it will return False. If the positive rating
        is successful it will return True

        This function is a coroutine"""
        return await self._add_rating(RatingType.good)

    async def add_negative_rating(self):
        """Changes the mod rating to negative, the author of the rating will be the authenticated user.
        If the mod has already been negatively rated by the user it will return False. If the negative rating
        is successful it will return True.

        This function is a coroutine"""
        return await self._add_rating(RatingType.bad)


class Stats:
    """Represents a summary of stats for a mod

    Attributes
    -----------
    id : int
        Mod ID of the stats. Filter attribute.
    rank : int
        Current rank of the mod. Filter attribute.
    rank_total : int
        Number of ranking spots the current rank is measured against. Filter attribute
    downloads : int
        Amount of times the mod was downloaded. Filter attribute
    subscribers : int
        Amount of subscribers. Filter attribute
    total : int
        Number of times this item has been rated. 
    positive : int
        Number of positive ratings. Filter attribute
    negative : int
        Number of negative ratings. Filter attribute
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
    expires : int
        Unix timestamp until this mods's statistics are considered stale. Endpoint
        should be polled again when this expires.
    """
    def __init__(self, **attrs):
        self.id = attrs.pop("mod_id")
        self.rank = attrs.pop("popularity_rank_position")
        self.rank_total = attrs.pop("popularity_rank_total_mods")
        self.downloads = attrs.pop("downloads_total")
        self.subscribers = attrs.pop("subscribers_total")
        self.expires = attrs.pop("date_expires")
        self.total = attrs.pop("ratings_total")
        self.positive = attrs.pop("ratings_positive")
        self.negative = attrs.pop("ratings_negative")
        self.percentage = attrs.pop("ratings_percentage_positive")
        self.weighted = attrs.pop("ratings_weighted_aggregate")
        self.text = attrs.pop("ratings_display_text")

    def __repr__(self):
        return f"<modio.Stats id={self.id} expired={self.is_stale()}>"

    def is_stale(self):
        """Returns a bool depending on whether or not the stats are considered stale.

        Returns
        --------
        bool
            True if stats are expired, False else.
        """
        return time.time() <= self.expires

class Tag:
    """mod.io Tag objects are represented as dictionnaries and are returned
    as such by the function of this library, each entry of in the dictionnary
    is composed of the tag name as the key and the date_added as the value. Use
    dict.keys() to access tags as a list.

    Filter-Only Attributes
    -----------------------
    These attributes can only be used at endpoints which return instances
    of this class and takes filter arguments. They are not attached to the
    object itself and trying to access them will cause an AttributeError

    date : int
        Unix timestamp of date tag was added.
    tag : str
        String representation of the tag.
    """
    pass

class MetaData:
    """mod.io MetaData objects are represented as dictionnaries and are returned
    as such by the function of this library, each entry of in the dictionnary
    is composed of the metakey as the key and the metavalue as the value.
    """
    pass

class Dependencies:
    """mod.io Depedencies objects are represented as dictionnaries and are returned
    as such by the function of this library, each entry of in the dictionnary
    is composed of the dependency (mod) id as the key and the date_added as the value. Use
    dict.keys() to access dependencies as a list.

    """
    pass

class User:
    """Represents a modio user.

    Attributes
    ----------
    id : int
        ID of the user. Filter attribute.
    name_id : str
        Subdomain name of the user. For example: https://mod.io/members/username-id-here. Filter attribute.
    username : str
        Name of the user. Filter attribute.
    last_online : int
        Unix timestamp of date the user was last online.
    avatar : modio.Image
        Contains avatar data
    tz : str
        Timezone of the user, format is country/city. Filter attribute.
    lang : str
        Users language preference. See localization for the supported languages. Filter attribute.
    profile : str
        URL to the user's mod.io profile.

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.name_id = attrs.pop("name_id")
        self.username = attrs.pop("username")
        self.last_online = attrs.pop("date_online")

        avatar = attrs.pop("avatar")

        if len(avatar.keys()) > 0:
            self.avatar = Image(**avatar)
        else:
            self.avatar = None

        self.tz = attrs.pop("timezone")
        self.lang = attrs.pop("language")
        self.profile = attrs.pop("profile_url")

    def __repr__(self):
        return f"<modio.User id={self.id} username={self.username}>"

class TeamMember(User):
    """Inherits from modio.User. Represents a user as part of a team.
    
    Attributes
    -----------
    team_id : int
        The id of the user in the context of their team, not the same as
        user id. Filter attribute.
    level : int
        Level of permissions the user has. Filter attribute.
        1 : Moderator
        4 : Creator
        8 : Administrator
    date : int
        Unix timestamp of the date the user was added to the team. Filter attribute.
    position : str
        Custom title given to the user in this team. Filter attribute.

    Filter-Only Attributes
    -----------------------
    These attributes can only be used at endpoints which return instances
    of this class and takes filter arguments. They are not attached to the
    object itself and trying to access them will cause an AttributeError

    user_id : int
        Unique id of the user.  
    username : str
        Username of the user. 

    """
    def __init__(self, **attrs):
        super().__init__(**attrs.pop("user"))
        self.team_id = attrs.pop("id")
        self.level = attrs.pop("level")
        self.date = attrs.pop("date_added")
        self.position = attrs.pop("position")
        self._client = attrs.pop("client")
        self._mod = attrs.pop("mod")

    def __repr__(self):
        return f"<modio.TeamMember team_id={self.team_id} id={self.id} level={self.level}>"

    async def edit(self, *, level=None, position=None):
        """Edit a team member's details.

        This function is a coroutine

        Parameters
        -----------
        level : Optional[int]
            Level of permissions the user has
            1 : Moderator
            4 : Creator
            8 : Administrator
        position : Optional[str]
            Custom title given to the user in this team.

        """
        data = {"level" : level, "position" : position}
        msg = self._client._put_request(f'/games/{self._mod.game}/mods/{self._mod.id}/team/{self.team_id}', data=data)
        return Message(**msg)

    async def delete(self):
        """Remove the user from the team. Fires a MOD_TEAM_CHANGED event.

        This function is a coroutine"""
        r = self._client._delete_request(f'/games/{self._mod.game}/mods/{self._mod.id}/team/{self.team_id}')
        return r
    

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
    description :str
        Detailed description of the mod, supports HTML.
    homepage : Optional[str]
        Official homepage for your mod. Must be a valid URL. Optional
    stock : int
        Maximium number of subscribers for this mod. Optional, if not included disables
    metadata : Optional[str]
        Metadata stored by developers which may include properties on how information 
        required. Optional.
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
    def __init__(self, filters={}):
        for key, value in filters.items():
            self._set(key, value)

    def _set(self, key, value, text="{}"):
        _lib_to_api = {
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
            "game" : "game_id",
            "live" : "date_live",
            "updated" : "date_updated",
            "team_id" : "id",
            "kvp" : "metadata_kvp",
            "expires" : "date_expires",
            "mod" : "mod_id",
            "file" : "modfile",
            "virus" : "virus_positive",
            "size" : "filesize",
            "hash" : "filehash",
            "rank" : "popularity_rank_position",
            "rank_total" : "popularity_rank_position",
            "downloads" : "downloads_total",
            "subscribers" : "subscribers_total",
            "positive" : "ratings_positive",
            "negative": "ratings_negative",
            "sort_downloads" : "downloads",
            "sort_popular" : "popular",
            "sort_subscribers" : "subscribers",
            "sort_rating" : "rating",
            "member_id" : "id",
            "parent" : "reply_id",
            "position": "thread_position",
            "tz" : "timezone",
            "lang": "language"
        }

        try:
            key = _lib_to_api[key]
        except KeyError:
            pass

        if key == "event_type":
            if value.value < 6:
                value = f"MOD{'_' if value != EventType.file_changed else ''}{value.name.upper()}"
            else:
                value = f"USER_{value.name.upper()}"

        self.__setattr__(text.format(key), value)

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
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-max")
        return self

    def min(self, **kwargs):
        """Where the preceding column value is greater than or equal to the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-min")
        return self

    def smaller_than(self, **kwargs):
        """Where the preceding column value is smaller than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
        """
        for key, value in kwargs.items():
            self._set(key, value, "{}-st")
        return self

    def greater_than(self, **kwargs):
        """Where the preceding column value is greater than the value specified. There are not set 
        parameters, this methods takes any named keywords and transforms them into arguments that will be passed 
        to the request. E.g. 'game=40'
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

        Paramters
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
        Total number of results avalaible for that endpoint
    """

    def __init__(self, **attrs):
        self.count = attrs.pop("result_count")
        self.limit = attrs.pop("result_limit")
        self.offset = attrs.pop("result_offset")
        self.total = attrs.pop("result_total")

    def __repr__(self):
        return f"<modio.Pagination count={self.count} limit={self.limit} offset={self.offset}>"

    def max(self):
        """Returns True if there are no additional results after this set. Can fail if the returned count is coincidentally
        exactly the same as the limit."""
        return (self.offset + self.count) == self.total

    def min(self):
        """Returns True if there are no additional results before this set."""
        return self.offset == 0

    def next(self):
        """Returns the offset required for the next set of results"""
        return self.offset + self.limit

    def previous(self):
        """Returns the offset required for the previous set of results"""
        return self.offset - self.limit

    def page(self):
        """Returns the current page number. Page numbers start at 0"""
        return self.offset // self.limit


class Object:
    """A dud class that can be used to replace other classes, keyword arguments
    passed will become attributes.

    """
    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __repr__(self):
        return str(self.__dict__)

