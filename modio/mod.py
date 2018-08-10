from math import sqrt
import time

from .objects import *
from .errors import modioException
from .utils import *

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
        Latest release instance. Can be None.
    media : modio.ModMedia
        Contains mod media data (links and images)
    rating : modio.RatingSummary
        Summary of all rating for this mod
    tags : modio.Tag
        Tags for this mod.

    """
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id")
        self.status = attrs.pop("status")
        self.visible = attrs.pop("visible")
        self.game = attrs.pop("game_id")
        self.submitter = User(**attrs.pop("submitted_by"))
        self.date = attrs.pop("date_added")
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
        self._file = attrs.pop("modfile", None)
        self.media = ModMedia(**attrs.pop("media"))
        self.maturity = attrs.pop("maturity_option")

        self.rating = Stats(**attrs.pop("rating"))
        self.client = client
        self.tags = [Tag(**tag) for tag in attrs.pop("tags", [])]

    @property
    def file(self):
        return ModFile(**self._file, game_id=self.game, client=client) if self._file else None

    def _update_tags(self):
        self.tags = self.get_tags()

    def _tags_to_str(self):
        return [tag.name for tag in self.tags]    

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
        file_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/files/{id}")
        return ModFile(**file_json, game_id=self.game, client=self.client)

    def get_files(self, **fields):
        """Get all mod files for this mod. Takes filtering arguments
        
        Returns
        --------
        list[ModFile]
            List of all modfiles for this mod
        """
        files_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/files", **fields)
        return [ModFile(**file, game_id=self.game, client=self.client) for file in files_json["data"]]

    def get_events(self, **fields):
        """Get all events for that mod sorted by latest. Takes filtering arguments.

        Returns
        --------
        list[Events]
            List of all the events for this mod

        """
        event_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/events", **fields)
        return [Event(**event) for event in event_json["data"]]

    def get_tags(self, **fields): 
        """Gets all the tags for this mod. Takes filtering arguments.

        Returns
        --------
        list[Tag]
            list of all the tags

        """
        tag_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/tags", **fields)
        return [Tag(**tag) for tag in tag_json["data"]]

    def get_meta(self):
        meta_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/metadatakvp")
        return {meta["key"] : meta["value"] for meta in meta_json["data"]}

    def get_dependencies(self, **fields):
        depen_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/dependencies", **fields)
        return {dependecy["mod_id"] : dependecy["date_added"] for dependecy in depen_json["data"]}

    def get_team(self):
        team_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/team")
        return [TeamMember(**member) for member in team_json["data"]]

    def get_comments(self, **fields):
        comment_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/comments", **fields)
        return [Comment(**comment) for comment in comment_json["data"]]

    def get_stats(self):
        stats_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/stats")
        return Stats(**stats_json)

    def edit(self, **fields):
        mod_json = self.client._put_request(f'/games/{self.game}/mods/{self.id}', data = fields)
        return self.__init__(self.client, **mod_json)

    def delete(self):
        r =self.client._delete_request(f'/games/{self.game}/mods/{self.id}')
        return r

    def add_file(self, file : NewModFile):
        if not isinstance(file, NewModFile):
            raise modioException("mod argument must be type modio.NewModFile")

        file_d = file.__dict__
        files = {"filedata" : file_d.pop("file")}
        file_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/files', h_type = 1, data = file_d, files=files)

        return ModFile(**file_json)

    def add_media(self, **fields):
        media_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/media', h_type = 1, files = fields)
        return Message(**media_json)

    def delete_media(self):
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/media')
        return r

    def subscribe(self):
        try:
            mod_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/subscribe')
        except BadRequest:
            pass

        return Mod(self.client, **mod_json)

    def unsubscribe(self):
        try:
            r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/subscribe')
        except BadRequest:
            pass

        return r

    def add_tags(self, tags : list):
        self._update_tags()
        tags = [tag.lower() for tag in (tags - self._tags_to_str())]
        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags}

        message = self.client._post_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)
        
        for tag in tags:
            self.tags.append(Tag(name=tag, date_added=time.time()))

        return Message(**message)

    def del_tags(self, tags : list):
        self._update_tags()
        tags = [tag.lower() for tag in tags if tag.lower() in self._tags_to_str()]
        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags}

        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)

        for tag in self.tags:
            if tag.name in tags:
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

        try:
            checked = self.client._post_request(f'/games/{self.game}/mods/{self.id}/rating', data={"rating":rating})
        except BadRequest:
            return

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

        checked = self.client._post_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata)
            
        return Message(**checked)

    def del_meta(self, **fields):
        metadata = {}
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}:{fields[data]}"
            index += 1

        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata)
        return r

    def add_dependencies(self, dependencies : list):
        while len(depedencies) > 0:
            dependecy = {f"dependencies[{dependencies.index(data)}]" : data for data in dependencies}
            dependencies -= dependencies[:5]

            r = self.client._post_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependecy)

        return r

        # if len(dependencies) > 5:
        #     raise modioException("You can only submit 5 dependencies at a time")

        # dependecy = {}
        # for data in dependencies:
        #     dependecy[f"dependencies[{dependencies.index(data)}]"] = data

        # msg = self.client._post_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependecy)

        # return Message(**msg)


    def del_dependencies(self, dependencies : list):
        dependecy = {f"dependencies[{dependencies.index(data)}]" : data for data in dependencies}
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependecy)
        return r

    def add_team_member(self, **fields):
        msg = self.client._post_request(f'/games/{self.game}/mods/{self.id}/team', data=fields)
        return Message(**msg)

    def update_team_member(self, **fields):
        msg = self.client._put_request(f'/games/{self.game}/mods/{self.id}/team/{fields.pop("id")}', data=fields)
        return Message(**msg)

    def del_team_member(self, id : int):
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/team/{id}')
        return r

    def del_comment(self, id : int):
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/comments/{id}')
        return r
