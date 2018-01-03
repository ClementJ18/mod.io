import requests
from .mod import Mod
from .objects import *
BASE_PATH = "https://api.mod.io/v1"

class Game:
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id", None)
        self.submitter = User(**attrs.pop("submitted_by", None))
        self.date_added = attrs.pop("date_added", None)
        self.date_updated = attrs.pop("date_updated", None)
        self.date_live = attrs.pop("date_live", None)
        self.presentation = attrs.pop("presentation", None)
        self.submission = attrs.pop("submission", None)
        self.curation = attrs.pop("curation", None)
        self.community = attrs.pop("community", None)
        self.revenue = attrs.pop("revenue", None)
        self.api = attrs.pop("api", None)
        self.ugc_name = attrs.pop("ugc_name", None)
        self.icon = Image(**attrs.pop("icon", None))
        self.logo = Image(**attrs.pop("logo", None))
        self.header = Image(**attrs.pop("header", None))
        self.homepage = attrs.pop("homepage", None)
        self.name = attrs.pop("name", None)
        self.name_id = attrs.pop("name_id", None)
        self.summary = attrs.pop("summary", None)
        self.instructions = attrs.pop("instructions", None)
        self.profile_url = attrs.pop("profile_url", None)
        self.tag_options = attrs.pop("tag_options", None)
        self.client = client

    def get_mod(self, id : int):
        mod_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}".format(self.id, id))

        return Mod(self.client, **mod_json)

    def get_mods(self):
        mod_json = self.client._get_request(BASE_PATH + "/games/{}/mods".format(self.id))

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self.client, **mod))

        return mod_list

    def get_activity(self): #in common with mod obj
        activity_json = self.client._get_request(BASE_PATH + "/games/{}/activity".format(self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(GameActivity(**activity))

        return activity_list

    def get_mods_activity(self):
        activity_json = self.client._get_request(BASE_PATH + "/games/{}/mods/activity".format(self.id))

        activity_list = list()
        for activity in activity_json["data"]:
            activity_list.append(ModActivity(**activity))

        return activity_list

    def get_tags(self): #in common with mod obj
        tag_json = self.client._get_request(BASE_PATH + "/games/{}/tags".format(self.id))

        tags_list = list()
        for tag_option in tag_json["data"]:
            tags_list.append(GameTag(**tag_option))

        return tags_list

    def get_team(self): #in common with mod obj
        team_json = self.client._get_request(BASE_PATH + "/games/{}/team".format(self.id))

        team_list = list()
        for team_member in team_json["data"]:
            team_list.append(TeamMember(**team_member))

        return team_list

    def edit(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.put(BASE_PATH + '/games/{}'.format(self.id), params= fields, headers = headers)

        self.__init__(self.client, **self.client._error_check(r))

    def add_mod(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json'
        }

        r = requests.post(BASE_PATH + '/games/{}/mods'.format(self.id), params= fields, headers = headers)

        return Mod(self.client, **self.client._error_check(r))

    def add_tag(self, **fields):
        pass

    def del_tag(self, **fields):
        pass

    def add_team_member(self, **fields):
        pass

    def update_team_member(self, **fields):
        pass

    def del_team_member(self, **fields):
        pass

