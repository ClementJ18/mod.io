from math import sqrt
import time

from .objects import *
from .errors import modioException

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
    date : int
        UNIX timestamp of the date the mod was registered
    updated : int
        UNIX timestamp of the date the mod was last updated
    live : int
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
    rating : modio.Stats
        Summary of all rating for this mod
    tags : dict
        Tags for this mod.
    kvp : dict
        Contains key-value metadata.

    """
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id")
        self.status = attrs.pop("status")
        self.visible = attrs.pop("visible")
        self.game = attrs.pop("game_id")
        self.submitter = User(**attrs.pop("submitted_by"))
        self.date = attrs.pop("date_added")
        self.updated = attrs.pop("date_updated")
        self.live = attrs.pop("date_live")
        self.logo = Image(**attrs.pop("logo"))
        self.homepage = attrs.pop("homepage_url", None)
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id")
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description")
        self.metadata = attrs.pop("metadata_blob")
        self.kvp = {data["metakey"] : data["metavalue"] for data in attrs.pop("metadata_kvp")}
        self.profile = attrs.pop("profile_url")
        self._file = attrs.pop("modfile", None)
        self.media = ModMedia(**attrs.pop("media"))
        self.maturity = attrs.pop("maturity_option")

        self.rating = Stats(**attrs.pop("rating"))
        self.client = client
        self.tags = {tag["name"] : tag["date_added"] for tag in attrs.pop("tags", [])}

    @property
    def file(self):
        return ModFile(**self._file, game_id=self.game, client=client) if self._file else None 

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

    def get_files(self, *, filter=None):
        """Get all mod files for this mod. Takes filtering arguments

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results
        
        Returns
        --------
        list[ModFile]
            List of all modfiles for this mod
        """
        files_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/files", filter=filter)
        return [ModFile(**file, game_id=self.game, client=self.client) for file in files_json["data"]]

    def get_events(self, *, filter=None):
        """Get all events for that mod sorted by latest. Takes filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[Events]
            List of all the events for this mod

        """
        event_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/events", filter=filter)
        return [Event(**event) for event in event_json["data"]]

    def get_tags(self, *, filter=None): 
        """Gets all the tags for this mod. Takes filtering arguments. Updates the instance's
        tag attribute.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        dict{name : date_added}
            dict of tags with the names as keys and date_added as values

        """
        tag_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/tags", filter=filter)
        new_tags = {tag["name"] : tag["date_added"] for tag in tag_json["data"]}
        self.tags = new_tags
        return new_tags

    def get_meta(self):
        """Returns a dict of metakey-metavalue pairs. This will also updated the mod's kvp attribute.

        Returns
        --------
        dict{metakey : metavalue}
            dict of metadata
        """
        meta_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/metadatakvp")
        new_meta = {meta["key"] : meta["value"] for meta in meta_json["data"]}
        self.kvp = new_meta
        return new_meta

    def get_dependencies(self, *, filter=None):
        """Returns a dict of dependency_id-date_added pairs. Takes filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        dict{id : date}
            dict of dependencies

        """
        depen_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/dependencies", filter=filter)
        return {dependecy["mod_id"] : dependecy["date_added"] for dependecy in depen_json["data"]}

    def get_team(self, *, filter=filter):
        """Returns a list of TeamMember object representing the Team in charge of the mod. Takes
        filtering arguments

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[TeamMember]
            List of team members

        """
        team_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/team", filter=filter)
        return [TeamMember(**member, client=self.client, mod=self) for member in team_json["data"]]

    def get_comments(self, *, filter=None):
        """Returns a list of all the comments for this mod. Takes filtering arguments

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[Comment]
            List of comments.
        """
        comment_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/comments", filter=filter)
        return [Comment(**comment, client=self.client, mod=self) for comment in comment_json["data"]]

    def get_stats(self):
        """Returns a Stats object, representing a series of stats for the mod

        Returns
        -------
        Stats
            The stats summary object for the mod.
        """
        stats_json = self.client._get_request(f"/games/{self.game}/mods/{self.id}/stats")
        return Stats(**stats_json)

    def edit(self, **fields):
        """Used to edit the mod details. Sucessful editing will update the mod instance.

        Parameters
        -----------
        status : int
            For game admins only.
            0 : Not accepted
            1 : Accepted
            2 : Archived
        visible : int
            0 : Hidden
            1 : Public
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
        maturity : int
            Maturity option of the mod. 
            0 : None
            1 : Alcohol
            2 : Drugs
            4 : Violence
            8 : Explicit
            ? : Above options can be added together to create custom settings (e.g 3 : 
            alcohol and drugs present)
        metadata : str
                Metadata stored by the mod developer which may include properties as to how 
                the item works, or other information you need to display.
        """
        mod_json = self.client._put_request(f'/games/{self.game}/mods/{self.id}', data = fields)
        return self.__init__(self.client, **mod_json)

    def delete(self):
        """Delete a mod and set its status to deleted."""
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}')
        self.status = 3
        return r

    def add_file(self, file : NewModFile):
        """Adds a new file to the mod, to do so first construct an instance of NewModFile
        and then pass it to the function.
        
        Parameters
        -----------
        file : NewModFile
            The mod file to upload

        Raises
        -------
        modioException
            file argument must be type modio.NewModFile

        Returns
        --------
        ModFile
            The modfile after being processed by the mod.io API

        """
        if not isinstance(file, NewModFile):
            raise modioException("file argument must be type modio.NewModFile")

        file_d = file.__dict__
        files = {"filedata" : file_d.pop("file")}
        file_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/files', h_type = 1, data = file_d, files=files)

        return ModFile(**file_json)

    def add_media(self, **fields):
        """Upload new media to the mod.

        Parameters
        -----------
        logo : str
            Path to the logo file. If on windows, must be \\ escaped. Image file which will represent 
            your mods logo. Must be gif, jpg or png format and cannot exceed 8MB in filesize. Dimensions 
            must be at least 640x360 and we recommended you supply a high resolution image with a 16 / 9 
            ratio. mod.io will use this logo to create three thumbnails with the dimensions of 320x180, 
            640x360 and 1280x720.
        images : Union[str, list]
            Can be either the path to a .zip file containing all the images or a list of paths to multiple
            image files. If on windows, must be \\ escaped. Only valid gif, jpg and png images in the zip file 
            will be processed. Alternatively you can POST one or more images to this endpoint and they will be 
            detected and added to the mods gallery.
        youtube : list[str]
            List of youtube links to be added to the gallery
        sketchfab : list[str]
            List of sketchfab links to the be added to the gallery.

        Returns
        -------
        Message
            A message confirming the submission of the media
        """
        logo = fields.pop("logo", None)
        if logo:
            fields["logo"] = open(logo)

        images = fields.pop("images", None)
        if isinstance(images, str):
            images = {"images" : ("image.zip", open(images))}
        elif isinstance(images, list):
            images = {f"images[{images.index(image)}]" : open(image) for image in images}
            
        yt = fields.pop("youtube", [])
        yt = {f"youtube[{yt.index(link)}]" : link for link in yt}

        sketch = fields.pop("sketchfab", [])
        sketch = {f"sketchfab[{yt.index(link)}]" : link for link in sketch}

        fields = {**fields, **yt, **sketch, **images}

        try:
            media_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/media', h_type = 1, files = fields)
        finally:
            fields["logo"].close()
            for image in images.values():
                image.close()


        return Message(**media_json)

    def delete_media(self, **fields):
        """Delete media from the mod page. 

        Parameters
        -----------
        images : list[str]
            Optional. List of image filenames that you want to delete
        youtube : list[str]
            Optional. List of youtube links that you want to delete
        sketchfab : list[str]
            Optional. List sketchfab links that you want to delete
        """
        images = fields.pop("images", [])
        images = {f"images[{images.index(image)}]" : image for image in images}

        yt = fields.pop("youtube", [])
        yt = {f"youtube[{yt.index(link)}]" : link for link in yt}

        sketch = fields.pop("sketchfab", [])
        sketch = {f"sketchfab[{sketch.index(link)}]" : link for link in sketch}

        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/media')
        return r

    def subscribe(self):
        """Subscribe to the mod. Returns None if user is already subsribed. 

        Returns
        --------
        Mod
            The mod that was just subscribed to, if the user was already subscribed it will return None
        """
        try:
            mod_json = self.client._post_request(f'/games/{self.game}/mods/{self.id}/subscribe')
            return Mod(self.client, **mod_json)
        except BadRequest:
            pass

    def unsubscribe(self):
        """Unsubscribe from a mod. Returns None if the user is not subscribed."""

        try:
            r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/subscribe')
            return r
        except BadRequest:
            pass

    def add_tags(self, tags : list):
        """Add tags to a mod, tags are case insensitive and duplicates will be removed. Tags
        which are not in the game's tag_options will not be added.

        Parameters
        -----------
        tags : list[str]
            list of tags to be added. 

        """
        self.get_tags()
        tags = set([tag.lower() for tag in tags if tag.lower() not in self.tags.keys()])
        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags}

        message = self.client._post_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)
        
        for tag in tags:
            self.tags[tag] = time.time()

        return Message(**message)

    def del_tags(self, tags : list = None):
        """Delete tags from the mod, tags are case insensitive and duplicates will be removed. Providing
        no arguments will remove every tag from the mod.

        Parameters
        tags : list
            List of tags to remove, if no list is provided, will remove every tag from the mod.

        """
        self.get_tags()

        if tags:
            tags = set([tag.lower() for tag in tags if tag.lower() in self.tags.keys()])
        else:
            tags = self.tags.keys()

        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags}

        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)

        for tag in tags:
            del self.tags[tag]
            
        return r

    def add_rating(self, rating : RatingType):
        """Adds a good or bad rating to the mod, the author of the rating will be the authenticated user.
        If the mod has already been rated by the user it will return None.

        Parameters
        -----------
        rating : modio.RatingType
            The rating that will be assigned to the mod.

        Raises
        -------
        modioException
            rating argument must be RatingType

        """
        def confidence(ups, downs):
            n = ups + downs

            if n == 0:
                return 0

            z = 1.96 #1.44 = 85%, 1.96 = 95%
            phat = float(ups) / n
            return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

        if not isinstance(rating, RatingType):
            raise modioException("rating is an argument that can only be RatingType.good or RatingType.bad")

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
        """Add metadate key-value pairs to the mod. To submit new meta data, mass meta data keys
        as keyword arguments and meta data value as a list of values. E.g pistol_dmg = [800, 400].
        Keys support alphanumeric, '-' and '_'. Total lengh of key and values cannot exceed 255
        characters.

        Returns
        --------
        Message
            message on the status of the successful added meta data

        """
        metadata = {}
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}:{':'.join(fields[data])}"
            index += 1

        checked = self.client._post_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata)
            
        return Message(**checked)

    def del_meta(self, **fields):
        """Deletes metadata from a mod. To do so pass the meta-key as a keyword argument and the
        meta-values you wish to delete as a list. You can pass an empty list in which case all
        meta-values for the meta-key will be deleted.

        """
        metadata = {}
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}{':' if len(fields[data]) > 0 else ''}{':'.join(fields[data])}"
            index += 1

        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata)
        return r

    def add_dependencies(self, dependencies : list):
        """Add mod dependencies required by the corresponding mod. A dependency is a mod 
        that should be installed for this mod to run. Since the API officially only supports
        adding 5 dependencies at a time, passing more than 5 to this function will cause
        additional requests for every 5 additional dependency.

        Parameters
        ----------
        dependencies : list[int]
            List fo dependencies to submit.

        """
        while len(depedencies) > 0:
            dependecy = {f"dependencies[{dependencies.index(data)}]" : data for data in dependencies[:5]}
            dependencies = dependencies[5:]

            r = self.client._post_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependecy)

        return r

    def delete_dependencies(self, dependencies : list):
        """Delete mod dependecies required by this mod.

        Parameters
        -----------
        dependencies : list[int]
            List of dependencies to remove
        """
        dependecy = {f"dependencies[{dependencies.index(data)}]" : data for data in dependencies}
        r = self.client._delete_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependecy)
        return r

    def add_team_member(self, *, email, level, position=None):
        """Add a user to the mod team. Will fire a MOD_TEAM_CHANGED event.

        Parameters
        -----------
        email : str
            mod.io email of the user you wish to add
        level : int
            Level of permissions you grant the user
            1 : Moderator
            4 : Creator
            8 : Administrator
        position : Optional[str]
            Title of the user position

        """
        data = {"email" : email, "level" : level, "position" : position}
        msg = self.client._post_request(f'/games/{self.game}/mods/{self.id}/team', data=data)
        return Message(**msg)

