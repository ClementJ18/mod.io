import requests
from .mod import Mod
from .objects import *
from .errors import *

class Game:
    """Represents an instance of a modio.Game. Do not create manually.
    
    Attributes
    -----------
    id : int
        ID of the game
    status : int
        0 : Not accepted
        1 : Accepted (default)
        2 : Archived (default)
        3 : Deleted
    submitter : modio.User
        Instance of the modio user having submitted the game
    date_added : int
        UNIX timestamp of the date the game was registered
    date_updated : int
        UNIX timestamp of the date the game was last updated
    date_live : int
        UNIX timestamp of the date the game went live
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
        containing mature content
    ugc_name : str
        Word used to describe user-generated content (mods, items, addons etc).
    icon : modio.Image
        The game icon
    logo : modio.Image
        The game logo
    header : modio.Image
        The game header
    name : str
        Name of the game
    name_id : str
        sub_domain name for the game (https://name_id.mod.io)
    summary : str
        Summary of the game
    instructions : str
        Instructions on uploading mods for this game, only applicable
        if :attr:`submissions` equals 0
    instructions_url : str
        Link to a mod.io guide, your modding wiki or a page where modders can learn how to 
        make and submit mods to your games profile.
    profile_url : str
        URL to the game's mod.io page.
    tag_options : list[modio.GameTag]
        List of tags from which mods can pick

    """
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id")
        self.status = attrs.pop("status")
        self.submitter = User(**attrs.pop("submitted_by"))
        self.date_added = attrs.pop("date_added")
        self.date_updated = attrs.pop("date_updated")
        self.date_live = attrs.pop("date_live")
        self.presentation = attrs.pop("presentation_option")
        self.submission = attrs.pop("submission_option")
        self.curation = attrs.pop("curation_option")
        self.community = attrs.pop("community_options")
        self.revenue = attrs.pop("revenue_options")
        self.api = attrs.pop("api_access_options", )
        self.ugc_name = attrs.pop("ugc_name")
        self.icon = Image(**attrs.pop("icon", None))
        self.logo = Image(**attrs.pop("logo", None))
        self.header = Image(**attrs.pop("header", None))
        self.homepage = attrs.pop("homepage", None)
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id")
        self.summary = attrs.pop("summary")
        self.instructions = attrs.pop("instructions", None)
        self.instructions_url = attrs.pop("instructions_url", None)
        self.profile_url = attrs.pop("profile_url")
        self.tag_options = [GameTag(**tag) for tag in attrs.pop("tag_options", [])]
        self.maturity = attrs.pop("maturity_options")
        self.client = client

    def __str__(self):
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'

    def get_mod(self, id : int):
        """Queries the mod.io API for the given mod ID and if found returns it as a 
        modio.Mod instance. If not found raises NotFound

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
        :class: `Mod`
            The mod with the given ID
        
        """
        mod_json = self.client._get_request(f"/games/{self.id}/mods/{id}")

        return Mod(self.client, **mod_json)

    def get_mods(self, **fields):
        """Gets all the mods available for mods. Takes filtering arguments.

        Returns
        --------
        list
            A list of modio.Mod instances
               
        """
        mod_json = self.client._get_request(f"/games/{self.id}/mods")

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self.client, **mod))

        return mod_list

    def get_mod_events(self, **fields):
        """Gets all the mod events available for this game sorted by latest event first. Takes 
        filtering arguments.

        Returns
        --------
        list
            A list of modio.Event instances
               
        """
        event_json = self.client._get_request(f"/games/{self.id}/mods/events")

        return [Event(**event) for event in event_json["data"]]

    def get_tags(self, **fields):
        """Gets all the game tags available for this game.

        Returns
        --------
        list
            A list of modio.GameTag instances
               
        """
        tag_json = self.client._get_request(f"/games/{self.id}/tags")

        return [GameTag(**tag_option) for tag_option in tag_json["data"]]

    def edit(self, **fields):
        """Used to edit the game details. For editing the icon, logo or header use :func:`add_media`.
        Sucessful editing will update the game instance.

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

        game_json = self.client._put_request(f'/games/{self.id}', h_type = 0, data = fields)

        self.__init__(self.client, **game_json)

    def add_mod(self, mod):
        """Add a mod to this game.
        
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
        if self.submission == 0:
            raise modioException("Cannot submit new mods through non-official sources (game wise)")

        if not isinstance(mod, NewMod):
            raise modioException("mod argument must be type modio.NewMod")

        mod_d = mod.__dict__
        tags = mod_d.pop("tags")
        files = {"logo":mod_d.pop("logo")}
        for tag in tags:
            mod_d[f"tags[{tags.index(tag)}]"] = tag

        mod_json = self.client._post_request(f'/games/{self.id}/mods', h_type = 1, data = mod_d, files=files)
        
        return Mod(self.client, **mod_json)

    def add_media(self, **fields):
        """Upload new media to to the game. This function can take between 1 to 3 arguments
        depending on what media you desire to upload/update
        
        Parameters
        -----------
        logo : str
            Path to the file that you desire to be the game's logo. Dimensions must be at least 
            640x360 and we recommended you supply a high resolution image with a 16 / 9 ratio. mod.io 
            will use this logo to create three thumbnails with the dimensions of 320x180, 640x360 and 
            1280x720.
        icon : str
            Path to the file that you desire to be the game's icon. Must be gif, jpg or png format 
            and cannot exceed 1MB in filesize. Dimensions must be at least 64x64 and a transparent 
            png that works on a colorful background is recommended. mod.io will use this icon to 
            create three thumbnails with the dimensions of 64x64, 128x128 and 256x256.
        header : str
            Path to the file that you desire to be the game's header. Must be gif, jpg or png format 
            and cannot exceed 256KB in filesize. Dimensions of 400x100 and a light transparent png that 
            works on a dark background is recommended.

        Returns
        --------
        Message
            A message containing the result of the query if successful.
        """
        for image in field:
            field[image] = open(field[image])

        message = self.client._post_request(f'/games/{self.id}/media', h_type = 1, files = fields)
        self.__int__(self.client, self.client._get_request(f"/games/{self.id}", h_type = 0))
        
        return Message(**message)

    def add_tags(self, **fields):
        """Add tags which mods can apply to their profiles. If the tag name already exists it will
        overwrite it.

        Parameters
        -----------
        name : str
            Name of the tag group
        type : str
            dropdown : Mods can select only one tag from this group, dropdown menu shown on site profile.
            checkboxes : Mods can select multiple tags from this group, checkboxes shown on site profile.
        hidden : bool
            Whether or not this group of tagas should be hidden from users and mod devs.
        tags : list[str]
            Array of tags that mod creators can apply to their mod

        """
        if "tags" in fields:
            tags = fields.pop("tags")
            for tag in tags:
                fields[f"tags[{tags.index(tag)}]"] = tag

        message = self.client._post_request(f'/games/{self.id}/tags', h_type = 0, data = {"input_json" : fields})

        self.tag_options.append(GameTag(**fields))
        return Message(**message)

    def del_tags(self, **fields):
        """Delete one or more tags from a tag option
        
        Parameters
        -----------
        name : str
            Name of the group from which you wish to delete from
        tags : list[str]
            Optional. Tags to delete from group. If left blank the entire group will be
            deleted
        """
        tags = fields.pop("tags", [])
        for tag in tags:
            fields[f"tags[{tags.index(tag)}]"] = tag

        r = self.client._delete_request(f'/games/{self.id}/tags', h_type = 0, data = fields)
        if len(tags) > 0:
            self.tags[fields["name"]] -= tags
        else:
            del self.tags[fields["name"]]

        return r

