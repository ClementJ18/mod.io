import requests
from math import sqrt
import time

from .utils import find
from .objects import *
from .errors import *

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
        self.modfile = ModFile(**attrs.pop("modfile", None), game_id=self.game_id, client=client)
        self.media = ModMedia(**attrs.pop("media", None))
        self.maturity_options = attrs.pop("maturity_options", None)

        self.rating_summary = RatingSummary(**attrs.pop("rating_summary", None))
        self.client = client
        
        tags_list = list()
        tags = attrs.pop("tags", None)
        if not tags is None:
            for tag in tags:
                tags_list.append(ModTag(**tag))

        self.tags = tags_list

    def get_file(self, id : int):
        file_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/files/{id}")
        return ModFile(**file_json, game_id=self.game_id, client=self.client)

    def get_files(self, **fields):
        files_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/files", **fields)

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(**file, game_id=self.game_id, client=self.client))

        return file_list

    def get_events(self, **fields):
        event_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/events", **fields)

        event_list = list()
        for event in event_json["data"]:
            event_list.append(Event(**event))

        return event_list

    def get_tags(self, **fields): #in common with game obj
        tag_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/tags", **fields)

        tags_list = list()
        for tag_option in tag_json["data"]:
            tags_list.append(ModTag(**tag_option))

        return tags_list

    def get_meta(self):
        meta_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/metadatakvp")

        meta_list = list()
        for meta in meta_json["data"]:
            meta_list.append(MetaData(**meta))

        return meta_list

    def get_dependencies(self, **fields):
        depen_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/dependencies", **fields)

        depen_list = list()
        for dependecy in depen_json["data"]:
            depen_list.append(ModDependencies(**dependecy))

        return depen_list

    def get_team(self):
        team_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/team")

        team_list = list()
        for member in team_json["data"]:
            team_list.append(TeamMember(**member))

        return team_list

    def get_comments(self, **fields):
        comment_json = self.client._get_request(f"/games/{self.game_id}/mods/{self.id}/comments", **fields)

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

        if all(item in self.__dict__.items() for item in fields.items()):
            return self

        r = requests.put(f'/games/{self.game_id}/mods/{self.id}', data = fields, headers = headers)

        return Mod(self.client, **self.client._error_check(r))

    def delete(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}', headers = headers)

        return self.client._error_check(r)

    def add_file(self, file):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Accept': 'application/json'
        }

        if not isinstance(file, NewFile):
            raise modioException("mod argument must be type modio.NewFile")

        file_d = file.__dict__
        files = {"filedata" : file_d.pop("file")}
        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/files', data = file_d, files=files, headers = headers)

        return ModFile(**self.client._error_check(r))

    def add_media(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Accept': 'application/json'
        }

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/media', files = fields, headers = headers)

        return Message(**self.client._error_check(r))

    def delete_media(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/media', headers = headers)
        r = self.client._error_check(r)

        return r

    def subscribe(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/subscribe', headers = headers)

        return Mod(self.client, **self.client._error_check(r))

    def unsubscribe(self):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/subscribe', headers = headers)
        r = self.client._error_check(r)
        return r

    def add_tags(self, *tags):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        fields = dict()
        for tag in tags:
            fields[f"tags[{tags.index(tag)}]"] = tag

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/tags', data = fields, headers = headers)

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
            fields[f"tags[{tags.index(tag)}]"] = tag

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/tags', data = fields, headers = headers)
        r = self.client._error_check(r)

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

        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/rating', data={"rating":rating}, headers=headers)

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

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/metadatakvp', data=metadata, headers=headers)
        checked = self.client._error_check(r)
            
        return Message(**checked)

    def del_meta(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        metadata = dict()
        index = 0
        for data in fields:
            metadata[f"metadata[{index}]"] = f"{data}:{fields[data]}"
            index += 1

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/metadatakvp', data=metadata, headers=headers)
        r = self.client._error_check(r)

        return r

    def add_depen(self, dependencies : list):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        #to add more than 5 depen at a time
        # composite_list = [dependencies[x:x+5] for x in range(0, len(dependencies)-5, 5)]
        # for depend in composite_list:
        #     dependecy = dict()
        #     for data in depend:
        #         dependecy["dependencies[{}]".format(depend.index(data))] = data

        #     r = requests.post('/games/{self.game_id}/mods/{self.id}/dependencies'.format(self.game_id, self.id), data=dependecy, headers=headers)
        #     self.client._error_check(r)

        # return "all good"

        if len(dependencies) > 5:
            raise modioException("You can only submit 5 dependencies at a time")

        dependecy = dict()
        for data in dependencies:
            dependecy[f"dependencies[{dependencies.index(data)}]"] = data

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/dependencies', data=dependecy, headers=headers)

        return Message(**self.client._error_check(r))


    def del_depen(self, dependencies : list):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        dependecy = dict()
        for data in dependencies:
            dependecy[f"dependencies[{dependencies.index(data)}]"] = data

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/dependencies', data=dependecy, headers=headers)
        r = self.client._error_check(r)

        return r

    def add_team_member(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.post(f'/games/{self.game_id}/mods/{self.id}/team', data=fields, headers=headers)

        return Message(**self.client._error_check(r))



    def update_team_member(self, **fields):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.put(f'/games/{self.game_id}/mods/{self.id}/team/{id}', data=fields, headers=headers)

        return Message(**self.client._error_check(r))

    def del_team_member(self, id : int):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/team/{id}', headers=headers)
        r = self.client._error_check(r)

        return r

    def del_comment(self, id):
        headers = {
          'Authorization': 'Bearer ' + self.client.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        r = requests.delete(f'/games/{self.game_id}/mods/{self.id}/comments/{id}', headers=headers)
        r = self.client._error_check(r)

        return r
