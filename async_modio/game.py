from .mod import Mod
from .objects import *
from .errors import modioException
from .utils import *

import json

class Game:
    """Represents an instance of a modio.Game. Do not create manually.
    
    Attributes
    -----------
    id : int
        ID of the game. Filter attribute.
    status : int
        Status of the game. Filter attribute.
        0 : Not accepted
        1 : Accepted (default)
        2 : Archived (default)
        3 : Deleted
    submitter : modio.User
        Instance of the modio user having submitted the game. Filter 
        attribute.
    date : int
        UNIX timestamp of the date the game was registered. Filter attribute.
    updated : int
        UNIX timestamp of the date the game was last updated. Filter attribute.
    live : int
        UNIX timestamp of the date the game went live. Filter attribute.
    presentation : int
        Filter attribute.
        0 : Display mods for that game in a grid on mod.io
        1 : Display mods for that game in a table on mod.io
    submission : int
        Filter attribute.
        0 : Mod uploads must occur via a tool created by the game developers
        1 : Mod uploads can occur from anywhere, including the website and API
    curation : int
        Filter attribute.
        0 : No curation: Mods are immediately available to play
        1 : Paid curation: Mods are immediately available to play unless 
        they choose to receive donations. These mods must be accepted to be listed
        2 : Full curation: All mods must be accepted by someone to be listed
    community : int
        Filter attribute.
        0 : All of the options below are disabled
        1 : Discussion board enabled
        2 : Guides and news enabled
        ? : Above options can be added together to create custom settings (e.g 3 : 
        discussion board, guides and news enabled)
    revenue : int
        Filter attribute.
        0 : All of the options below are disabled
        1 : Allow mods to be sold
        2 : Allow mods to receive donations
        4 : Allow mods to be traded
        8 : Allow mods to control supply and scarcity
        ? : Above options can be added together to create custom settings (e.g 3 :
        allow mods to be sold and receive donations)
    api : int
        Filter attribute.
        0 : All of the options below are disabled
        1 : Allow 3rd parties to access this games API endpoints
        2 : Allow mods to be downloaded directly (if disabled all download URLs will 
        contain a frequently changing verification hash to stop unauthorized use)
        ? : Above options can be added together to create custom settings (e.g 3 : 
        allow 3rd parties to access this games API endpoints and allow mods to be
        downloaded directly)
    maturity_options : int
        Filter attribute.
        0 : Don't allow mod developpers to decide whether or not to flag their mod as 
        containing mature content (if game devs wish to handle it)
        1 : Allow mod developpers to decide whether or not to flag their mod as 
        containing mature content
    ugc : str
        Word used to describe user-generated content (mods, items, addons etc).
        Filter attribute.
    icon : modio.Image
        The game icon
    logo : modio.Image
        The game logo
    header : modio.Image
        The game header
    name : str
        Name of the game. Filter attribute.
    name_id : str
        sub_domain name for the game (https://name_id.mod.io). Filter attribute.
    summary : str
        Summary of the game. Filter attribute.
    instructions : str
        Instructions on uploading mods for this game, only applicable
        if :attr:`submissions` equals 0
    instructions_url : str
        Link to a mod.io guide, your modding wiki or a page where modders can learn how to 
        make and submit mods to your games profile. Filter attribute.
    profile : str
        URL to the game's mod.io page.
    tag_options : list[modio.TagOption]
        List of tags from which mods can pick

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.status = attrs.pop("status")
        self.submitter = User(**attrs.pop("submitted_by"))
        self.date = attrs.pop("date_added")
        self.updated = attrs.pop("date_updated")
        self.live = attrs.pop("date_live")
        self.presentation = attrs.pop("presentation_option")
        self.submission = attrs.pop("submission_option")
        self.curation = attrs.pop("curation_option")
        self.community = attrs.pop("community_options")
        self.revenue = attrs.pop("revenue_options")
        self.api = attrs.pop("api_access_options", )
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
        self.maturity_options = attrs.pop("maturity_options")
        self._client = attrs.pop("client")

    def __repr__(self):
        return f'<modio.Game id={self.id} name={self.name}>'

    def _all_tags(self):
        tag_list = []
        for tag in self.tag_options:
            tag_list.extend(tag.tags)

        return tag_list


    async def get_mod(self, id : int):
        """Queries the mod.io API for the given mod ID and if found returns it as a 
        modio.Mod instance. If not found raises NotFound.

        This function is a coroutine

        Parameters
        -----------
        id : int
            The ID of the mod to query the API for

        Raises
        -------
        NotFound
            A mod with the supplied id was not found.

        Returns
        --------
        modio.Mod
            The mod with the given ID
        
        """
        mod_json = await self._client._get_request(f"/games/{self.id}/mods/{id}")
        return Mod(client=self._client, **mod_json)

    async def get_mods(self, filter=None):
        """Gets all the mods available for the game. Takes filtering arguments. Returns a 
        named tuple with parameters results and pagination.

        This function is a coroutine

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.Mod]
            A list of modio.Mod instances
        modio.Pagination
            Pagination data
               
        """
        mod_json = await self._client._get_request(f"/games/{self.id}/mods", filter=filter)
        return Returned([Mod(client=self._client, **mod) for mod in mod_json["data"]], Pagination(**mod_json))

    async def get_mod_events(self, *, filter=None):
        """Gets all the mod events available for this game sorted by latest event first. Takes 
        filtering arguments.

        This function is a coroutine

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.Event]
            A list of modio.Event instances
        modio.Pagination
            Pagination data
               
        """
        event_json = await self._client._get_request(f"/games/{self.id}/mods/events", filter=filter)

        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    async def get_tags(self, *, filter=None):
        """Gets all the game tags available for this game. Takes filtering
        arguments. Updates the tag_option attribute.

        This function is a coroutine

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.TagOption]
            A list of modio.TagOption instances
        modio.Pagination
            Pagination data
               
        """
        tag_json = await self._client._get_request(f"/games/{self.id}/tags", filter=filter)
        self.tag_options = tags = [TagOption(**tag_option) for tag_option in tag_json["data"]]
        return Returned(tags, Pagination(**tag_json))

    async def get_stats(self, *, filter=None):
        """Gets the stat objects for all the mods of this game. Takes 
        filtering arguments.

        This function is a coroutine

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.Stats]
            List of all the mod stats
        modio.Pagination
            Pagination data
        """
        stats_json = await self._client._get_request(f"/games/{self.id}/mods/stats", filter=filter)
        return Returned([Stats(**stats) for stats in stats_json["data"]], Pagination(**stats_json))

    async def get_owner(self):
        """Returns the original submitter of the resource.

        This function is a coroutine

        Returns
        --------
        User
            User that submitted the resource
        """
        user_json = await self._client._post_request(f"/general/ownership", data={"resource_type" : "games", "resource_id" : self.id})
        return User(**user_json)

    async def edit(self, **fields):
        """Used to edit the game details. For editing the icon, logo or header use :func:`add_media`.
        Sucessful editing will update the game instance.

        This function is a coroutine

        Parameters
        -----------
        status : int
            0 : Not accepted
            1 : Accepted
        name : str
            Name of the game, cannot exceed 80 characters
        name_id : str
            Subdomain for the game, cannot exceed 20 characters
        summary : str
            Explaination of game mod support, cannot exceed 250 characters
        instructions : str
            Instructions and link creators should follow to upload mods.
        instructions_url : str
            Link to guide where modders can learn to make and submit mods
        ugc_name : str
            Word used to describe user-generated content (mods, items, addons etc).
        presentation : int
            0 : Display mods for that game in a grid on mod.io
            1 : Display mods for that game in a table on mod.io
        submission : int
            0 : Mod uploads must occur via a tool created by the game developers
            1 : Mod uploads can occur from anywhere, including the website and API
        curation : int
            0 : No curation: Mods are immediately available to play
            1 : Paid curation: Mods are immediately available to play unless 
            they choose to receive donations. These mods must be accepted to be listed
            2 : Full curation: All mods must be accepted by someone to be listed
        community : int
            0 : All of the options below are disabled
            1 : Discussion board enabled
            2 : Guides and news enabled
            ? : Above options can be added together to create custom settings (e.g 3 : 
            discussion board, guides and news enabled)
        revenue : int
            0 : All of the options below are disabled
            1 : Allow mods to be sold
            2 : Allow mods to receive donations
            4 : Allow mods to be traded
            8 : Allow mods to control supply and scarcity
            ? : Above options can be added together to create custom settings (e.g 3 :
            allow mods to be sold and receive donations)
        api : int
            0 : All of the options below are disabled
            1 : Allow 3rd parties to access this games API endpoints
            2 : Allow mods to be downloaded directly (if disabled all download URLs will 
            contain a frequently changing verification hash to stop unauthorized use)
            ? : Above options can be added together to create custom settings (e.g 3 : 
            allow 3rd parties to access this games API endpoints and allow mods to be
            downloaded directly)
        maturity : int
            0 : Don't allow mod developpers to decide whether or not to flag their mod as 
            containing mature content (if game devs wish to handle it)
            1 : Allow mod developpers to decide whether or not to flag their mod as 
            containing mature content"""

        game_json = await self._client._put_request(f'/games/{self.id}', data = fields)
        self.__init__(self._client, **game_json)

    async def add_mod(self, mod):
        """Add a mod to this game.

        This function is a coroutine
        
        Parameters
        -----------
        mod : modio.NewMod
            The mod to be submitted

        Raises
        -------
        modioException
            Not instance of modio.NewMod or submissions from 3rd party disabled
        ValueError
            One of the requirements for a parameter has not been met.

        Returns
        --------
        modio.Mod
            The newly created mod
        """
        if not isinstance(mod, NewMod):
            raise modioException("mod argument must be type modio.NewMod")

        mod_d = mod.__dict__.copy()
        tags = mod_d.pop("tags")
        files = {"logo":mod_d.pop("logo")}
        for tag in tags:
            mod_d[f"tags[{tags.index(tag)}]"] = tag

        try:
            mod_json = await self._client._post_request(f'/games/{self.id}/mods', h_type = 1, data = mod_d, files=files)
        finally:
            mod.logo.close()

        return Mod(client=self._client, **mod_json)

    async def add_media(self, **media):
        """Upload new media to to the game. This function can take between 1 to 3 arguments
        depending on what media you desire to upload/update.

        This function is a coroutine
        
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
        for image in media:
            media[image] = open(media[image], "rb")

        try:
            message = await self._client._post_request(f'/games/{self.id}/media', h_type = 1, files = media)
        finally:
            for image in media.values():
                image.close()
        
        return Message(**message)

    async def add_tags(self, **tag_option):
        """Add tags which mods can apply to their profiles. If the tag name already exists it will
        overwrite it.

        This function is a coroutine

        Parameters
        -----------
        name : str
            Name of the tag group
        type : Optional[str]
            Defaults to dropdown
            dropdown : Mods can select only one tag from this group, dropdown menu shown on site profile.
            checkboxes : Mods can select multiple tags from this group, checkboxes shown on site profile.
        hidden : Optional[bool]
            Whether or not this group of tags should be hidden from users and mod devs. Defaults to False
        tags : list[str]
            Array of tags that mod creators can apply to their mod

        """
        raw_tags = tag_option.get("tags", [])
        tags = {f"tags[{raw_tags.index(tag)}]" : tag for tag in raw_tags}
        tags["name"] = tag_option.get("name")
        tags["type"] = tag_option.get("type", "dropdown")
        tags["hidden"] = json.dumps(tag_option.get("hidden", False))
        print(tags)

        message = await self._client._post_request(f'/games/{self.id}/tags', data=tags)

        self.tag_options.append(TagOption(**tag_option))
        return Message(**message)

    async def delete_tags(self, **tags):
        """Delete one or more tags from a tag option.

        This function is a coroutine
        
        Parameters
        -----------
        name : str
            Name of the group from which you wish to delete from
        tags : Optional[list[str]]
            Optional. Tags to delete from group. If left blank the entire group will be
            deleted

        Returns
        --------
        bool
            Returns True if the tags were sucessfully removed, False if the requests was
            sucessful but the tags was not removed (if the tag wasn't part of the option.)
        """
        raw_tags = tags.get("tags", [])
        data = {f"tags[{raw_tags.index(tag)}]" : tag for tag in raw_tags} if len(raw_tags) > 0 else {"tags[]":""}
        data["name"] = tags.get("name")

        r = await self._client._delete_request(f'/games/{self.id}/tags', data = data)

        option = find(self.tag_options, name=data["name"])
        if len(raw_tags) > 0:
            option.tags = [tag for tag in option.tags if tag not in raw_tags]
        else:
            self.tag_options.remove(option)

        return not isinstance(r, dict)

