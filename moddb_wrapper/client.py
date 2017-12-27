import requests
from errors import *

class Client:
    def __init__(self, api_key, access_token=None):
        self.api_key = api_key
        self.access_token = access_token
        self.headers = {
          'Accept': 'application/json'
        }

    def _get_request(self, url, need_token=False):
        if self.access_token is None:
            headers = {
              'Accept': 'application/json'
            }
        else:
            headers = {
              'Accept': 'application/json',
              'Authorization': self.access_token
            }

        if need_token:
            r = requests.get(url, 
                headers = headers)
        else:
            r = requests.get(url, params={
              'api_key': self.api_key
            }, headers = headers)

        if "error" in r.json():
            code = r.json()["error"]["code"]
            if code == 400:
                raise BadRequest()
            elif code == 401:
                raise Unauthorized()
            elif code == 403:
                raise Forbidden()
            elif code == 404:
                raise NotFound()
            elif code == 405:
                raise MethodNotAllowed()
            elif code == 406:
                raise NotAcceptable()
            elif code == 410:
                raise Gone()
            elif code == 422:
                raise UnprocessableEntity()
            elif code == 429:
                raise TooManyRequests()
            else:
                raise ModDBException(r.json()["error"]["message"])

            
        else:
            return r.json()

    def get_game(self, id):
        game_json = self._get_request('https://api.mod.io/v1/games/{}'.format(id))
        return Game(game_json, self)

    def get_games(self):
        game_json = self._get_request('https://api.mod.io/v1/games')

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(game, self))

        return game_list

    def get_users(self):
        user_json = self._get_request("https://api.mod.io/v1/users")

        user_list = list()
        for user in user_json["data"]:
            user_list.append(User(user))

        return user_list


    def get_user(self, id):
        user_json = self._get_request("https://api.mod.io/v1/users/{}".format(id))

        return User(user_json)

    def get_me(self):
        me_json = self._get_request("https://api.mod.io/v1/me", True)

        return User(me_json)

    def get_me_sub(self):
        mod_json = self._get_request("https://api.mod.io/v1/me/subscribed", True)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(mod, self))

        return mod_list

    def get_me_games(self):
        game_json = self._get_request('https://api.mod.io/v1/me/games', True)

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(game, self))

        return game_list

    def get_me_mods(self):
        mod_json = self._get_request("https://api.mod.io/v1/me/mods", True)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(mod, self))

        return mod_list

    def get_me_modfiles(self):
        files_json = self._get_request("https://api.mod.io/v1/me/files", True)

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(file))

        return file_list

