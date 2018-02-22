import requests
import json

from .game import Game
from .mod import Mod
from .errors import *
from .objects import *
from .utils import *

BASE_PATH = "https://api.test.mod.io/v1"

class Client:
    """Represents the base-level client to make requests to the mod.io API with.

    Parameters
    -----------
    api_key : str
        The api key that will be used to authenticate the bot while it makes most of 
        its GET requests. This can be generated on the mod.io website.
    auth : Optional[str]
        The O Auth 2 token that will be used to make more complex GET requests and to make
        POST requests. This can either be generated using the library's oauth2 functions
        or through the mod.io website. This is referred as an access token in the rest of
        the documentation.

    Attributes
    -----------
    rate_limit : int
        Number of requests that can be made using the supplied API Key/access token. Is
        None until first request is made.
    rate_remain : int
        Number of requests remaining. Once this number hits 0 the requests will become 
        rejected and the library will return 429 TooManyRequests. Is None until first
        request is made
    rate_retry : int
        Number of minutes until the rate limits are reset for this API Key/access token.
        Is None until the rate_remain is 0. 
    """

    def __init__(self, **fields):
        self.api_key = fields.pop("api_key")
        self.access_token = fields.pop("auth", None)
        self.rate_limit = None
        self.rate_remain = None
        self.rate_retry = None

    def _error_check(self, r):
        """Updates the rate-limit attributes and check validity of the request."""
        self.rate_limit = r.headers.get("X-RateLimit-Limit", self.rate_limit)
        self.rate_remain = r.headers.get("X-RateLimit-Remaining", self.rate_remain)
        self.rate_retry = r.headers.get("X-Ratelimit-RetryAfter", None)
        request_json = r.json()

        if "error" in request_json:
            code = request_json["error"]["code"]
            msg = request_json["error"]["message"]
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
                errors = request_json["error"]["errors"]
                raise UnprocessableEntity(msg, errors)
            elif code == 429:
                raise TooManyRequests(msg, self.rate_retry)
            else:
                raise ModDBException(msg)
        else:
            return request_json

    def _get_request(self, url, need_token=False, **fields):
        """Contains the code for GET request. Adapts the given search terms to 
        fit the API requirements."""
        extra = dict()
        if "limit" in fields:
            extra["_limit"] = int(fields.pop("limit"))

        if "offset" in fields:
            extra["_offset"] = int(fields.pop("offset"))

        if "name" in fields:
            extra["_q"] = fields.pop("name")

        if "sort" in fields:
            extra["_sort"] = fields.pop("sort")

        fields = {k.replace("_", "-") : v for k, v in fields.items()}
        extra = {**extra, **fields}

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
              'api_key': self.api_key,
              **extra
            }, headers = headers)

        return self._error_check(r)

    def get_game(self, id : int):
        game_json = self._get_request(BASE_PATH + '/games/{}'.format(id))
        return Game(self, **game_json)

    def get_games(self, **fields):
        game_json = self._get_request(BASE_PATH + '/games', **fields)

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(self, **game))

        return game_list

    def get_users(self, **fields):
        user_json = self._get_request(BASE_PATH + "/users", **fields)

        user_list = list()
        for user in user_json["data"]:
            user_list.append(User(**user))

        return user_list

    def get_user(self, id):
        user_json = self._get_request(BASE_PATH + "/users/{}".format(id))

        return User(**user_json)

    def get_me(self):
        me_json = self._get_request(BASE_PATH + "/me", True)

        return User(**me_json)

    def get_me_sub(self, **fields):
        mod_json = self._get_request(BASE_PATH + "/me/subscribed", True, **fields)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self, **mod))

        return mod_list

    def get_me_games(self, **fields):
        game_json = self._get_request(BASE_PATH + "/me/games", True, **fields)

        game_list = list()
        for game in game_json["data"]:
            game_list.append(Game(self, **game))

        return game_list

    def get_me_mods(self, **fields):
        mod_json = self._get_request(BASE_PATH + "/me/mods", True, **fields)

        mod_list = list()
        for mod in mod_json["data"]:
            mod_list.append(Mod(self, **mod))

        return mod_list

    def get_me_modfiles(self, **fields):
        files_json = self._get_request(BASE_PATH + "/me/files", True, **fields)

        file_list = list()
        for file in files_json["data"]:
            file_list.append(MeModFile(**file))

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

    def report(self, *, resource, type=0, name, summary):
        headers = {
          'Authorization': 'Bearer ' + self.access_token,
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }

        fields = {
            "id" : resource.id,
            "resource" : str(type(resource).__name__).lower() + "s",
            "name" : name,
            "type" : type,
            "summary" : summary
        }

        if fields["resource"] not in ["games", "mods", "users"]:
            raise ModDBException("You cannot report this type of resources")

        r = requests.post(BASE_PATH + '/report', data = fields, headers = headers)

        return Message(**self._error_check(r))
        
