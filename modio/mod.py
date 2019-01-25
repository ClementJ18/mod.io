import time

from .objects import *
from .errors import modioException, BadRequest
from .utils import _convert_date, _clean_and_convert

class Mod:
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
    game : int
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
        Latest release instance. Can be None. Filter attribute.
    media : ModMedia
        Contains mod media data (links and images)
    rating : Stats
        Summary of all rating for this mod
    tags : dict
        Tags for this mod. Filter attribute.
    kvp : dict
        Contains key-value metadata. Filter attribute.
    plaintext : str
        description field converted into plaintext.

    """
    def __init__(self, **attrs):
        self.id = attrs.pop("id")
        self.status = Status(attrs.pop("status"))
        self.visible = Visibility(attrs.pop("visible"))
        self.game = attrs.pop("game_id")
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
        self.stats = Stats(**attrs.pop("stats"))
        self.tags = {tag["name"] : tag["date_added"] for tag in attrs.pop("tags", [])}
        self._client = attrs.pop("client")
        self._file = attrs.pop("modfile", None)
        self._kvp_raw = attrs.pop("metadata_kvp")
        self.file =  ModFile(**self._file, game_id=self.game, client=self._client) if self._file else None 
        self.submitter = User(client=self._client, **attrs.pop("submitted_by"))
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
        return f"<Mod id={self.id} name={self.name} game={self.game}>"   

    def get_file(self, id : int):
        """Get the Mod File with the following ID.

        |coro|
        
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
        file_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/files/{id}")
        return ModFile(**file_json, game_id=self.game, client=self._client)

    def get_files(self, *, filter=None):
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
        files_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/files", filter=filter)
        return Returned([ModFile(**file, game_id=self.game, client=self._client) for file in files_json["data"]], Pagination(**files_json))

    def get_events(self, *, filter=None):
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
        event_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/events", filter=filter)
        return Returned([Event(**event) for event in event_json["data"]], Pagination(**event_json))

    def get_tags(self, *, filter=None): 
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
        tag_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/tags", filter=filter)
        self.tags = new_tags = {tag["name"] : _convert_date(tag["date_added"]) for tag in tag_json["data"]}
        return Returned(new_tags, Pagination(**tag_json))

    def get_metadata(self):
        """Returns a dict of metakey-metavalue pairs. This will also update the mod's kvp attribute.

        |coro|

        Returns
        --------
        Returned[List[MetaData], Pagination]
            The results and pagination tuple from this request
        """
        meta_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/metadatakvp")
        self._kvp_raw = meta_json["data"]
        return Returned(self.kvp, Pagination(**meta_json))

    def get_dependencies(self, *, filter=None):
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
        depen_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/dependencies", filter=filter)
        return Returned({dependecy["mod_id"] : _convert_date(dependecy["date_added"]) for dependecy in depen_json["data"]}, Pagination(**depen_json))

    def get_team(self, *, filter=None):
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
        team_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/team", filter=filter)
        return Returned([TeamMember(**member, client=self._client, mod=self) for member in team_json["data"]], Pagination(**team_json))

    def get_comments(self, *, filter=None):
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
        comment_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/comments", filter=filter)
        return Returned([Comment(**comment, client=self._client, mod=self) for comment in comment_json["data"]], Pagination(**comment_json))

        # comments = []
        # for comment_d in comment_json["data"]:
        #     comment = Comment(**comment_d, client=self._client, mod=self)
        #     try:
        #         if comment.level == 1:
        #             comments.append(comment)
        #         elif comment.level == 2:
        #             comments[-1].children.append(comment)
        #         elif comment.level == 3:
        #             comments[-1].children[-1].children.append(comment)
        #     except IndexError:
        #         comments.append(comment)


    def get_stats(self):
        """Returns a Stats object, representing a series of stats for the mod.

        |coro|

        Returns
        -------
        Stats
            The stats summary object for the mod.
        """
        stats_json = self._client._get_request(f"/games/{self.game}/mods/{self.id}/stats")
        self.stats = stats = Stats(**stats_json)
        return stats

    def get_owner(self):
        """Returns the original submitter of the resource.

        |coro|

        Returns
        --------
        User
            User that submitted the resource
        """
        user_json = self._client._post_request(f"/general/ownership", data={"resource_type" : "mods", "resource_id" : self.id})
        return User(client=self._client, **user_json)

    def edit(self, **fields):
        """Used to edit the mod details. Sucessful editing will update the mod instance.

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
        """
        fields = _clean_and_convert(fields)
        mod_json = self._client._put_request(f'/games/{self.game}/mods/{self.id}', data = fields)
        return self.__init__(client=self._client, **mod_json)

    def delete(self):
        """Delete a mod and set its status to deleted.

        |coro|
        """
        r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}')
        self.status = 3
        return r

    def add_file(self, file : NewModFile):
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
        if not isinstance(file, NewModFile):
            raise modioException("file argument must be type NewModFile")

        file_d = file.__dict__.copy()
        file_file = file_d.pop("file")

        with open(file_file, "rb") as f:
            file_json = self._client._post_request(f'/games/{self.game}/mods/{self.id}/files', h_type = 1, data = file_d, files={"filedata" : f})

        return ModFile(**file_json, game_id=self.game, client=self._client)

    def add_media(self, *, logo = None, images = [], youtube = [], sketchfab = []):
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
        media = {}

        if logo:
            media["logo"] = open(logo, "rb")

        if isinstance(images, str):
            images_d = {"images" : ("image.zip", open(images, "rb"))}
        elif isinstance(images, list):
            images_d = {f"image{images.index(image)}" : open(image, "rb") for image in images}
            
        yt = {f"youtube[{youtube.index(link)}]" : link for link in youtube}
        sketch = {f"sketchfab[{sketchfab.index(link)}]" : link for link in sketchfab}

        media = {**media, **images_d}
        links = {**yt, **sketch}

        try:
            media_json = self._client._post_request(f'/games/{self.game}/mods/{self.id}/media', h_type = 1, files = media, data = links)
        finally:
            if logo:
                media["logo"].close()
            if isinstance(images, str):
                images_d["images"][1].close()
            elif isinstance(images, list):
                for image in images_d.values():
                    image.close()

        return Message(**media_json)

    def delete_media(self, *, images = [], youtube = [], sketchfab = []):
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
        images = {f"images[{images.index(image)}]" : image for image in images}
        yt = {f"youtube[{youtube.index(link)}]" : link for link in youtube}
        sketch = {f"sketchfab[{sketchfab.index(link)}]" : link for link in sketchfab}
        fields = {**images, **yt, **sketch}

        r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}/media', data = fields)
        return r

    def subscribe(self):
        """Subscribe to the mod. Returns None if user is already subscribed. 

        |coro|

        Returns
        --------
        Mod
            The mod that was just subscribed to, if the user was already subscribed it will return None
        """
        try:
            mod_json = self._client._post_request(f'/games/{self.game}/mods/{self.id}/subscribe')
            return Mod(client=self._client, **mod_json)
        except BadRequest:
            pass

    def unsubscribe(self):
        """Unsubscribe from a mod. Returns None if the user is not subscribed.

        |coro|"""

        try:
            r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}/subscribe')
            return r
        except BadRequest:
            pass

    def add_tags(self, *tags):
        """Add tags to a mod, tags are case insensitive and duplicates will be removed. Tags
        which are not in the game's tag_options will not be added.

        |coro|

        Parameters
        -----------
        tags : List[str]
            list of tags to be added. 

        """
        self.get_tags()
        tags = list(set([tag.lower() for tag in tags if tag.lower() not in self.tags.keys()]))
        
        if not tags:
            raise modioException("No unique tags were submitted")

        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags}

        message = self._client._post_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)
        
        for tag in tags:
            self.tags[tag] = int(time.time())

        return Message(**message)

    def delete_tags(self, *tags):
        """Delete tags from the mod, tags are case insensitive and duplicates will be removed. Providing
        no arguments will remove every tag from the mod.

        |coro|

        Parameters
        -----------
        tags : list
            List of tags to remove, if no list is provided, will remove every tag from the mod.

        """
        self.get_tags()
        if tags:
            tags = list(set([tag.lower() for tag in tags if tag.lower() in self.tags.keys()]))
        else:
            tags = list(self.tags.keys())

        if not tags:
            raise modioException("No unique tags were submitted")

        fields = {f"tags[{tags.index(tag)}]" : tag for tag in tags} if tags else {"tags[]":""}

        r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}/tags', data = fields)

        for tag in tags:
            del self.tags[tag]
            
        return r

    def _add_rating(self, rating : RatingType):
        try:
            self._client._post_request(f'/games/{self.game}/mods/{self.id}/ratings', data={"rating":rating.value})
        except BadRequest:
            return False

        self.get_stats()
        return True

    def add_positive_rating(self):
        """Adds a good rating to the mod, the author of the rating will be the authenticated user.
        If the mod has already been rated by the user it will return False. If the positive rating
        is successful it will return True

        |coro|"""
        return self._add_rating(RatingType.good)

    def add_negative_rating(self):
        """Adds a bad rating to the mod, the author of the rating will be the authenticated user.
        If the mod has already been rated by the user it will return False. If the negative rating
        is successful it will return True.

        |coro|"""
        return self._add_rating(RatingType.bad)

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
        for data in metadata:
            metadata_d[f"metadata[{index}]"] = f"{data}:{':'.join(metadata[data])}"
            index += 1

        checked = self._client._post_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata_d)
        
        for key, value in metadata.items():
            for item in value:
                self._kvp_raw.append({"metakey" : key, "metavalue" : item})

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
        for data in metadata:
            metadata_d[f"metadata[{index}]"] = f"{data}{':' if len(metadata[data]) > 0 else ''}{':'.join(metadata[data])}"
            index += 1

        r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}/metadatakvp', data=metadata_d)

        for key, values in metadata.items():
            if not values:
                self._kvp_raw = [x for x in self._kvp_raw if x["metakey"] != key]
            else:
                self._kvp_raw = [x for x in self._kvp_raw if x["metakey"] != key and x["metavalue"] not in values]

        return r

    def add_dependencies(self, dependencies : list):
        """Add mod dependencies required by the corresponding mod. A dependency is a mod 
        that should be installed for this mod to run. 

        |coro|
        
        Parameters
        ----------
        dependencies : List[Union[int, Mod]]
            List of mod ids to submit as dependencies. 

        """
        dependency = {f"dependencies[{dependencies.index(data)}]" : getattr(data, "id", data) for data in dependencies}
        r = self._client._post_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependency)
        return Message(**r)

    def delete_dependencies(self, dependencies : list):
        """Delete mod dependecies required by this mod.

        |coro|

        Parameters
        -----------
        dependencies : List[Union[int, Mod]]
            List of dependencies to remove
        """
        dependency = {f"dependencies[{dependencies.index(data)}]" : getattr(data, "id", data) for data in dependencies}
        r = self._client._delete_request(f'/games/{self.game}/mods/{self.id}/dependencies', data=dependency)
        return r

    def add_team_member(self, email, level, *, position=None):
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
        data = {"email" : email, "level" : level.value, "position" : position}
        msg = self._client._post_request(f'/games/{self.game}/mods/{self.id}/team', data=data)
        return Message(**msg)

    def report(self, name, summary, type = Report(0)):
        """Report a this mod, make sure to read mod.io's ToU to understand what is
        and isnt allowed.

        |coro|

        Parameters
        -----------
        name : str
            Name of the report
        summary : str
            Detailed description of your report. Make sure you include all relevant information and 
            links to help moderators investigate and respond appropiately.
        type : Report
            Type of the report

        Returns
        --------
        Message
            The returned message on the success of the query.

        """
        fields = {
            "id" : self.id,
            "resource" :  "mods",
            "name" : name,
            "type" : type.value,
            "summary" : summary
        }

        msg = self._client._post_request('/report', data = fields)
        return Message(**msg)

