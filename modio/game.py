"""Games are the umbrella entities under which all mods are stored."""
import json
from typing import List, Literal, Optional

from .mod import Mod
from .entities import Event, Image, Message, GameStats, ModStats, Platform, TagOption, User
from .objects import Filter, NewMod, Pagination, Returned
from .utils import _convert_date, find
from .enums import APIAccess, Community, Curation, MaturityOptions, Presentation, Revenue, Status, Submission
from .mixins import OwnerMixin, ReportMixin


class Game(ReportMixin, OwnerMixin):
    """Represents an instance of a Game. Do not create manually.

    Attributes
    -----------
    id : int
        ID of the game. Filter attribute.
    status : Status
        Status of the game. (see `status and visibility <https://docs.mod.io/#status-amp-visibility>`_ for details) Filter attribute.
    submitter : Optional[User]
        Instance of the modio user who submitted the game. Filter
        attribute.
    date : datetime.datetime
        UNIX timestamp of the date the game was registered. Filter attribute.
    updated : datetime.datetime
        UNIX timestamp of the date the game was last updated. Filter attribute.
    live : datetime.datetime
        UNIX timestamp of the date the game went live. Filter attribute.
    presentation : Presentation
        Presentation style used on the mod.io website. Filter attribute.
    submission : Submission
        Submission process modders must follow. Filter attribute.
    curation : Curation
        Curation process used to approve mods. Filter attribute.
    community : Community
        Community features enabled on the mod.io website. Filter attribute.
    revenue : Revenue
        Revenue capabilities mods can enable. Filter attribute.
    api : APIAccess
        Level of API access allowed by this game. Filter attribute.
    maturity_options : MaturityOptions
        Switch to allow developers to select if they flag their mods as containing mature
        content. Filter attribute.
    ugc : str
        Word used to describe user-generated content (mods, items, addons etc).
        Filter attribute.
    icon : Image
        The game icon
    logo : Image
        The game logo
    header : Image
        The game header
    name : str
        Name of the game. Filter attribute.
    name_id : str
        sub_domain name for the game (https://name_id.mod.io). Filter attribute.
    summary : str
        Summary of the game. Filter attribute.
    instructions : str
        Instructions on uploading mods for this game, only applicable
        if :attr:`submission` equals 0
    instructions_url : str
        Link to a mod.io guide, your modding wiki or a page where modders can learn how to
        make and submit mods to your games profile. Filter attribute.
    profile : str
        URL to the game's mod.io page.
    tag_options : List[TagOption]
        List of tags from which mods can pick
    stats : Optional[GameStats]
        The game stats
    other_urls : Dict[str, str]
        A dictionnary of labels and urls for
        the game
    platforms : List[Platform]
        Platforms this games supports
    """

    _resource_type = "games"

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.status = Status(attrs.pop("status"))
        self.date = _convert_date(attrs.pop("date_added"))
        self.updated = _convert_date(attrs.pop("date_updated"))
        self.live = _convert_date(attrs.pop("date_live"))
        self.presentation = Presentation(attrs.pop("presentation_option"))
        self.submission = Submission(attrs.pop("submission_option"))
        self.curation = Curation(attrs.pop("curation_option"))
        self.community = Community(attrs.pop("community_options"))
        self.revenue = Revenue(attrs.pop("revenue_options"))
        self.api = APIAccess(
            attrs.pop(
                "api_access_options",
            )
        )
        self.ugc = attrs.pop("ugc_name")
        self.icon = Image(**attrs.pop("icon", None))
        self.logo = Image(**attrs.pop("logo", None))
        self.header = Image(**attrs.pop("header", None))
        self.homepage = attrs.pop("homepage", None)
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id")
        self.summary = attrs.pop("summary")
        self.instructions = attrs.pop("instructions", None)
        self.instructions_url = attrs.pop("instructions_url", None)
        self.profile = attrs.pop("profile_url")
        self.tag_options = [TagOption(**tag) for tag in attrs.pop("tag_options", [])]
        self.maturity_options = MaturityOptions(attrs.pop("maturity_options"))
        self.connection = attrs.pop("connection")
        self.submitter = None
        self.stats = None
        # self.theme = Theme(**attrs.pop("theme"))
        self.other_urls = {value["label"]: value["url"] for value in attrs.pop("other_urls")}
        self.platforms = [Platform(**platform) for platform in attrs.pop("platforms")]

        _submitter = attrs.pop("submitted_by", {})
        if _submitter:
            self.submitter = User(connection=self.connection, **_submitter)

        _stats = attrs.pop("stats", {})
        if _stats:
            self.stats = GameStats(**_stats)

    def __repr__(self):
        return f"<Game id={self.id} name={self.name}>"

    def get_mod(self, mod_id: int) -> Mod:
        """Queries the mod.io API for the given mod ID and if found returns it as a
        Mod instance. If not found raises NotFound.

        |coro|

        Parameters
        -----------
        mod_id : int
            The ID of the mod to query the API for

        Raises
        -------
        NotFound
            A mod with the supplied id was not found.

        Returns
        --------
        :class: `Mod`
            The mod with the given ID

        """
        mod_json = self.connection.get_request(f"/games/{self.id}/mods/{mod_id}")
        return Mod(connection=self.connection, **mod_json)

    async def async_get_mod(self, mod_id: int) -> Mod:
        mod_json = await self.connection.async_get_request(f"/games/{self.id}/mods/{mod_id}")
        return Mod(connection=self.connection, **mod_json)

    def get_mods(self, *, filters: Filter = None) -> Returned[Mod]:
        """Gets all the mods available for the game. Returns a
        named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filters : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Mod], Pagination]
            The results and pagination tuple from this request

        """
        mod_json = self.connection.get_request(f"/games/{self.id}/mods", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    async def async_get_mods(self, *, filters: Filter = None) -> Returned[Mod]:
        mod_json = await self.connection.async_get_request(f"/games/{self.id}/mods", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    def get_mod_events(self, *, filters: Filter = None) -> Returned[Event]:
        """Gets all the mod events available for this game sorted by latest event first. |filterable|

        |coro|

        Parameters
        -----------
        filters : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Event], Pagination]
            The results and pagination tuple from this request

        """
        event_json = self.connection.get_request(f"/games/{self.id}/mods/events", filters=filters)

        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    async def async_get_mod_events(self, *, filters: Filter = None) -> Returned[Event]:
        event_json = await self.connection.async_get_request(f"/games/{self.id}/mods/events", filters=filters)
        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    def get_tag_options(self, *, filters: Filter = None):
        """Gets all the game tags available for this game. Updates the tag_option attribute. |filterable|

        |coro|

        Parameters
        -----------
        filters : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[TagOption], Pagination]
            The results and pagination tuple from this request

        """
        tag_json = self.connection.get_request(f"/games/{self.id}/tags", filters=filters)
        self.tag_options = tags = [TagOption(**tag_option) for tag_option in tag_json["data"]]
        return Returned(tags, Pagination(**tag_json))

    async def async_get_tag_options(self, *, filters: Filter = None):
        tag_json = await self.connection.async_get_request(f"/games/{self.id}/tags", filters=filters)
        self.tag_options = tags = [TagOption(**tag_option) for tag_option in tag_json["data"]]
        return Returned(tags, Pagination(**tag_json))

    def get_stats(self, *, filters: Filter = None):
        """Get the stats for the game. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        GameStats
            The stats for the game.
        """

        stats_json = self.connection.get_request(f"/games/{self.id}/stats", filters=filters)
        return GameStats(**stats_json)

    async def async_get_stats(self, *, filters: Filter = None):
        stats_json = await self.connection.async_get_request(f"/games/{self.id}/stats", filters=filters)
        return GameStats(**stats_json)

    def get_mods_stats(self, *, filters: Filter = None):
        """Gets the stat for all the mods of this game. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[ModStats], Pagination]
            The results and pagination tuple from this request
        """
        stats_json = self.connection.get_request(f"/games/{self.id}/mods/stats", filters=filters)
        return Returned([ModStats(**stats) for stats in stats_json["data"]], Pagination(**stats_json))

    async def async_get_mods_stats(self, *, filters: Filter = None):
        stats_json = await self.connection.async_get_request(f"/games/{self.id}/mods/stats", filters=filters)
        return Returned([ModStats(**stats) for stats in stats_json["data"]], Pagination(**stats_json))

    def add_mod(self, mod: NewMod) -> Mod:
        """Add a mod to this game.

        |coro|

        Parameters
        -----------
        mod : NewMod
            The mod to be submitted

        Raises
        -------
        ValueError
            One of the requirements for a parameter has not been met.

        Returns
        --------
        Mod
            The newly created mod
        """
        mod_d = mod.__dict__.copy()
        tags = list(mod_d.pop("tags"))
        for index, tag in enumerate(tags):
            mod_d[f"tags[{index}]"] = tag

        with open(mod_d.pop("logo"), "rb") as f:
            mod_json = self.connection.post_request(
                f"/games/{self.id}/mods", h_type=1, data=mod_d, files={"logo": f}
            )

        return Mod(connection=self.connection, **mod_json)

    async def async_add_mod(self, mod: NewMod) -> Mod:
        mod_d = mod.__dict__.copy()
        tags = list(mod_d.pop("tags"))
        for index, tag in enumerate(tags):
            mod_d[f"tags[{index}]"] = tag

        with open(mod_d.pop("logo"), "rb") as f:
            mod_json = await self.connection.async_post_request(
                f"/games/{self.id}/mods", h_type=1, data=mod_d, files={"logo": f}
            )

        return Mod(connection=self.connection, **mod_json)

    def add_media(self, *, logo: str = None, icon: str = None, header: str = None):
        """Upload new media to to the game. This function can take between 1 to 3 arguments
        depending on what media you desire to upload/update.

        |coro|

        Parameters
        -----------
        logo : Optional[str]
            Path to the file that you desire to be the game's logo. Dimensions must be at least
            640x360 and we recommended you supply a high resolution image with a 16 / 9 ratio. mod.io
            will use this logo to create three thumbnails with the dimensions of 320x180, 640x360 and
            1280x720.
        icon : Optional[str]
            Path to the file that you desire to be the game's icon. Must be gif, jpg or png format
            and cannot exceed 1MB in filesize. Dimensions must be at least 64x64 and a transparent
            png that works on a colorful background is recommended. mod.io will use this icon to
            create three thumbnails with the dimensions of 64x64, 128x128 and 256x256.
        header : Optional[str]
            Path to the file that you desire to be the game's header. Must be gif, jpg or png format
            and cannot exceed 256KB in filesize. Dimensions of 400x100 and a light transparent png that
            works on a dark background is recommended.

        Returns
        --------
        Message
            A message containing the result of the query if successful.
        """
        media = {}
        if logo:
            media["logo"] = open(logo, "rb")

        if icon:
            media["icon"] = open(icon, "rb")

        if header:
            media["header"] = open(header, "rb")

        try:
            message = self.connection.post_request(f"/games/{self.id}/media", h_type=1, files=media)
        finally:
            for image in media.values():
                image.close()

        return Message(**message)

    async def async_add_media(self, *, logo: str = None, icon: str = None, header: str = None):
        media = {}
        if logo:
            media["logo"] = open(logo, "rb")

        if icon:
            media["icon"] = open(icon, "rb")

        if header:
            media["header"] = open(header, "rb")

        try:
            message = await self.connection.async_post_request(
                f"/games/{self.id}/media", h_type=1, files=media
            )
        finally:
            for image in media.values():
                image.close()

        return Message(**message)

    def add_tag_options(
        self,
        name: str,
        *,
        tags: Optional[List[str]] = None,
        hidden: Optional[bool] = False,
        locked: Optional[bool] = False,
        tag_type: Optional[Literal["dropdown", "checkboxes"]] = "dropdown",
    ):
        """Add tags which mods can apply to their profiles. If the tag names already exists,
        settings such as hidden or type will be overwritten to the values provided and all the
        tags will be added to the group.

        |coro|

        Parameters
        -----------
        name : str
            Name of the tag group
        type : Optional[Literal['dropdown', 'checkboxes']]
            Defaults to dropdown
            dropdown : Mods can select only one tag from this group, dropdown menu shown on site profile.
            checkboxes : Mods can select multiple tags from this group, checkboxes shown on site profile.
        hidden : Optional[bool]
            Whether or not this group of tags should be hidden from users and mod devs. Defaults to False
        locked : Optional[bool]
            Whether or not mods can assign from this group of tag to themselves. If locked only game admins
            will be able to assign the tag. Defaults to False.
        tags : Optional[List[str]]
            Array of tags that mod creators can apply to their mod
        """
        if tags is None:
            tags = []

        tags = {f"tags[{index}]": tag for index, tag in enumerate(tags)}
        tags = {
            "name": name,
            "type": tag_type,
            "hidden": json.dumps(hidden),
            "locked": json.dumps(locked),
            **tags,
        }
        message = self.connection.post_request(f"/games/{self.id}/tags", data=tags)

        tag_option = find(self.tag_options, name=name)
        if not tag_option:
            self.tag_options.append(TagOption(**tags))
        else:
            tag_option.type = tag_type
            tag_option.hidden = hidden
            tag_option.tags.extend(tags)

        return Message(**message)

    async def async_add_tag_options(
        self,
        name: str,
        *,
        tags: Optional[List[str]] = None,
        hidden: Optional[bool] = False,
        locked: Optional[bool] = False,
        tag_type: Optional[Literal["dropdown", "checkboxes"]] = "dropdown",
    ):
        if tags is None:
            tags = []

        tags = {f"tags[{index}]": tag for index, tag in enumerate(tags)}
        tags = {
            "name": name,
            "type": tag_type,
            "hidden": json.dumps(hidden),
            "locked": json.dumps(locked),
            **tags,
        }
        message = await self.connection.async_post_request(f"/games/{self.id}/tags", data=tags)

        tag_option = find(self.tag_options, name=name)
        if not tag_option:
            self.tag_options.append(TagOption(**tags))
        else:
            tag_option.type = tag_type
            tag_option.hidden = hidden
            tag_option.tags.extend(tags)

        return Message(**message)

    def delete_tag_options(self, name: str, *, tags: Optional[List[str]] = None) -> bool:
        """Delete one or more tags from a tag option.

        |coro|

        Parameters
        -----------
        name : str
            Name of the group from which you wish to delete from
        tags : Optional[List[str]]
            Optional. Tags to delete from group. If left blank the entire group will be
            deleted

        Returns
        --------
        bool
            Returns True if the tags were sucessfully removed, False if the requests was
            sucessful but the tags was not removed (if the tag wasn't part of the option.)
        """
        data = {f"tags[{index}]": tag for index, tag in enumerate(tags)} if tags else {"tags[]": ""}
        data["name"] = name

        resp = self.connection.delete_request(f"/games/{self.id}/tags", data=data)

        option = find(self.tag_options, name=name)
        if tags:
            option.tags = [tag for tag in option.tags if tag not in tags]
        else:
            self.tag_options.remove(option)

        return not isinstance(resp, dict)

    async def async_delete_tag_options(self, name: str, *, tags: Optional[List[str]] = None) -> bool:
        data = {f"tags[{index}]": tag for index, tag in enumerate(tags)} if tags else {"tags[]": ""}
        data["name"] = name

        resp = await self.connection.async_delete_request(f"/games/{self.id}/tags", data=data)

        option = find(self.tag_options, name=name)
        if tags:
            option.tags = [tag for tag in option.tags if tag not in tags]
        else:
            self.tag_options.remove(option)

        return not isinstance(resp, dict)