class Game:
    def __init__(self, game_json, client):
        self.id = game_json["id"]
        self.submitter = User(game_json["submitted_by"])
        self.date_added = game_json["date_added"]
        self.date_updated = game_json["date_updated"]
        self.date_live = game_json["date_live"]
        self.presentation = game_json["presentation"]
        self.submission = game_json["submission"]
        self.curation = game_json["curation"]
        self.community = game_json["community"]
        self.revenue = game_json["revenue"]
        self.api = game_json["api"]
        self.ugc_name = game_json["ugc_name"]
        self.icon = Image(game_json["icon"])
        self.logo = Image(game_json["logo"])
        self.header = Image(game_json["header"])
        self.homepage = game_json["homepage"]
        self.name = game_json["name"]
        self.name_id = game_json["name_id"]
        self.summary = game_json["summary"]
        self.instructions = game_json["instructions"]
        self.profile_url = game_json["profile_url"]
        self.tag_options = game_json["tag_options"]
        self.client = client

    def get_mod(self, id):
        mod_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}".format(self.id, id))

        return Mod(mod_json, self.client)

    def get_mods(self):
        mod_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods".format(self.id))

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(mod), self.client)

        return mod_list

    def get_activity(self): #in common with mod obj
        activity_json = self.client._get_request("https://api.mod.io/v1/games/{}/activity".format(self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(GameActivity(activity))

        return activity_list

    def get_mods_activity(self):
        activity_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/activity".format(self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(ModActivity(activity))

        return activity_list

    def get_tags(self): #in common with mod obj
        tag_json = self.client._get_request("https://api.mod.io/v1/games/{}/tags".format(self.id))

        tags_list = list()
        for tag_option in tag_json["data"]:
            tag_list.append(GameTag(tag_option))

        return tag_list

    def get_team(self): #in common with mod obj
        team_json = self.client._get_request("https://api.mod.io/v1/games/{}/team".format(self.id))

        team_list = list()
        for team_member in team_json["data"]:
            team_list.append(TeamMember(team_member))

        return team_list

class Mod:
    def __init__(self, mod_json, client):
        self.id = mod_json["id"]
        self.game_id = mod_json["game_id"]
        self.submitter = User(mod_json["submitted_by"])
        self.date_added = mod_json["date_added"]
        self.date_updated = mod_json["date_updated"]
        self.date_live = mod_json["date_live"]
        self.logo = Image(mod_json["logo"])
        self.homepage = mod_json["homepage"]
        self.name = mod_json["name"]
        self.name_id = mod_json["name_id"]
        self.summary = mod_json["summary"]
        self.description = mod_json["description"]
        self.metadata_blob = mod_json["metadata_blob"]
        self.profile_url = mod_json["profile_url"]
        self.modfile = ModFile(mod_json["modfile"])
        self.media = ModMedia(mod_json["media"])
        self.rating_summary = RatingSummary(mod_json["rating_summary"])
        self.client = client
        
        tag_list = list()
        for tag in mod_json["tags"]:
            tag_list.append(Tag(tag))

        self.tags = tag_list

    def get_file(self, id):
        file_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/files/{}".format(self.game_id, self.id, id))
        return ModFile(file_json)

    def get_files(self):
        files_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/files".format(self.game_id, self.id))

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(file))

        return file_list

    def get_activity(self): #in common with game obj
        activity_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/activity".format(self.mod_id, self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(ModActivity(activity))

        return activity_list

    def get_tags(self): #in common with game obj
        tag_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/tags".format(self.mod_id, self.id))

        tags_list = list()
        for tag_option in tag_json["data"]:
            tag_list.append(ModTag(tag_option))

        return tag_list

    def get_meta(self):
        meta_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/metadatakvp".format(self.mod_id, self.id))

        meta_list = list()
        for meta in meta_json["data"]:
            meta_list.append(MetaData(meta))

    def get_dependencies(self):
        depen_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/dependecies".format(self.mod_id, self.id))

        depen_list = list()
        for dependecy in depen_json["data"]:
            depen_list.append(ModDependencies(dependecy))

        return depen_list

    def get_team(self): #in common with game obj
        team_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/team".format(self.mod_id, self.id))

        team_list = list()
        for member in team_json["data"]:
            team_list.append(TeamMember(member))

        return team_list

    def get_comments(self):
        comment_json = self.client._get_request("https://api.mod.io/v1/games/{}/mods/{}/comments".format(self.mod_id, self.id))

        comment_list = list()
        for comment in comment_json["data"]:
            comment_list.append(Comment(comment))

        return comment_list

class Message:
    def __init__(self, message_json):
        self.code = message_json["code"]
        self.message = message_json["message"]

class Error:
    def __init__(self, error):
        self.code = error["code"]
        self.message = error["message"]
        self.errors = error["errors"]

class Image: #is used for Logo Object, Icon Object, Header Object, Avatar Object and Image Object
    def __init__(self, img_json):
        self.filename = img_json["filename"]
        self.original = img_json["original"]
        if len(img_json) > 2:
            self.small = list(img_json.values())[2]
        if len(img_json) > 3:
            self.medium = list(img_json.values())[3]
        if len(img_json) > 4:
            self.large = list(img_json.values())[4]

class GameActivity:
    def __init__(self, activity_json):
        self.id = activity_json["id"]
        self.game_id = activity_json["game_id"]
        self.user_id = activity_json["user_id"]
        self.date_added = activity_json["date_added"]
        self.event = activity_json["event"]

        changes_list = list()
        for change in activity_json["changes"]:
            changes_list.append(FieldChange(change))

        self.changes = changes_list

class ModActivity:
    def __init__(self, activity_json):
        self.id = activity_json["id"]
        self.mod_id = activity_json["mod_id"]
        self.user_id = activity_json["user_id"]
        self.date_added = activity_json["date_added"]
        self.event = activity_json["event"]
        
        changes_list = list()
        for change in activity_json["changes"]:
            changes_list.append(FieldChange(change))

        self.changes = changes_list

class FieldChange:
    def __init__(self, field_json):
        self.field = field_json["field"]
        self.before = field_json["before"]
        self.after = field_json["after"]

class Comment:
    def __init__(self, comment_json):
        self.id = comment_json["id"]
        self.mod_id = comment_json["mod_id"]
        self.submitter = User(comment_json["submitter"])
        self.date_added = comment_json["date_added"]
        self.reply_id = comment_json["reply_id"]
        self.reply_position = comment_json["reply_position"]
        self.karma = comment_json["karma"]
        self.karma_guest = comment_json["karma_guest"]
        self.content = comment_json["content"]

class ModDependencies:
    def __init__(self, dependecies_json):
        self.mod_id = dependecies_json["mod_id"]
        self.date_added = dependecies_json["date_added"]

class ModFile:
    def __init__(self, modfile_json):
        self.id = modfile_json["id"]
        self.mod_id = modfile_json["mod_id"]
        self.date_added = modfile_json["date_added"]
        self.date_scanned = modfile_json["date_scanned"]
        self.virus_status = modfile_json["virus_status"]
        self.virus_positive = modfile_json["virus_positive"]
        self.virustotal_hash = modfile_json["virustotal_hash"]
        self.filesize = modfile_json["filesize"]
        self.filehash = modfile_json["filehash"]["md5"]
        self.filename = modfile_json["filename"]
        self.version = modfile_json["version"]
        self.changelog = modfile_json["changelog"]

class ModMedia:
    def __init__(self, media_json):
        self.youtube = media_json["youtube"]
        self.sketchfab = media_json["sketchfab"]

        images_list = list()
        for image in media_json["images"]:
            images_list.append(Image(image))

        self.images = images_list

class ModTag:
    def __init__(self, tag_json):
        self.name = tag_json["name"]
        self.date_added = tag_json["date_added"]

class GameTag:
    def __init__(self, tag_json):
        self.name = tag_json["name"]
        self.type = tag_json["type"]
        self.hidden = tag_json["hidden"]
        self.tags = tag_json["tags"]

class MetaData:
    def __init__(self, meta_json):
        self.key = meta_json["key"]
        self.value = meta_json["value"]

class RatingSummary:
    def __init__(self, rating_json):
        self.total_ratings = rating_json["total_ratings"]
        self.positive_ratings = rating_json["positive_ratings"]
        self.negative_ratings = rating_json["negative_ratings"]
        self.percentage_positive = rating_json["percentage_positive"]
        self.weighted_aggregate = rating_json["weighted_aggregate"]
        self.display_text = rating_json["display_text"]

class TeamMember:
    def __init__(self, member_json):
        self.id = member_json["id"]
        self.user = User(member_json["user"])
        self.level = member_json["level"]
        self.date_added = member_json["date_added"]
        self.position = member_json["position"]

class User:
    def __init__(self, user_json):
        self.id = user_json["id"]
        self.name_id = user_json["name_id"]
        self.username = user_json["username"]
        self.date_online = user_json["date_online"]
        self.avatar = Image(user_json["avatar"])
        self.timezone = user_json["timezone"]
        self.language = user_json["language"]
        self.profile_url = user_json["profile_url"]
