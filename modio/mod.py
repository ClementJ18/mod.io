import requests
from math import sqrt
import json
import time

from .utils import find
from .objects import *
from .errors import *
BASE_PATH = "https://api.test.mod.io/v1"

class Mod:
    def __init__(self, client, **attrs):
        self.id = attrs.pop("id", None)
        self.status = attrs.pop("status", None)
        self.visiable = attrs.pop("visible", None)
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
        self.modfile = ModFile(**attrs.pop("modfile", None), game_id=self.game_id)
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
        return ModFile(**file_json, game_id=self.game_id)

    def get_files(self, **fields):
        files_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/files".format(self.game_id, self.id))

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(**file, game_id=self.game_id))

        return file_list

    def get_events(self, **fields):
        event_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/events".format(self.game_id, self.id))

        event_list = list()
        for event in event_json["data"]:
            event_list.append(Event(**event))

        return event_list

    def get_tags(self, **fields): #in common with game obj
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

    def get_dependencies(self, **fields):
        depen_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/dependencies".format(self.game_id, self.id))

        depen_list = list()
        for dependecy in depen_json["data"]:
            depen_list.append(ModDependencies(**dependecy))

        return depen_list

    def get_team(self):
        team_json = self.client._get_request(BASE_PATH + "/games/{}/mods/{}/team".format(self.game_id, self.id))

        team_list = list()
        for member in team_json["data"]:
            team_list.append(TeamMember(**member))

        return team_list

    def get_comments(self, **fields):
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

    def add_media(self, **fields):
            headers = {
              'Authorization': 'Bearer ' + self.client.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json'
            }

            r = requests.post(BASE_PATH + '/games/{}/mods/{}/media/{}'.format(self.game_id, self.id, id), params= fields, headers = headers)

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

    def add_tags(self, *tags):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        fields = dict()
        for tag in tags:
            fields["tags[{}]".format(tags.index(tag))] = tag

        r = requests.post(BASE_PATH + '/games/{}/mods/{}/tags'.format(self.game_id, self.id), data = fields, headers = headers)

        message = self.client._error_check(r)
        for tag in tags:
            self.tags.append(ModTag(name=tag, date_added=int(time.time())))

        return Message(**message)

    def del_tags(self, *tags):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        fields = dict()
        for tag in tags:
            fields["tags[{}]".format(tags.index(tag))] = tag

        r = requests.delete(BASE_PATH + '/games/{}/mods/{}/tags'.format(self.game_id, self.id), data = fields, headers = headers)

        try:
            r = self.client._error_check(r)
        except json.JSONDecodeError:
            pass

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
            raise ModDBException("Rating is an argument that can only be 1 or -1")

        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.post(BASE_PATH + '/games/{}/mods/{}/rating'.format(self.game_id, self.id), data={"rating":rating}, headers=headers)

        checked = self.client._error_check(r)
        self.rating_summary.total_rating += 1
        if rating == 1:
            self.rating_summary.positive_ratings += 1
        else:
            self.rating_summary.negative_ratings += 1

        self.rating_summary.percentage_positive = int((self.rating_summary.positive_ratings / self.rating_summary.total_rating)*100)
        self.rating_summary.weighted_aggregate = confidence(self.rating_summary.positive_ratings, self.rating_summary.negative_ratings)
        #need to recalculate mod message

        return Message(**checked)

    #working?
    def add_meta(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        metadata = dict()
        index = 0
        for data in fields:
            metadata["metadata[{}]".format(index)] = "{}:{}".format(data, fields[data])
            index += 1

        r = requests.post(BASE_PATH + '/games/{}/mods/{}/metadatakvp'.format(self.game_id, self.id), data=metadata, headers=headers)
        checked = self.client._error_check(r)

        for data in fields:
            
        return Message(**checked)

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
