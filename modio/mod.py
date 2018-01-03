import requests
from .objects import *
BASE_PATH = "https://api.mod.io/v1"

class Mod:
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id", None)
        self.game_id = attrs.pop("game_id", None)
        self.submitter = User(**attrs.pop("submitted_by", None))
        self.date_added = attrs.pop("date_added", None)
        self.date_updated = attrs.pop("date_updated", None)
        self.date_live = attrs.pop("date_live", None)
        self.logo = Image(**attrs.pop("logo", None))
        self.homepage = attrs.pop("homepage", None)
        self.name = attrs.pop("name", None)
        self.name_id = attrs.pop("name_id", None)
        self.summary = attrs.pop("summary", None)
        self.description = attrs.pop("description", None)
        self.metadata_blob = attrs.pop("metadata_blob", None)
        self.profile_url = attrs.pop("profile_url", None)
        self.modfile = ModFile(**attrs.pop("modfile", None))
        self.media = ModMedia(**attrs.pop("media", None))
        self.rating_summary = RatingSummary(**attrs.pop("rating_summary", None))
        self.client = client
        
        tags_list = list()
        tags = attrs.pop("tags", None)
        if not tags is None:
            for tag in tags:
                tags_list.append(ModTag(**tag))

        self.tags = tags_list

    def get_file(self, id : int):
        file_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/files/{}".format(self.game_id, self.id, id))
        return ModFile(**file_json)

    def get_files(self):
        files_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/files".format(self.game_id, self.id))

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(**file))

        return file_list

    def get_activity(self): #in common with game obj
        activity_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/activity".format(self.game_id, self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(ModActivity(**activity))

        return activity_list

    def get_tags(self): #in common with game obj
        tag_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/tags".format(self.game_id, self.id))

        tags_list = list()
        for tag_option in tag_json["data"]:
            tags_list.append(ModTag(**tag_option))

        return tags_list

    def get_meta(self):
        meta_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/metadatakvp".format(self.game_id, self.id))

        meta_list = list()
        for meta in meta_json["data"]:
            meta_list.append(MetaData(**meta))

        return meta_list

    def get_dependencies(self):
        depen_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/dependecies".format(self.game_id, self.id))

        depen_list = list()
        for dependecy in depen_json["data"]:
            depen_list.append(ModDependencies(**dependecy))

        return depen_list

    def get_team(self): #in common with game obj
        team_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/team".format(self.game_id, self.id))

        team_list = list()
        for member in team_json["data"]:
            team_list.append(TeamMember(**member))

        return team_list

    def get_comments(self):
        comment_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/comments".format(self.game_id, self.id))

        comment_list = list()
        for comment in comment_json["data"]:
            comment_list.append(Comment(**comment))

        return comment_list

    def edit(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.put(BASE_PATH + '/games/{}/mods/{}'.format(self.game_id, self.id), params= fields, headers = headers)

        self.__init__(self.client, **self.client._error_check(r))

    def delete(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(BASE_PATH + '/games/{}/mods/{}'.format(self.game_id, self.id), params={}, headers = headers)

        return self.client._error_check(r)

    def add_file(self, **fields):
        pass

    def edit_file(self, id, **fields):
            headers = {
              'Authorization': 'Bearer ' + self.client.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json'
            }

            r = requests.put(BASE_PATH + '/games/{}/mods/{}/files/{}'.format(self.game_id, self.id, id), params= fields, headers = headers)

            return ModFile(self.client._error_check(r))

    def add_media(self, **fields):
        pass

    def edit_media(self, id, **fields):
            headers = {
              'Authorization': 'Bearer ' + self.client.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json'
            }

            r = requests.put(BASE_PATH + '/games/{}/mods/{}/media/{}'.format(self.game_id, self.id, id), params= fields, headers = headers)

            return ModMedia(**self.client._error_check(r))

    def delete_media(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(BASE_PATH + '/games/{}/mods/{}/media'.format(self.game_id, self.id), params={}, headers = headers)

        return ModMedia(**self.client._error_check(r))

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def add_tag(self, **fields):
        pass

    def del_tag(self, **fields):
        pass

    def add_rating(self, rating):
        pass

    def add_meta(self, **fields):
        pass

    def del_meta(self, **fields):
        pass

    def add_depen(self, **fields):
        pass

    def del_depen(self, **fields):
        pass

    def add_team_member(self, **fields):
        pass

    def update_team_member(self, **fields):
        pass

    def del_team_member(self, **fields):
        pass

    def del_comment(self, id):
        pass
