import requests
from .errors import ModDBException
BASE_PATH = "https://api.test.mod.io/v1"    

class Message:
    def __init__(self, **attrs):
        self.code = attrs.pop("code", None)
        self.message =attrs.pop("message", None)

    def __str__(self):
        return "{} : {}".format(self.code, self.message)

class Error:
    def __init__(self, **attrs):
        self.code = attrs.pop("code", None)
        self.message = attrs.pop("message", None)
        self.errors = attrs.pop("errors", None)

class Image:
    def __init__(self, **attrs):
        self.filename = attrs.pop("filename", None)
        self.original = attrs.pop("original", None)

        if len(attrs) > 2:
            self.small = list(attrs.values())[2]
        if len(attrs) > 3:
            self.medium = list(attrs.values())[3]
        if len(attrs) > 4:
            self.large = list(attrs.values())[4]            

class Event:
    def __init__(self, **attrs):
        self.id = attrs.pop("id", None)
        self.mod_id = attrs.pop("mod_id", None)
        self.user_id = attrs.pop("user_id", None)
        self.date_added = attrs.pop("date_added", None)
        self.event = attrs.pop("event_type", None)
        
class FieldChange:
    def __init__(self, **attrs):
        self.field = attrs.pop("field", None)
        self.before = attrs.pop("before", None)
        self.after = attrs.pop("after", None)

class Comment:
    def __init__(self, **attrs):
        self.id = attrs.pop("id", None)
        self.mod_id = attrs.pop("mod_id", None)
        self.submitter = User(**attrs.pop("submitter", None))
        self.date_added = attrs.pop("date_added", None)
        self.reply_id = attrs.pop("reply_id", None)
        self.reply_position = attrs.pop("reply_position", None)
        self.karma = attrs.pop("karma", None)
        self.karma_guest = attrs.pop("karma_guest", None)
        self.content = attrs.pop("content", None)

class ModDependencies:
    def __init__(self, **attrs):
        self.mod_id = attrs.pop("mod_id", None)
        self.date_added = attrs.pop("date_added", None)

class MeModFile:
    def __init__(self,**attrs):
        self.id = attrs.pop("id", None)
        self.mod_id = attrs.pop("mod_id", None)
        self.date_added = attrs.pop("date_added", None)
        self.date_scanned = attrs.pop("date_scanned", None)
        self.virus_status = attrs.pop("virus_status", None)
        self.virus_positive = attrs.pop("virus_positive", None)
        self.virustotal_hash = attrs.pop("virustotal_hash", None)
        self.filesize = attrs.pop("filesize", None)

        self.filehash = attrs.pop("filehash", None)
        if not self.filehash is None:
            self.filehash = self.filehash["md5"]

        self.filename = attrs.pop("filename", None)
        self.version = attrs.pop("version", None)
        self.changelog = attrs.pop("changelog", None)
        self.meta_data = attrs.pop("metadata_blob", None)
        self.download = attrs.pop("download", None)

        def edit_file(self, **fields):
            raise ModDBException("This endpoint cannot be used for ModFile object recuperated through the me/modfiles endpoint")

class ModFile(MeModFile):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.game_id = attrs.pop("game_id", None)

        #doesn't work
        def edit_file(self, **fields):
            headers = {
              'Authorization': 'Bearer ' + self.client.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json'
            }

            r = requests.put(BASE_PATH + '/games/{}/mods/{}/files/{}'.format(self.game_id, self.mod_id, self.id), params= fields, headers = headers)

            return ModFile(self.client._error_check(r))

class ModMedia:
    def __init__(self, **attrs):
        self.youtube = attrs.pop("youtube", None)
        self.sketchfab = attrs.pop("sketchfab", None)

        images_list = list()
        images = attrs.pop("images", None)
        if not images is None:
            for image in images:
                images_list.append(Image(**image))

        self.images = images_list

class ModTag:
    def __init__(self, **attrs):
        self.name = attrs.pop("name", None)
        self.date_added = attrs.pop("date_added", None)

    def __str__(self):
        return self.name

class GameTag:
    def __init__(self, **attrs):
        self.name = attrs.pop("name", None)
        self.type = attrs.pop("type", None)
        self.hidden = attrs.pop("hidden", None)
        self.tags = attrs.pop("tags", None)

    def __str__(self):
        return self.name

class MetaData:
    def __init__(self, **attrs):
        self.key = attrs.pop("metakey", None)
        self.value = attrs.pop("metavalue", None)

class RatingSummary:
    def __init__(self, **attrs):
        self.total_ratings = attrs.pop("total_ratings", None)
        self.positive_ratings = attrs.pop("positive_ratings", None)
        self.negative_ratings = attrs.pop("negative_ratings", None)
        self.percentage_positive = attrs.pop("percentage_positive", None)
        self.weighted_aggregate = attrs.pop("weighted_aggregate", None)
        self.display_text = attrs.pop("display_text", None)

class TeamMember:
    def __init__(self, **attrs):
        self.id = attrs.pop("id", None)
        self.user = User(**attrs.pop("user", None))
        self.level = attrs.pop("level", None)
        self.date_added = attrs.pop("date_added", None)
        self.position = attrs.pop("position", None)

class User:
    def __init__(self, **attrs):
        self.id = attrs.pop("id", None)
        self.name_id = attrs.pop("name_id", None)
        self.username = attrs.pop("username", None)
        self.date_online = attrs.pop("date_online", None)

        avatar = attrs.pop("avatar", None)

        if len(avatar.keys()) > 0:
            self.avatar = Image(**avatar)
        else:
            self.avatar = None

        self.timezone = attrs.pop("timezone", None)
        self.language = attrs.pop("language", None)
        self.profile_url = attrs.pop("profile_url", None)

class NewMod:
    def __init__(self, **attrs):
        self.name = attrs.pop("name")
        self.name_id = attrs.pop("name_id", None)
        self.summary = attrs.pop("summary")
        self.description = attrs.pop("description")
        self.homepage = attrs.pop("homepage", None)
        self.metadata_blob = attrs.pop("metadata_blob")
        self.stock = int(attrs.pop("stock"))
        self.tags = list()

    def add_tags(self, *args):
        self.tags += [tag for tag in args if tag not in self.tags]

    def add_logo(self, path):
        self.logo = open(path, "rb")

