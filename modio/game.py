import requests
import json
from .mod import Mod
from .objects import *
from .utils import find
from .errors import *
BASE_PATH = "https://api.test.mod.io/v1"

class Game:
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id", None)
        self.status = attrs.pop("status", None)
        self.submitter = User(**attrs.pop("submitted_by", None))
        self.date_added = attrs.pop("date_added", None)
        self.date_updated = attrs.pop("date_updated", None)
        self.date_live = attrs.pop("date_live", None)
        self.presentation = attrs.pop("presentation_options", None)
        self.submission = attrs.pop("submission_options", None)
        self.curation = attrs.pop("curation_options", None)
        self.community = attrs.pop("community_options", None)
        self.revenue = attrs.pop("revenue_options", None)
        self.api = attrs.pop("api_options", None)
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
        self.tag_options = list()

        for tag in attrs.pop("tag_options", None):
            game_tag = GameTag(**tag)
            self.tag_options.append(game_tag)

        self.client = client

    def __cmp__(self, other):
        return self.id == other.id

    def get_mod(self, id : int):
        mod_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}".format(self.id, id))

        return Mod(self.client, **mod_json)

    def get_mods(self, **fields):
        mod_json = self.client._get_request(BASE_PATH + "/games/{}/mods".format(self.id))

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self.client, **mod))

        return mod_list

    def get_mod_events(self, **fields):
        event_json = self.client._get_request(BASE_PATH + "/games/{}/mods/events".format(self.id))

        event_list = list()
        for event in event_json["data"]:
            event_list.append(Event(**event))

        return event_list

    def get_tags(self, **fields):
        tag_json = self.client._get_request(BASE_PATH + "/games/{}/tags".format(self.id))

        tags_list = list()
        for tag_option in tag_json["data"]:
            tags_list.append(GameTag(**tag_option))

        return tags_list

    def edit(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }
        if all(item in self.__dict__.items() for item in fields.items()):
            return self

        r = requests.put(BASE_PATH + '/games/{}'.format(self.id), data = fields, headers = headers)

        return Game(self.client, **self.client._error_check(r))

    #still not working *bonks head on table*
    def add_mod(self, mod):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json'
        }

        r = requests.post(BASE_PATH + '/games/{}/mods'.format(self.id), data = {"logo" : mod.logo}, headers = headers)
        
        return Mod(self.client, **self.client._error_check(r))

    def add_media(self, media):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json'
        }

        r = requests.post(BASE_PATH + '/games/{}/media'.format(self.id), data = {"logo" : mod.logo}, headers = headers)
        
        return Message(**self.client._error_check(r))

    def add_tags(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        if "tags" in fields:
            tags = fields.pop("tags")
            for tag in tags:
                fields["tags[{}]".format(tags.index(tag))] = tag

        print(fields)
        r = requests.post(BASE_PATH + '/games/{}/tags'.format(self.id), data = {"input_json" : fields}, headers = headers)

        message = self.client._error_check(r)
        self.tag_options.append(GameTag(**fields))
        return Message(**message)

    def del_tags(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        if "tags" in fields:
            tags = fields.pop("tags")
            for tag in tags:
                fields["tags[{}]".format(tags.index(tag))] = tag

        r = requests.delete(BASE_PATH + '/games/{}/tags'.format(self.id), data = fields, headers = headers)

        try:
            r = self.client._error_check(r)
        except json.JSONDecodeError:
            pass


        for tag in self.tags:
            if tag.name in tags:
                self.tags.remove(tag)

        return r

