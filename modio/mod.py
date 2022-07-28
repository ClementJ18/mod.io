"""Module storing representation of the mod objects"""
from typing import List, Optional, Union
from .enums import Level, Maturity, Status, Visibility
from .errors import modioException
from .mixins import OwnerMixin, RatingMixin, ReportMixin
from .entities import (
    Comment,
    Event,
    Image,
    Message,
    ModFile,
    ModMedia,
    ModStats,
    TeamMember,
    User,
)
from .objects import Filter, NewModFile, Pagination, Returned
from .utils import _convert_date, _clean_and_convert


class Mod(ReportMixin, RatingMixin, OwnerMixin):
    """Represent a modio mod object.

    Filter-Only Attributes
    -----------------------
    These attributes can only be used at endpoints which return instances
    of this class and takes filter arguments. They are not attached to the
    object itself and trying to access them will cause an AttributeError

    sort_downloads : str
        Sort argument, provide to sort function to sort by most/least
        downloaded
    sort_popular : str
        Sort argument, provide to sort function to sort by most/least
        popular
    sort_rating : str
        Sort argument, provide to sort function to sort by weighed
        rating
    sort_subscribers : str
        Sort argument, provide to sort function to sort by most/least
        subscribers

    Attributes
    -----------
    id : int
        ID of the mod. Filter attribute.
    status : Status
        Status of the mod. Filter attribute.
    visible : Visibility
        Visibility of the mod. Filter attribute.
    game_id : int
        ID of the game the mod is for. Filter attribute.
    submitter : User
        Instance of the modio User that submitted the mod. Filter attribute.
    date : datetime.datetime
        UNIX timestamp of the date the mod was registered. Filter attribute.
    updated : datetime.datetime
        UNIX timestamp of the date the mod was last updated. Filter attribute.
    live : datetime.datetime
        UNIX timestamp of the date the mod went live. Filter attribute.
    logo : Image
        The mod logo
    homepage : str
        Link to the homepage of the mod, can be None. Filter attribute.
    name : str
        Name of the mod. Filter attribute.
    name_id : str
        sub_domain mod for the game (https://game_name.mod.io/name_id). Filter
        attribute.
    summary : str
        Summary of the mod. Filter attribute.
    description :str
        Detailed description of the mod, supports HTML. Filter attribute.
    metadata : str
        Metadata stored by developers which may include properties on how information
        required. Can be None. Filter attribute.
    maturity : Maturity
        Maturity option of the mod. Filter attribute.
    profile : str
        URL of the mod's modio profile
    file : ModFile
        Latest released instance. Can be None. Filter attribute.
    media : ModMedia
        Contains mod media data (links and images)
    stats : ModStats
        Summary of all stats for this mod
    tags : dict
        Tags for this mod. Filter attribute.
    kvp : dict
        Contains key-value metadata. Filter attribute.
    plaintext : str
        description field converted into plaintext.
    """

    _resource_type = "mods"
    mod_key = "id"

    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.status = Status(attrs.pop("status"))
        self.visible = Visibility(attrs.pop("visible"))
        self.game_id = attrs.pop("game_id")
        # self.game_name = attrs.pop("game_name")
        self.date = _convert_date(attrs.pop("date_added"))
        self.updated = _convert_date(attrs.pop("date_updated"))
        self.live = _convert_date(attrs.pop("date_live"))
        self.logo = Image(**attrs.pop("logo"))
        self.homepage = attrs.pop("homepage_url", None)
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id")
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description")
        self.metadata = attrs.pop("metadata_blob")
        self.profile = attrs.pop("profile_url")
        self.media = ModMedia(**attrs.pop("media"))
        self.maturity = Maturity(attrs.pop("maturity_option"))
        self.stats = ModStats(**attrs.pop("stats"))
        self.tags = {tag["name"]: tag["date_added"] for tag in attrs.pop("tags", [])}
        self.connection = attrs.pop("connection")
        self._file = attrs.pop("modfile", None)
        self._kvp_raw = attrs.pop("metadata_kvp")
        self.file = (
            ModFile(**self._file, game_id=self.game_id, connection=self.connection) if self._file else None
        )
        self.submitter = User(connection=self.connection, **attrs.pop("submitted_by"))
        self.plaintext = attrs.pop("description_plaintext")

    @property
    def kvp(self):
        meta = {}
        for item in self._kvp_raw:
            if item["metakey"] not in meta:
                meta[item["metakey"]] = []

            meta[item["metakey"]].append(item["metavalue"])

        return meta

    def __repr__(self):
        return f"<Mod id={self.id} name={self.name} game_id={self.game_id}>"

    def get_file(self, file_id: int) -> ModFile:
        """Get the Mod File with the following ID.

        |coro|

        Parameters
        -----------
        file_id : int
            ID of the mod file you wish to retrieve

        Raises
        -------
        NotFound
            A mod with that ID has not been found

        Returns
        -------
        ModFile
            The found modfile
        """
        file_json = self.connection.get_request(f"/games/{self.game_id}/mods/{self.id}/files/{file_id}")
        return ModFile(**file_json, game_id=self.game_id, connection=self.connection)

    async def async_get_file(self, file_id: int) -> ModFile:
        file_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/files/{file_id}"
        )
        return ModFile(**file_json, game_id=self.game_id, connection=self.connection)

    def get_files(self, *, filters: Filter = None) -> Returned[ModFile]:
        """Get all mod files for this mod. Returns a named tuple
        with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[ModFile], Pagination]
            The results and pagination tuple from this request
        """
        files_json = self.connection.get_request(
            f"/games/{self.game_id}/mods/{self.id}/files", filters=filters
        )
        return Returned(
            [
                ModFile(**file, game_id=self.game_id, connection=self.connection)
                for file in files_json["data"]
            ],
            Pagination(**files_json),
        )

    async def async_get_files(self, *, filters: Filter = None) -> Returned[ModFile]:
        files_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/files", filters=filters
        )
        return Returned(
            [
                ModFile(**file, game_id=self.game_id, connection=self.connection)
                for file in files_json["data"]
            ],
            Pagination(**files_json),
        )

    def get_events(self, *, filters: Filter = None) -> Returned[Event]:
        """Get all events for that mod sorted by latest. Returns,
        a named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Event], Pagination]
            The results and pagination tuple from this request

        """
        event_json = self.connection.get_request(
            f"/games/{self.game_id}/mods/{self.id}/events", filters=filters
        )
        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    async def async_get_events(self, *, filters: Filter = None) -> Returned[Event]:
        event_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/events", filters=filters
        )
        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    def get_tags(self, *, filters: Filter = None) -> Returned[dict]:
        """Gets all the tags for this mod. Updates the instance's
        tag attribute. Returns a named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Tag], Pagination]
            The results and pagination tuple from this request

        """
        tag_json = self.connection.get_request(f"/games/{self.game_id}/mods/{self.id}/tags", filters=filters)
        self.tags = new_tags = {tag["name"]: _convert_date(tag["date_added"]) for tag in tag_json["data"]}
        return Returned(new_tags, Pagination(**tag_json))

    async def async_get_tags(self, *, filters: Filter = None) -> Returned[dict]:
        tag_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/tags", filters=filters
        )
        self.tags = new_tags = {tag["name"]: _convert_date(tag["date_added"]) for tag in tag_json["data"]}
        return Returned(new_tags, Pagination(**tag_json))

    def get_metadata(self) -> Returned[dict]:
        """Returns a dict of metakey-metavalue pairs. This will also update the mod's kvp attribute.

        |coro|

        Returns
        --------
        Returned[List[MetaData], Pagination]
            The results and pagination tuple from this request
        """
        meta_json = self.connection.get_request(f"/games/{self.game_id}/mods/{self.id}/metadatakvp")
        self._kvp_raw = meta_json["data"]
        return Returned(self.kvp, Pagination(**meta_json))

    async def async_get_metadata(self) -> Returned[dict]:
        meta_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/metadatakvp"
        )
        self._kvp_raw = meta_json["data"]
        return Returned(self.kvp, Pagination(**meta_json))

    def get_dependencies(self, *, filters: Filter = None) -> Returned[dict]:
        """Returns a dict of dependency_id-date_added pairs. Returns
        a named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Dependency], Pagination]
            The results and pagination tuple from this request

        """
        depen_json = self.connection.get_request(
            f"/games/{self.game_id}/mods/{self.id}/dependencies", filters=filters
        )
        return Returned(
            {dependecy["mod_id"]: _convert_date(dependecy["date_added"]) for dependecy in depen_json["data"]},
            Pagination(**depen_json),
        )

    async def async_get_dependencies(self, *, filters: Filter = None) -> Returned[dict]:
        depen_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/dependencies", filters=filters
        )
        return Returned(
            {dependecy["mod_id"]: _convert_date(dependecy["date_added"]) for dependecy in depen_json["data"]},
            Pagination(**depen_json),
        )

    def get_team(self, *, filters: Filter = None) -> Returned[TeamMember]:
        """Returns a list of TeamMember object representing the Team in charge of the mod. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[TeamMember], Pagination]
            The results and pagination tuple from this request

        """
        team_json = self.connection.get_request(f"/games/{self.game_id}/mods/{self.id}/team", filters=filters)
        return Returned(
            [TeamMember(**member, connection=self.connection, mod=self) for member in team_json["data"]],
            Pagination(**team_json),
        )

    async def async_get_team(self, *, filters: Filter = None) -> Returned[TeamMember]:
        team_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/team", filters=filters
        )
        return Returned(
            [TeamMember(**member, connection=self.connection, mod=self) for member in team_json["data"]],
            Pagination(**team_json),
        )

    def get_comments(self, *, filters: Filter = None) -> Returned[Comment]:
        """Returns a list of all the top level comments for this mod wih comments replying
        to top level comments stored in the children attribute. This can be flattened using
        the utils.flatten function. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Comment], Pagination]
            The results and pagination tuple from this request
        """
        comment_json = self.connection.get_request(
            f"/games/{self.game_id}/mods/{self.id}/comments", filters=filters
        )
        return Returned(
            [Comment(**comment, connection=self.connection, mod=self) for comment in comment_json["data"]],
            Pagination(**comment_json),
        )

    async def async_get_comments(self, *, filters: Filter = None) -> Returned[Comment]:
        comment_json = await self.connection.async_get_request(
            f"/games/{self.game_id}/mods/{self.id}/comments", filters=filters
        )
        return Returned(
            [Comment(**comment, connection=self.connection, mod=self) for comment in comment_json["data"]],
            Pagination(**comment_json),
        )

    def add_comment(self, content: str, *, reply: int = None) -> Comment:
        """Add a comment to the mod page. You can specify a comment to reply too.

        |coro|

        Parameters
        -----------
        content : str
            The content of the comment
        reply : Optional[Comment]
            The comment to reply to

        Returns
        -------
        Comment
            The comment created
        """
        data = {"content": content}
        if reply:
            data["reply_id"] = reply.id

        comment = self.connection.post_request(f"/games/{self.game_id}/mods/{self.id}/comments", data=data)
        return Comment(connection=self.connection, mod=self, **comment)

    async def async_add_comment(self, content: str, *, reply: int = None) -> Comment:
        data = {"content": content}
        if reply:
            data["reply_id"] = reply.id

        comment = await self.connection.async_post_request(
            f"/games/{self.game_id}/mods/{self.id}/comments", data=data
        )
        return Comment(connection=self.connection, mod=self, **comment)

    def get_stats(self) -> ModStats:
        """Returns a ModStats object, representing a series of stats for the mod.

        |coro|

        Returns
        -------
        Stats
            The stats summary object for the mod.
        """
        stats_json = self.connection.get_request(f"/games/{self.game_id}/mods/{self.id}/stats")
        self.stats = stats = ModStats(**stats_json)
        return stats

    async def async_get_stats(self) -> ModStats:
        stats_json = await self.connection.async_get_request(f"/games/{self.game_id}/mods/{self.id}/stats")
        self.stats = stats = ModStats(**stats_json)
        return stats

    def edit(self, **fields) -> "Mod":
        """Used to edit the mod details. Sucessful editing will return the updated mod.

        |coro|

        Parameters
        -----------
        status : Status
            For game admins only.
        visible : Visibility
            Modify the game visibility
        name : str
            Name of the mod, cannot exceed 80 characters
        name_id : str
            Subdomain for the mod, cannot exceed 80 characters
        summary : str
            Summary of the mod, cannot exceed 250 characters
        description : str
            Detailed description for your mod, which can include details such as
            'About', 'Features', 'Install Instructions', 'FAQ', etc. HTML supported
            and encouraged.
        homepage : str
            URL to the official homepage for this mod.
        stock : str
            Maximium number of subscribers for this mod. A value of 0 disables this limit.
        maturity : Maturity
            Maturity option of the mod.
        metadata : str
                Metadata stored by the mod developer which may include properties as to how
                the item works, or other information you need to display.

        Returns
        --------
        Mod
            The updated version of the mod
        """
        fields = _clean_and_convert(fields)
        mod_json = self.connection.put_request(f"/games/{self.game_id}/mods/{self.id}", data=fields)
        return self.__class__(connection=self.connection, **mod_json)

    async def async_edit(self, **fields) -> "Mod":
        fields = _clean_and_convert(fields)
        mod_json = await self.connection.async_put_request(
            f"/games/{self.game_id}/mods/{self.id}", data=fields
        )
        return self.__class__(connection=self.connection, **mod_json)

    def delete(self):
        """Delete a mod and set its status to deleted.

        |coro|
        """
        resp = self.connection.delete_request(f"/games/{self.game_id}/mods/{self.id}")
        self.status = 3
        return resp

    async def async_delete(self):
        resp = await self.connection.async_delete_request(f"/games/{self.game_id}/mods/{self.id}")
        self.status = 3
        return resp

    def add_file(self, file: NewModFile) -> ModFile:
        """Adds a new file to the mod, to do so first construct an instance of NewModFile
        and then pass it to the function.

        |coro|

        Parameters
        -----------
        file : NewModFile
            The mod file to upload

        Raises
        -------
        modioException
            file argument must be type NewModFile

        Returns
        --------
        ModFile
            The modfile after being processed by the mod.io API

        """
        file_d = file.__dict__.copy()
        file_file = file_d.pop("file")

        with open(file_file, "rb") as f:
            file_json = self.connection.post_request(
                f"/games/{self.game_id}/mods/{self.id}/files", h_type=1, data=file_d, files={"filedata": f}
            )

        return ModFile(**file_json, game_id=self.game_id, connection=self.connection)

    async def async_add_file(self, file: NewModFile) -> ModFile:
        file_d = file.__dict__.copy()
        file_file = file_d.pop("file")

        with open(file_file, "rb") as f:
            file_json = await self.connection.async_post_request(
                f"/games/{self.game_id}/mods/{self.id}/files", h_type=1, data=file_d, files={"filedata": f}
            )

        return ModFile(**file_json, game_id=self.game_id, connection=self.connection)

    def _prepare_media(self, logo, images, youtube, sketchfab):
        media = {}

        if logo:
            media["logo"] = open(logo, "rb")

        if isinstance(images, str):
            images_d = {"images": ("image.zip", open(images, "rb"))}
        elif isinstance(images, list):
            images_d = {f"image{index}": open(image, "rb") for index, image in enumerate(images)}

        yt = {f"youtube[{index}]": link for index, link in enumerate(youtube)}
        sketch = {f"sketchfab[{index}]": link for index, link in enumerate(sketchfab)}

        media = {**media, **images_d}
        links = {**yt, **sketch}

        return media, links

    def add_media(
        self,
        *,
        logo: Optional[str] = None,
        images: Optional[Union[str, List[str]]] = (),
        youtube: List[str] = (),
        sketchfab: List[str] = (),
    ):
        """Upload new media to the mod.

        |coro|

        Parameters
        -----------
        logo : Optional[str]
            Path to the logo file. If on windows, must be \\ escaped. Image file which will represent
            your mods logo. Must be gif, jpg or png format and cannot exceed 8MB in filesize. Dimensions
            must be at least 640x360 and we recommended you supply a high resolution image with a 16 / 9
            ratio. mod.io will use this logo to create three thumbnails with the dimensions of 320x180,
            640x360 and 1280x720.
        images : Optional[Union[str, list]]
            Can be either the path to a file called .zip file containing all the images or a list of paths to multiple
            image files. If on windows, must be \\ escaped. Only valid gif, jpg and png images in the zip file
            will be processed.
        youtube : Optional[List[str]]
            List of youtube links to be added to the gallery
        sketchfab : Optional[List[str]]
            List of sketchfab links to the be added to the gallery.

        Returns
        -------
        Message
            A message confirming the submission of the media
        """
        medias, links = self._prepare_media(logo, images, youtube, sketchfab)

        try:
            media_json = self.connection.post_request(
                f"/games/{self.game_id}/mods/{self.id}/media", h_type=1, files=medias, data=links
            )
        finally:
            for media in medias.values():
                if isinstance(media, tuple):
                    media[1].close()
                else:
                    media.close()

        return Message(**media_json)

    async def async_add_media(
        self,
        *,
        logo: Optional[str] = None,
        images: Optional[Union[str, List[str]]] = (),
        youtube: List[str] = (),
        sketchfab: List[str] = (),
    ):
        medias, links = self._prepare_media(logo, images, youtube, sketchfab)

        try:
            media_json = await self.connection.async_post_request(
                f"/games/{self.game_id}/mods/{self.id}/media", h_type=1, files=medias, data=links
            )
        finally:
            for media in medias.values():
                if isinstance(media, tuple):
                    media[1].close()
                else:
                    media.close()

        return Message(**media_json)

    def _prepare_delete_media(self, images, youtube, sketchfab):
        images = {f"images[{index}]": image for index, image in enumerate(images)}
        yt = {f"youtube[{index}]": link for index, link in enumerate(youtube)}
        sketch = {f"sketchfab[{index}]": link for index, link in enumerate(sketchfab)}
        fields = {**images, **yt, **sketch}

        return fields

    def delete_media(
        self,
        *,
        images: Optional[List[str]] = (),
        youtube: Optional[List[str]] = (),
        sketchfab: Optional[List[str]] = (),
    ):
        """Delete media from the mod page.

        |coro|

        Parameters
        -----------
        images : Optional[List[str]]
            Optional. List of image filenames that you want to delete
        youtube : Optional[List[str]]
            Optional. List of youtube links that you want to delete
        sketchfab : Optional[List[str]]
            Optional. List sketchfab links that you want to delete
        """

        resp = self.connection.delete_request(
            f"/games/{self.game_id}/mods/{self.id}/media",
            data=self._prepare_delete_media(images, youtube, sketchfab),
        )
        return resp

    async def async_delete_media(
        self,
        *,
        images: Optional[List[str]] = (),
        youtube: Optional[List[str]] = (),
        sketchfab: Optional[List[str]] = (),
    ):
        resp = await self.connection.async_delete_request(
            f"/games/{self.game_id}/mods/{self.id}/media",
            data=self._prepare_delete_media(images, youtube, sketchfab),
        )
        return resp

    def subscribe(self) -> "Mod":
        """Subscribe to the mod. Returns None if user is already subscribed.

        |coro|

        Returns
        --------
        Mod
            The mod that was just subscribed to, if the user was already subscribed it will return None
        """
        mod_json = self.connection.post_request(f"/games/{self.game_id}/mods/{self.id}/subscribe")
        return Mod(connection=self.connection, **mod_json)

    async def async_subscribe(self) -> "Mod":
        mod_json = await self.connection.async_post_request(f"/games/{self.game_id}/mods/{self.id}/subscribe")
        return Mod(connection=self.connection, **mod_json)

    def unsubscribe(self):
        """Unsubscribe from a mod. Returns None if the user is not subscribed.

        |coro|"""

        resp = self.connection.delete_request(f"/games/{self.game_id}/mods/{self.id}/subscribe")
        return resp

    async def async_unsubscribe(self):
        resp = await self.connection.async_delete_request(f"/games/{self.game_id}/mods/{self.id}/subscribe")
        return resp

    def add_tags(self, *tags: str):
        """Add tags to a mod, tags are case insensitive and duplicates will be removed. Tags
        which are not in the game's tag_options will not be added.

        |coro|

        Parameters
        -----------
        tags : List[str]
            list of tags to be added.

        """
        fields = {f"tags[{index}]": tag for index, tag in enumerate(tags)}

        message = self.connection.post_request(f"/games/{self.game_id}/mods/{self.id}/tags", data=fields)

        return Message(**message)

    async def async_add_tags(self, *tags: str):
        fields = {f"tags[{index}]": tag for index, tag in enumerate(tags)}

        message = await self.connection.async_post_request(
            f"/games/{self.game_id}/mods/{self.id}/tags", data=fields
        )

        return Message(**message)

    def delete_tags(self, *tags: str):
        """Delete tags from the mod, tags are case insensitive and duplicates will be removed. Providing
        no arguments will remove every tag from the mod.

        |coro|

        Parameters
        -----------
        tags : List[str]
            List of tags to remove, if no list is provided, will remove every tag from the mod.

        """
        fields = {f"tags[{index}]": tag for index, tag in enumerate(tags)} if tags else {"tags[]": ""}
        self.connection.delete_request(f"/games/{self.game_id}/mods/{self.id}/tags", data=fields)

    async def async_delete_tags(self, *tags: str):
        fields = {f"tags[{index}]": tag for index, tag in enumerate(tags)} if tags else {"tags[]": ""}
        await self.connection.async_delete_request(f"/games/{self.game_id}/mods/{self.id}/tags", data=fields)

    def add_metadata(self, **metadata):
        """Add metadate key-value pairs to the mod. To submit new meta data, pass meta data keys
        as keyword arguments and meta data value as a list of values. E.g pistol_dmg = [800, 400].
        Keys support alphanumeric, '-' and '_'. Total lengh of key and values cannot exceed 255
        characters. To add meta-keys which contain a dash in their name they must be passed as an
        upacked dictionnary.

        |coro|

        Example
        --------
        `mod.add_metadata(difficulty=["hard", "medium", "easy"])`
            This will add the values "hard", "medium" and "easy" to the meta key "difficulty"
        `mod.add_metadata(**{"test-var": ["test1", "test2", "test3"]})`
            This will add the values "test1", "test2" and "test3" to meta key "test-var"

        Returns
        --------
        Message
            message on the status of the successful added meta data
        """
        metadata_d = {}
        index = 0
        for key, values in metadata.items():
            metadata_d[f"metadata[{index}]"] = f"{key}:{':'.join(values)}"
            index += 1

        checked = self.connection.post_request(
            f"/games/{self.game_id}/mods/{self.id}/metadatakvp", data=metadata_d
        )

        for key, value in metadata.items():
            for item in value:
                self._kvp_raw.append({"metakey": key, "metavalue": item})

        return Message(**checked)

    async def async_add_metadata(self, **metadata):
        metadata_d = {}
        index = 0
        for key, values in metadata.items():
            metadata_d[f"metadata[{index}]"] = f"{key}:{':'.join(values)}"
            index += 1

        checked = await self.connection.async_post_request(
            f"/games/{self.game_id}/mods/{self.id}/metadatakvp", data=metadata_d
        )

        for key, value in metadata.items():
            for item in value:
                self._kvp_raw.append({"metakey": key, "metavalue": item})

        return Message(**checked)

    def delete_metadata(self, **metadata):
        """Deletes metadata from a mod. To do so pass the meta-key as a keyword argument and the
        meta-values you wish to delete as a list. You can pass an empty list in which case all
        meta-values for the meta-key will be deleted. To delete meta-keys which contain a dash in their
        name they must be passed as an upacked dictionnary.

        |coro|

        Example
        --------
        `mod.delete_metadata(difficulty=["easy"])`
            This will remove the value "easy" from the meta key "difficulty"
        `mod.delete_metadata(difficulty=[])`
            This will remove the meta key "difficulty"
        `mod.delete_metadata(**{"test-var": ["test1"]})`
            This will remove the value "test1" from the meta key "test-var"
        `mod.delete_metadata(**{"test-var":[]})`
            This will remove the meta key "test-var"

        """
        metadata_d = {}
        index = 0
        for key, values in metadata.items():
            metadata_d[f"metadata[{index}]"] = f"{key}{':' if len(values) > 0 else ''}{':'.join(values)}"
            index += 1

        resp = self.connection.delete_request(
            f"/games/{self.game_id}/mods/{self.id}/metadatakvp", data=metadata_d
        )

        for key, values in metadata.items():
            if not values:
                self._kvp_raw = [x for x in self._kvp_raw if x["metakey"] != key]
            else:
                self._kvp_raw = [
                    x for x in self._kvp_raw if x["metakey"] != key and x["metavalue"] not in values
                ]

        return resp

    async def async_delete_metadata(self, **metadata):
        metadata_d = {}
        index = 0
        for key, values in metadata.items():
            metadata_d[f"metadata[{index}]"] = f"{key}{':' if len(values) > 0 else ''}{':'.join(values)}"
            index += 1

        resp = await self.connection.async_delete_request(
            f"/games/{self.game_id}/mods/{self.id}/metadatakvp", data=metadata_d
        )

        for key, values in metadata.items():
            if not values:
                self._kvp_raw = [x for x in self._kvp_raw if x["metakey"] != key]
            else:
                self._kvp_raw = [
                    x for x in self._kvp_raw if x["metakey"] != key and x["metavalue"] not in values
                ]

        return resp

    def add_dependencies(self, dependencies: List[Union[int, "Mod"]]):
        """Add mod dependencies required by the corresponding mod. A dependency is a mod
        that should be installed for this mod to run.

        |coro|

        Parameters
        ----------
        dependencies : List[Union[int, Mod]]
            List of mod ids to submit as dependencies.

        """
        dependency = {
            f"dependencies[{index}]": getattr(data, "id", data) for index, data in enumerate(dependencies)
        }
        resp = self.connection.post_request(
            f"/games/{self.game_id}/mods/{self.id}/dependencies", data=dependency
        )
        return Message(**resp)

    async def async_add_dependencies(self, dependencies: List[Union[int, "Mod"]]):
        dependency = {
            f"dependencies[{index}]": getattr(data, "id", data) for index, data in enumerate(dependencies)
        }
        resp = await self.connection.async_post_request(
            f"/games/{self.game_id}/mods/{self.id}/dependencies", data=dependency
        )
        return Message(**resp)

    def delete_dependencies(self, dependencies: List[Union[int, "Mod"]]):
        """Delete mod dependecies required by this mod. You must
        supply at least one dependency.

        |coro|

        Parameters
        -----------
        dependencies : List[Union[int, Mod]]
            List of dependencies to remove
        """
        if not dependencies:
            raise modioException("Please supply at least on dependency to be deleted.")

        data = {
            f"dependencies[{index}]": getattr(data, "id", data) for index, data in enumerate(dependencies)
        }

        resp = self.connection.delete_request(f"/games/{self.game_id}/mods/{self.id}/dependencies", data=data)
        return resp

    async def async_delete_dependencies(self, dependencies: List[Union[int, "Mod"]]):
        if not dependencies:
            raise modioException("Please supply at least on dependency to be deleted.")

        data = {
            f"dependencies[{index}]": getattr(data, "id", data) for index, data in enumerate(dependencies)
        }

        resp = await self.connection.async_delete_request(
            f"/games/{self.game_id}/mods/{self.id}/dependencies", data=data
        )
        return resp

    def add_team_member(self, email: str, level: Level, *, position: Optional[str] = None):
        """Add a user to the mod team. Will fire a MOD_TEAM_CHANGED event.

        |coro|

        Parameters
        -----------
        email : str
            mod.io email of the user you wish to add
        level : Level
            Level of permissions you grant the user
        position : Optional[str]
            Title of the user position

        """
        data = {"email": email, "level": level.value, "position": position}
        msg = self.connection.post_request(f"/games/{self.game_id}/mods/{self.id}/team", data=data)
        return Message(**msg)

    async def async_add_team_member(self, email: str, level: Level, *, position: Optional[str] = None):
        data = {"email": email, "level": level.value, "position": position}
        msg = await self.connection.async_post_request(
            f"/games/{self.game_id}/mods/{self.id}/team", data=data
        )
        return Message(**msg)
