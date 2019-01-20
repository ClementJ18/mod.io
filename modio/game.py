from .mod import Mod
from .objects import *
from .errors import modioException
from .utils import _convert_date, _clean_and_convert, find
from .enums import Submission

import json

class Game:
    """Represents an instance of a Game. Do not create manually.
    
    Attributes
    -----------
    id : int
        ID of the game. Filter attribute.
    status : Status
        Status of the game. Filter attribute.
    submitter : User
        Instance of the modio user having submitted the game. Filter 
        attribute.
    date : datetime.datetime
        UNIX timestamp of the date the game was registered. Filter attribute.
    updated : datetime.datetime
        UNIX timestamp of the date the game was last updated. Filter attribute.
    live : datetime.datetime
        UNIX timestamp of the date the game went live. Filter attribute.
    presentation : Presentation
        Filter attribute.
    submission : Submission
        Filter attribute.
    curation : Curation
        Filter attribute.
    community : Community
        Filter attribute.
    revenue : Revenue
        Filter attribute.
    api : APIAccess
        Filter attribute.
    maturity_options : MaturityOptions
        Filter attribute.
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

    """
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
        self.api = APIAccess(attrs.pop("api_access_options", ))
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
        self.submitter = User(client=self._client, **attrs.pop("submitted_by"))
        
    def __repr__(self):
        return f'<Game id={self.id} name={self.name}>'

    def _all_tags(self):
        tag_list = []
        for tag in self.tag_options:
            tag_list.extend(tag.tags)

        return tag_list


    def get_mod(self, id : int):
        """Queries the mod.io API for the given mod ID and if found returns it as a 
        Mod instance. If not found raises NotFound

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
        mod_json = self._client._get_request(f"/games/{self.id}/mods/{id}")
        return Mod(client=self._client, **mod_json)

    def get_mods(self, *, filter=None):
        """Gets all the mods available for the game. Takes filtering arguments. Returns a 
        named tuple with parameters results and pagination.

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        Returned
            The results and pagination tuple from this request
               
        """
        mod_json = self._client._get_request(f"/games/{self.id}/mods", filter=filter)
        return Returned([Mod(client=self._client, **mod) for mod in mod_json["data"]], Pagination(**mod_json))

    def get_mod_events(self, *, filter=None):
        """Gets all the mod events available for this game sorted by latest event first. Takes 
        filtering arguments.

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        Returned
            The results and pagination tuple from this request
               
        """
        event_json = self._client._get_request(f"/games/{self.id}/mods/events", filter=filter)

        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    def get_tag_options(self, *, filter=None):
        """Gets all the game tags available for this game. Takes filtering
        arguments. Updates the tag_option attribute

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        Returned
            The results and pagination tuple from this request
               
        """
        tag_json = self._client._get_request(f"/games/{self.id}/tags", filter=filter)
        self.tag_options = tags = [TagOption(**tag_option) for tag_option in tag_json["data"]]
        return Returned(tags, Pagination(**tag_json))

    def get_stats(self, *, filter=None):
        """Gets the stat objects for all the mods of this game. Takes 
        filtering arguments

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        Returned
            The results and pagination tuple from this request
        """
        stats_json = self._client._get_request(f"/games/{self.id}/mods/stats", filter=filter)
        return Returned([Stats(**stats) for stats in stats_json["data"]], Pagination(**stats_json))

    def get_owner(self):
        """Returns the original submitter of the resource

        Returns
        --------
        User
            User that submitted the resource
        """
        user_json = self._client._post_request(f"/general/ownership", data={"resource_type" : "games", "resource_id" : self.id})
        return User(client=self._client, **user_json)

    def edit(self, **fields):
        """Used to edit the game details. For editing the icon, logo or header use :func:`add_media`.
        Sucessful editing will update the game instance.

        Parameters
        -----------
        status : Status
            Game status
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
        presentation : Presentation
            How to display the game's mods on modio
        submission : Submissions
            Pick how mods can be uploaded
        curation : Curation
            Pick moderation levels of mods
        community : Community
            Change the community options of mods
        revenue : Revenue
            Change the revenue settings for mods
        api : APIAccess
            Change the api access of the mods
        maturity_options : MaturityOptions
            Chose whether or not to allow mature content"""

        fields = _clean_and_convert(fields)
        game_json = self._client._put_request(f'/games/{self.id}', data = fields)
        self.__init__(client=self._client, **game_json)

    def add_mod(self, mod):
        """Add a mod to this game.
        
        Parameters
        -----------
        mod : NewMod
            The mod to be submitted

        Raises
        -------
        modioException
            Not instance of NewMod or submissions from 3rd party disabled
        ValueError
            One of the requirements for a parameter has not been met.

        Returns
        --------
        Mod
            The newly created mod
        """
        if not isinstance(mod, NewMod):
            raise modioException("mod argument must be type NewMod")

        mod_d = mod.__dict__.copy()
        tags = list(mod_d.pop("tags"))
        for tag in tags:
            mod_d[f"tags[{tags.index(tag)}]"] = tag

        with open(mod_d.pop("logo"), "rb") as f:
            mod_json = self._client._post_request(f'/games/{self.id}/mods', h_type = 1, data = mod_d, files={"logo": f})

        return Mod(client=self._client, **mod_json)

    def add_media(self, *, logo = None, icon = None, header = None):
        """Upload new media to to the game. This function can take between 1 to 3 arguments
        depending on what media you desire to upload/update
        
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
            message = self._client._post_request(f'/games/{self.id}/media', h_type = 1, files = media)
        finally:
            for image in media.values():
                image.close()
        
        return Message(**message)

    def add_tag_options(self, name, *, tags = [], hidden = False, type = 'dropdown'):
        """Add tags which mods can apply to their profiles. If the tag names already exists,
        settings such as hidden or type will be overwritten to the values provided and all the 
        tags will be added to the group.

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
        tags : Optional[List[str]]
            Array of tags that mod creators can apply to their mod
        """
        tags = {f"tags[{tags.index(tag)}]" : tag for tag in tags}
        tags = {"name": name, "type": type, "hidden": json.dumps(hidden), **tags}
        message = self._client._post_request(f'/games/{self.id}/tags', data=tags)

        tag_option = find(self.tag_options, name=name)
        if not tag_option:
            self.tag_options.append(TagOption(**tags))
        else:
            tag_option.type = type
            tag_option.hidden = hidden
            tag_option.tags.extend(tags)

        return Message(**message)

    def delete_tag_options(self, name, *, tags = []):
        """Delete one or more tags from a tag option
        
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
        data = {f"tags[{tags.index(tag)}]" : tag for tag in tags} if tags else {"tags[]":""}
        data["name"] = name

        r = self._client._delete_request(f'/games/{self.id}/tags', data = data)

        option = find(self.tag_options, name=name)
        if tags:
            option.tags = [tag for tag in option.tags if tag not in tags]
        else:
            self.tag_options.remove(option)

        return not isinstance(r, dict)

    def report(self, name, summary, type = Report(0)):
        """Report a this game, make sure to read mod.io's ToU to understand what is
        and isnt allowed.

        Parameters
        -----------
        name : str
            Name of the report
        summary : str
            Detailed description of your report. Make sure you include all relevant information and 
            links to help moderators investigate and respond appropiately.
        type : Report
            Report type

        Returns
        --------
        Message
            The returned message on the success of the query.

        """
        fields = {
            "id" : self.id,
            "resource" :  "games",
            "name" : name,
            "type" : type.value,
            "summary" : summary
        }

        msg = self._client._post_request('/report', data = fields)
        return Message(**msg)

