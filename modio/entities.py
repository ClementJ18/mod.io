"""Module for miscs objects."""
import time

from .mixins import OwnerMixin, RatingMixin, ReportMixin, StatsMixin
from .errors import modioException
from .utils import concat_docs, _convert_date
from .enums import EventType, RatingType, TargetPlatform, VirusStatus


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
        return f"<Message code={self.code}>"


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
        A link to a smaller version of the image, processed by  Size varies based
        on the object being processed. Can be None.
    medium : str
        A link to a medium version of the image, processed by  Size varies based
        on the object being processed. Can be None.
    large : str
        A link to a large version of the image, processed by  Size varies based
        on the object being processed. Can be None.

    """

    def __init__(self, **attrs):
        self.filename = attrs.pop("filename")
        self.original = attrs.pop("original")

        self.small = list(attrs.values())[2] if len(attrs) > 2 else None
        self.medium = list(attrs.values())[3] if len(attrs) > 3 else None
        self.large = list(attrs.values())[4] if len(attrs) > 4 else None

    def __repr__(self):
        return f"<Image filename={self.filename} original={self.original}>"


class Event:
    """Represents a mod event.

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

    Attributes
    -----------
    id : int
        Unique ID of the event. Filter attribute.
    mod : int
        ID of the mod this event is from. Filter attribute.
    user : int
        ID of the user that made the change. Filter attribute.
    date : datetime.datetime
        UNIX timestamp of the event occurrence. Filter attribute.
    type : EventType
        Type of the event. Filter attribute.
    game_id : int
        ID of the game that the mod the user change came from. Can be None if it is
        a mod event. Filter attribute.

    """

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.date = _convert_date(attrs.pop("date_added"))
        self._raw_type = attrs.pop("event_type")
        self.mod = attrs.pop("mod_id")
        self.user = attrs.pop("user_id")
        self.game_id = attrs.pop("game_id", None)

    @property
    def type(self):
        if self._raw_type.startswith("MOD"):
            return EventType[self._raw_type.replace("MOD_", "").replace("MOD", "").lower()]

        return EventType[self._raw_type.replace("USER_", "").lower()]

    def __repr__(self):
        return f"<Event id={self.id} type={self.type.name} mod={self.mod}>"


class Comment:
    """Represents a comment on a mod page.

    Attributes
    -----------
    id : int
        ID of the comment. Filter attribute.
    resource_id : int
        The parent resource. Filter attribute.
    user : User
        Istance of the user that submitted the comment. Filter attribute.
    date : datetime.datetime
        Unix timestamp of date the comment was posted. Filter attribute.
    parent_id : int
        ID of the parent this comment is replying to. 0 if comment
        is not a reply. Filter attribute.
    position : int
        The position of the comment. Filter attribute. How it works:
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
    children : List[Comment]
        List of comment replying to this one
    level : int
        The level of nesting from 1 to 3 where one is top level and three is
        the deepest level
    """

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.resource_id = attrs.pop("resource_id")
        self.date = _convert_date(attrs.pop("date_added"))
        self.parent_id = attrs.pop("reply_id")
        self.position = attrs.pop("thread_position")
        self.level = len(self.position.split("."))
        self.karma = attrs.pop("karma")
        self.content = attrs.pop("content")
        self.connection = attrs.pop("connection")
        self.mod = attrs.pop("mod")
        self.submitter = User(connection=self.connection, **attrs.pop("user"))
        self.children = []

    def __repr__(self):
        return f"<Comment id={self.id} mod={self.mod.id} karma={self.karma}>"

    def edit(self, content):
        """Update the contents of a comment.

        |coro|

        Parameters
        ----------
        content : str
            The new content of the comment

        Returns
        --------
        Comment
            The comment with the new content
        """
        comment = self.connection.put_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}", data={"content": content}
        )
        return self.__class__(connection=self.connection, mod=self.mod, **comment)

    async def async_edit(self, content):
        comment = await self.connection.async_put_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}", data={"content": content}
        )
        return self.__class__(connection=self.connection, mod=self.mod, **comment)

    def delete(self):
        """Remove the comment.

        |coro|"""
        resp = self.connection.delete_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}"
        )
        return resp

    async def async_delete(self):
        """Remove the comment.

        |coro|"""
        resp = await self.connection.async_delete_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}"
        )
        return resp

    def _add_karma(self, karma: bool):
        comment = self.connection.post_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}/karma",
            data={"karma": 1 if karma else -1},
        )
        return Comment(connection=self.connection, mod=self.mod, **comment)

    async def _async_add_karma(self, karma: bool):
        comment = await self.connection.async_post_request(
            f"/games/{self.mod.game_id}/mods/{self.mod.id}/comments/{self.id}/karma",
            data={"karma": 1 if karma else -1},
        )
        return Comment(connection=self.connection, mod=self.mod, **comment)

    def add_positive_karma(self):
        """Add positive karma to the comment

        |coro|

        Returns
        --------
        Comment
            The updated comment
        """
        return self._add_karma(True)

    async def async_add_positive_karma(self):
        return await self._async_add_karma(True)

    def add_negative_karma(self):
        """Add negative karma to the comment

        |coro|

        Returns
        --------
        Comment
            The updated comment
        """
        return self._add_karma(False)

    async def async_add_negative_karma(self):
        return await self._async_add_karma(False)


class ModFile(OwnerMixin):
    """A object to represents modfiles. If the modfile has been returned for the me/modfile endpoint
    then edit() and delete() cannot be called as a game is lacking.

    Attributes
    -----------
    id : int
        ID of the modfile. Filter attribute.
    mod : int
        ID of the mod it was added for. Filter attribute.
    date : datetime.datetime
        UNIX timestamp of the date the modfile was submitted. Filter attribute.
    scanned : datetime.datetime
        UNIX timestamp of the date the file was virus scanned. Filter attribute.
    virus_status : VirusStatus
        Current status of the virus scan for the file. Filter attribute.
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
    url : str
        url to download file
    date_expires : datetime.datetime
        UNIX timestamp of when the url expires
    game_id : int
        ID of the game of the mod this file belongs to. Can be None if this file
        was returned from the me/modfiles endpoint.
    platforms : List[Platform]
        List of platforms this file is avalaible on.
    """

    _resource_type = "files"

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.mod = attrs.pop("mod_id")
        self.date = attrs.pop("date_added")
        self.scanned = attrs.pop("date_scanned")
        self.virus_status = VirusStatus(attrs.pop("virus_status"))
        self.virus = bool(attrs.pop("virus_positive"))
        self.virus_hash = attrs.pop("virustotal_hash")
        self.size = attrs.pop("filesize")
        self.hash = attrs.pop("filehash")["md5"]
        self.filename = attrs.pop("filename")
        self.version = attrs.pop("version")
        self.changelog = attrs.pop("changelog")
        self.metadata = attrs.pop("metadata_blob")
        download = attrs.pop("download")
        self.url = download["binary_url"]
        self.date_expires = _convert_date(download.pop("date_expires"))
        self.game_id = attrs.pop("game_id", None)
        self.platforms = [Platform(**platform) for platform in attrs.pop("platforms")]
        self.connection = attrs.pop("connection")

    def __repr__(self):
        return f"<ModFile id={self.id} name={self.filename} version={self.version}>"

    def edit(self, **fields):
        """Edit the file's details. Returns an updated
        instances of the file.

        |coro|

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

        Returns
        --------
        ModFile
            The updated file
        """
        if not self.game_id:
            raise modioException(
                "This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint"
            )

        file_json = self.connection.put_request(
            f"/games/{self.game_id}/mods/{self.mod}/files/{self.id}", data=fields
        )

        return self.__class__(connection=self.connection, game_id=self.game_id, **file_json)

    async def async_edit(self, **fields):
        if not self.game_id:
            raise modioException(
                "This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint"
            )

        file_json = await self.connection.async_put_request(
            f"/games/{self.game_id}/mods/{self.mod}/files/{self.id}", data=fields
        )

        return self.__class__(connection=self.connection, game_id=self.game_id, **file_json)

    def delete(self):
        """Deletes the modfile, this will raise an error if the
        file is the active release for the mod.

        |coro|

        Raises
        -------
        Forbidden
            You cannot delete the active release of a mod
        """
        if not self.game_id:
            raise modioException(
                "This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint"
            )

        resp = self.connection.delete_request(f"/games/{self.game_id}/mods/{self.mod}/files/{self.id}")
        return resp

    async def async_delete(self):
        if not self.game_id:
            raise modioException(
                "This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint"
            )

        resp = await self.connection.async_delete_request(
            f"/games/{self.game_id}/mods/{self.mod}/files/{self.id}"
        )
        return resp

    def url_is_expired(self):
        """Check if the url is still valid for this modfile.

        Returns
        -------
        bool
            True if it's still valid, else False
        """
        return self.date_expires.timestamp() < time.time()


class ModMedia:
    """Represents all the media for a mod.

    Attributes
    -----------
    youtube : List[str]
        A list of youtube links
    sketchfab : List[str]
        A list of SketchFab links
    images : List[Image]
        A list of image objects (gallery)

    """

    def __init__(self, **attrs):
        self.youtube = attrs.pop("youtube")
        self.sketchfab = attrs.pop("sketchfab")
        self.images = [Image(**image) for image in attrs.pop("images", [])]


class Platform:
    """A platform

    Attributes
    ----------
    platform : TargetPlatform
        The platform
    label : str
        The human readable platform label
    moderated : bool
        Whether the platform is moderated by game admins
    """

    def __init__(self, **attrs):
        self.platform = TargetPlatform[attrs.pop("platform")]
        self.label = attrs.pop("label")
        self.moderated = attrs.pop("moderated")


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
    locked : bool
        Whether or not mods can self assign from this tag option.
    tags : List[str]
        Array of tags for this group

    """

    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.type = attrs.pop("type", "dropdown")
        self.hidden = attrs.pop("hidden", False)
        self.locked = attrs.pop("locked", False)
        self.tags = attrs.pop("tags", [])

    def __repr__(self):
        return f"<TagOption name={self.name} hidden={self.hidden} locked=>"


