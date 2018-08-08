from math import sqrt
import time

from .utils import find
from .objects import *
from .errors import *

class Mod:
    """Represent a modio mod object.

    Attributes
    -----------
    id : int
        ID of the mod
    status : int
        Status of the mod.
        0 : Not Accepted
        1 : Accepted
        2 : Archived (potentially out of date or incompatible)
        3 : Deleted
    visible : int
        Visibility of the mod.
        0 : Hidden
        1 : Public
    game : int
        ID of the game the mod is for.
    submitter : modio.User
        Instance of the modio User that submitted the mod.
    date_added : int
        UNIX timestamp of the date the mod was registered
    date_updated : int
        UNIX timestamp of the date the mod was last updated
    date_live : int
        UNIX timestamp of the date the mod went live
    logo : modio.Image
        The mod logo
    homepage : str
        Link to the homepage of the mod, can be None.
    name : str
        Name of the mod
    name_id : str
        sub_domain mod for the game (https://game_name.mod.io/name_id)
    summary : str
        Summary of the mod
    description :str
        Detailed description of the mod, supports HTML.
    metadata : str
        Metadata stored by developers which may include properties on how information 
        required. Can be None.
    maturity : int
        Maturity option of the mod. 
        0 : None
        1 : Alcohol
        2 : Drugs
        4 : Violence
        8 : Explicit
        ? : Above options can be added together to create custom settings (e.g 3 : 
        alcohol and drugs present)
    profile : str
        URL of the mod's modio profile
    file : modio.ModFile
        Latest release instance
    media : modio.ModMedia
        Contains mod media data (links and images)
    rating : modio.RatingSummary
        Summary of all rating for this mod
    tags : modio.ModTag
        Tags for this mod.

    """
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id")
        self.status = attrs.pop("status")
        self.visible = attrs.pop("visible")
        self.game = attrs.pop("game_id")
        self.submitter = User(**attrs.pop("submitted_by"))
        self.date_added = attrs.pop("date_added")
        self.date_updated = attrs.pop("date_updated")
        self.date_live = attrs.pop("date_live")
        self.logo = Image(**attrs.pop("logo"))
        self.homepage = attrs.pop("homepage_url", None)
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id")
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description")
        self.metadata = attrs.pop("metadata_blob")
        self.profile = attrs.pop("profile_url")
        self.file = ModFile(**attrs.pop("modfile"), game_id=self.game_id, client=client)
        self.media = ModMedia(**attrs.pop("media"))
        self.maturity = attrs.pop("maturity_options")

        self.rating = RatingSummary(**attrs.pop("rating"))
        self.client = client
        self.tags = [ModTag(**tag) for tag in attrs.pop("tags", [])]

    def get_file(self, id : int):
        """Get the Mod File with the following ID
        
        Parameters
        -----------
        id : int
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
        file_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/files/{id}")
        return ModFile(**file_json, game_id=self.game_id, client=self.client)

    def get_files(self, **fields):
        """Get all mod files for this mod. Takes filtering arguments
        
        Returns
        --------
        list[ModFile]
            List of all modfiles for this mod
        """
        files_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/files", **fields)
        return [ModFile(**file, game_id=self.game_id, client=self.client) for file in files_json["data"]]

    def get_events(self, **fields):
        """Get all events for that mod sorted by latest. Takes filtering arguments.

        Returns
        --------
        list[Events]
            List of all the events for this mod

        """
        event_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/events", **fields)
        return [Event(**event) for event in event_json["data"]]

    def get_tags(self, **fields): #in common with game obj
        tag_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/tags", **fields)
        return [ModTag(**tag) for tag in tag_json["data"]]

    def get_meta(self):
        meta_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/metadatakvp")
        return {meta["key"] : meta["value"] for meta in meta_json["data"]}

    def get_dependencies(self, **fields):
        depen_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/dependencies", **fields)
        return {dependecy["mod_id"] : dependecy["date_added"] for dependecy in depen_json["data"]}

    def get_team(self):
        team_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/team")
        return [TeamMember(**member) for member in team_json["data"]]

    def get_comments(self, **fields):
        comment_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/comments", **fields)
        return [Comment(**comment) for comment in comment_json["data"]]

    def edit(self, **fields):
        mod_json = self.client._put_request(f'/games/{self.game_id}/mods/{self.id}', h_type = 0, data = fields)
        return self.__init__(self.client, **mod_json)

    def delete(self):
        r =self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}', h_type = 0)
        return r

    def add_file(self, file):
        if not isinstance(file, NewFile):
            raise modioException("mod argument must be type modio.NewFile")

        file_d = file.__dict__
        files = {"filedata" : file_d.pop("file")}
        file_json = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/files', h_type = 1, data = file_d, files=files)

        return ModFile(**file_json)

    def add_media(self, **fields):
        media_json = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/media', h_type = 1, files = fields)
        return Message(**media_json)

    def delete_media(self):
        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/media', h_type = 0)
        return r

    def subscribe(self):
        mod_json = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/subscribe', h_type = 0)
        return Mod(self.client, **mod_json)

    def unsubscribe(self):
        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/subscribe', h_type = 0)
        return r

    def add_tags(self, *tags):
        fields = {}
        for tag in tags:
            fields[f"tags[{tags.index(tag)}]"] = tag

        message = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/tags', h_type = 0, data = fields)
        for tag in tags:
            self.tags.append(ModTag(name=tag, date_added=time.time()))

        return Message(**message)

    def del_tags(self, tags):
        fields = {}
        for tag in tags:
            fields[f"tags[{tags.index(tag)}]"] = tag

        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/tags', h_type = 0, data = fields)

        for mod_tag in self.tags:
            if mod_tag.name in tags:
                self.tags.remove(mod_tag)
            
        return r

    def add_rating(self, rating):
        def confidence(ups, downs):
            n = ups + downs

            if n == 0:
                return 0

            z = 1.96 #1.44 = 85%, 1.96 = 95%
            phat = float(ups) / n
            return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

        if not rating == 1 or not rating == -1:
            raise modioException("rating is an argument that can only be 1 or -1")

        checked = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/rating',  h_type=0, data={"rating":rating})

        self.rating.total += 1
        if rating == 1:
            self.rating.positive += 1
        else:
            self.rating.negative += 1

        self.rating.percentage = int((self.rating.positive / self.rating.total)*100)
        self.rating.weighted = confidence(self.rating.positive, self.rating.negative)
        #need to recalculate mod message

        return Message(**checked)

    def add_meta(self, **fields):
        metadata = {}
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}:{fields[data]}"
            index += 1

        checked = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/metadatakvp', h_type=0, data=metadata)
            
        return Message(**checked)

    def del_meta(self, **fields):
        metadata = {}
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}:{fields[data]}"
            index += 1

        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/metadatakvp', h_type=0, data=metadata)
        return r

    def add_depen(self, dependencies : list):
        #to add more than 5 depen at a time
        # composite_list = [dependencies[x:x+5] for x in range(0, len(dependencies)-5, 5)]
        # for depend in composite_list:
        #     dependecy = dict()
        #     for data in depend:
        #         dependecy[f"dependencies[{depend.index(data)}]"] = data

        #     r = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/dependencies', data=dependecy, h_type=0)
        #     self.client._error_check(r)

        # return "all good"

        if len(dependencies) > 5:
            raise modioException("You can only submit 5 dependencies at a time")

        dependecy = {}
        for data in dependencies:
            dependecy[f"dependencies[{dependencies.index(data)}]"] = data

        msg = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/dependencies', h_type=0, data=dependecy)

        return Message(**msg)


    def del_depen(self, dependencies : list):
        dependecy = dict()
        for data in dependencies:
            dependecy[f"dependencies[{dependencies.index(data)}]"] = data

        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/dependencies', h_type=0, data=dependecy)
        return r

    def add_team_member(self, **fields):
        msg = self.client._post_request(f'/games/{self.game_id}/mods/{self.id}/team', h_type=0, data=fields)
        return Message(**msg)

    def update_team_member(self, **fields):
        msg = self.client._put_request(f'/games/{self.game_id}/mods/{self.id}/team/{fields.pop("id")}', h_type=0, data=fields)
        return Message(**msg)

    def del_team_member(self, id : int):
        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/team/{id}', h_type=0)
        return r

    def del_comment(self, id):
        r = self.client._delete_request(f'/games/{self.game_id}/mods/{self.id}/comments/{id}', h_type=0)
        return r
