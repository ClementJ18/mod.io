import requests
from .game import Game
from .mod import Mod
from .errors import *
from .objects import *
from .utils import *

BASE_PATH = "https://api.mod.io/v1"

class Client:
    def __init__(self, api_key, access_token=None):
        self.api_key = api_key
        self.access_token = access_token

    def _error_check(self, r):
        if "error" in r.json():
            code = r.json()["error"]["code"]
            msg = r.json()["error"]["message"]
            if code == 400:
                raise BadRequest(msg)
            elif code == 401:
                raise Unauthorized(msg)
            elif code == 403:
                raise Forbidden(msg)
            elif code == 404:
                raise NotFound(msg)
            elif code == 405:
                raise MethodNotAllowed(msg)
            elif code == 406:
                raise NotAcceptable(msg)
            elif code == 410:
                raise Gone(msg)
            elif code == 422:
                errors = r.json()["error"]["errors"]
                raise UnprocessableEntity(msg, errors)
            elif code == 429:
                raise TooManyRequests(msg)
            else:
                raise ModDBException(msg)
        else:
            return r.json()

    def _get_request(self, url, need_token=False):
        if self.access_token is None:
            headers = {
              'Accept': 'application/json'
            }
        else:
            headers = {
              'Accept': 'application/json',
              'Authorization': "Bearer " + self.access_token
            }

        if need_token:
            r = requests.get(url, 
                headers = headers)
        else:
            r = requests.get(url, params={
              'api_key': self.api_key
            }, headers = headers)

        print(url)
        return self._error_check(r)

    def _post_request(self, url, file=False, **fields):
        if self.access_token is None:
            raise Forbidden("You need an O Auth 2 token to make write requests")

        if file:
            content_type = "multipart/form-data"
        else:
            content_type = "application/x-www-form-urlencoded"

        headers = {
          'Authorization': 'Bearer ' + self.access_token,
          'Content-Type': content_type,
          'Accept': 'application/json'
        }

        r = requests.post(url, params=fields, headers = headers)

        return self._error_check(r)

    def get_game(self, id : int):
        game_json = self._get_request('https://api.mod.io/v1/games/{}'.format(id))
        return Game(self, **game_json)

    def get_games(self):
        game_json = self._get_request('https://api.mod.io/v1/games')

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(self, **game))

        return game_list

    def get_users(self):
        user_json = self._get_request(BASE_PATH + "/users")

        user_list = list()
        for user in user_json["data"]:
            user_list.append(User(**user))

        return user_list

    def get_user(self, id : int):
        user_json = self._get_request(BASE_PATH + "/users/{}".format(id))

        return User(**user_json)

    def get_me(self):
        me_json = self._get_request(BASE_PATH + "/me", True)

        return User(**me_json)

    def get_me_sub(self):
        mod_json = self._get_request(BASE_PATH + "/me/subscribed", True)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self, **mod))

        return mod_list

    def get_me_games(self):
        game_json = self._get_request(BASE_PATH + "/me/games", True)

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(self, **game))

        return game_list

    def get_me_mods(self):
        mod_json = self._get_request(BASE_PATH + "/me/mods", True)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self, **mod))

        return mod_list

    def get_me_modfiles(self):
        files_json = self._get_request(BASE_PATH + "/me/files", True)

        file_list = list()
        for file in files_json["data"]:
            file_list.append(ModFile(**file))

        return file_list

    def email_request(self, email):
        headers = {
          'Accept': 'application/json',
          'Content-Type': "application/x-www-form-urlencoded"
        }

        r = requests.post(BASE_PATH + "/oauth/emailrequest", params={
          'api_key': self.api_key,
          'email' : email
        }, headers = headers)

        return Message(**self._error_check(r))

    def email_exchange(self, code):
        headers = {
          'Accept': 'application/json',
          'Content-Type': "application/x-www-form-urlencoded"
        }

        r = requests.post(BASE_PATH + "/oauth/emailexchange", params={
          'api_key': self.api_key,
          'security_code' : code
        }, headers = headers)

        return Message(**self._error_check(r))

    def report(self, **fields):
        message = self._post_request(BASE_PATH + '/report', False, **fields)

        return Message(**self._error_check(message))