class Rating(RatingMixin):
    """Represents a rating, objects obtained from the get_my_ratings endpoint

    Attributes
    -----------
    game_id : int
        The ID of the game the rated mod is for.
    mod_id : int
        The ID of the mod that was rated
    rating : RatingType
        The rating type
    date : datetime.datetime
        UNIX timestamp of whe the rating was added

    """

    mod_key = "mod_id"

    def __init__(self, **attrs):
        self.game_id = attrs.pop("game_id")
        self.mod_id = attrs.pop("mod_id")
        self.rating = RatingType(attrs.pop("rating"))
        self.date = _convert_date(attrs.pop("date_added"))
        self.connection = attrs.pop("connection")

    def __repr__(self) -> str:
        return f"< Rating mod_id={self.mod_id} rating={self.rating}>"


class ModStats(StatsMixin):
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
    date_expires : datetime.datetime
        Unix timestamp until this mods's statistics are considered stale. Endpoint
        should be polled again when this expires.
    """

    def __init__(self, **attrs):
        self.id = attrs.pop("mod_id")
        self.rank = attrs.pop("popularity_rank_position")
        self.rank_total = attrs.pop("popularity_rank_total_mods")
        self.downloads = attrs.pop("downloads_total")
        self.subscribers = attrs.pop("subscribers_total")
        self.date_expires = _convert_date(attrs.pop("date_expires"))
        self.total = attrs.pop("ratings_total")
        self.positive = attrs.pop("ratings_positive")
        self.negative = attrs.pop("ratings_negative")
        self.percentage = attrs.pop("ratings_percentage_positive")
        self.weighted = attrs.pop("ratings_weighted_aggregate")
        self.text = attrs.pop("ratings_display_text")


class GameStats(StatsMixin):
    """A stat object containing the stats specific to games

    Attributes
    -----------
    id : int
        The id of the game
    mods_count_total : int
        The total count of mods for this game
    mods_download_today : int
        The amount of mod downloaded today
    mods_download_total : int
        The amount of mods downloaded all times
    mods_download_daily_avg : int
        Average daily mod downlaods
    mods_subscribers_total : int
        Total amount of subscribers to all mods
    date_expires : datetime.datetime
        The date at which the stats are considered "stale"
        and no longer accurate.
    """

    def __init__(self, **attrs):
        self.id = attrs.pop("game_id")
        self.mods_count_total = attrs.pop("mods_count_total")
        self.mods_downloads_today = attrs.pop("mods_downloads_today")
        self.mods_downloads_total = attrs.pop("mods_downloads_total")
        self.mods_downloads_daily_avg = attrs.pop("mods_downloads_daily_average")
        self.mods_subscribers_total = attrs.pop("mods_subscribers_total")
        self.date_expires = _convert_date(attrs.pop("date_expires"))


class Theme:
    """Object representing a game's theme. This is mostly useful
    if you desire to create a visual interface for a game or
    one of its mods. All attributes are hex color codes.

    Attributes
    -----------
    primary : string
        Primary color of the game
    dark : string
        The "dark" color of the game
    light : string
        The "light" color of the game
    success : string
        The color of a successful action with
        the game interface
    warning : string
        The color of a warning with the
        game interface
    danger : string
        The color of a danger warning with
        the game interface
    """

    def __init__(self, **attrs):
        self.primary = attrs.pop("primary")
        self.dark = attrs.pop("dark")
        self.light = attrs.pop("light")
        self.success = attrs.pop("success")
        self.warning = attrs.pop("warning")
        self.danger = attrs.pop("danger")

    def __repr__(self):
        return f"< Theme primary={self.primary} >"


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

    date : datetime.datetime
        Unix timestamp of date tag was added.
    tag : str
        String representation of the tag.
    """


class MetaData:
    """mod.io MetaData objects are represented as dictionnaries and are returned
    as such by the function of this library, each entry of in the dictionnary
    is composed of the metakey as the key and the metavalue as the value.
    """


class Dependencies:
    """mod.io Depedencies objects are represented as dictionnaries and are returned
    as such by the function of this library, each entry of in the dictionnary
    is composed of the dependency (mod) id as the key and the date_added as the value. Use
    dict.keys() to access dependencies as a list.

    """


class User(ReportMixin):
    """Represents a modio user.

    Attributes
    ----------
    id : int
        ID of the user. Filter attribute.
    name_id : str
        Subdomain name of the user. For example: https://mod.io/members/username-id-here. Filter attribute.
    username : str
        Name of the user. Filter attribute.
    last_online : datetime.datetime
        Unix timestamp of date the user was last online.
    avatar : Image
        Contains avatar data
    tz : str
        Timezone of the user, format is country/city. Filter attribute.
    lang : str
        Users language preference. See localization for the supported languages. Filter attribute.
    profile : str
        URL to the user's mod.io profile.

    """

    _resource_type = "users"

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.name_id = attrs.pop("name_id")
        self.username = attrs.pop("username")
        self.last_online = _convert_date(attrs.pop("date_online"))

        avatar = attrs.pop("avatar")
        if avatar:
            self.avatar = Image(**avatar)
        else:
            self.avatar = None

        self.tz = attrs.pop("timezone")
        self.lang = attrs.pop("language")
        self.profile = attrs.pop("profile_url")
        self.connection = attrs.pop("connection")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

    def mute(self):
        """Mute a user, this will hide all mods authored by them from
        the authenticated user.

        |coro|
        """
        return self.connection.post_request(f"/users/{self.id}/mute")

    async def async_mute(self):
        return await self.connection.async_post_request(f"/users/{self.id}/mute")

    def unmute(self):
        """Unmute a user, this will show all mods authored by them from
        the authenticated user.

        |coro|
        """
        return self.connection.delete_request(f"/users/{self.id}/mute")

    async def async_unmute(self):
        return await self.connection.async_delete_request(f"/users/{self.id}/mute")


@concat_docs
class TeamMember(User):
    """Inherits from User. Represents a user as part of a team.
    Filter-Only Attributes
    -----------------------
    These attributes can only be used at endpoints which return instances
    of this class and takes filter arguments. They are not attached to the
    object itself and trying to access them will cause an AttributeError

    user_id : int
        Unique id of the user.
    username : str
        Username of the user.

    Attributes
    -----------
    team_id : int
        The id of the user in the context of their team, not the same as
        user id. Filter attribute.
    level : Level
        Permission level of the user
    date : datetime.datetime
        Unix timestamp of the date the user was added to the team. Filter attribute.
    position : str
        Custom title given to the user in this team. Filter attribute.
    mod : Mod
        The mod object the team is attached to.

    """

    def __init__(self, **attrs):
        self.connection = attrs.pop("connection")
        super().__init__(**attrs.pop("user"), connection=self.connection)
        self.team_id = attrs.pop("id")
        self.level = attrs.pop("level")
        self.date = attrs.pop("date_added")
        self.position = attrs.pop("position")
        self.mod = attrs.pop("mod")

    def __repr__(self):
        return f"<TeamMember team_id={self.team_id} id={self.id} level={self.level}>"
