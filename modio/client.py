import requests
import json
import time
from typing import Union

from .game import Game
from .mod import Mod
from .errors import *
from .objects import *

class Client:
    """Represents the base-level client to make requests to the mod.io API with. Upon
    initializiation the Client will confirm the api key and O Auth 2 token.

    Parameters
    -----------
    api_key : Optional[str]
        The api key that will be used to authenticate the bot while it makes most of 
        its GET requests. This can be generated on the mod.io website. Optional if an access 
        token is supplied.
    auth : Optional[str]
        The O Auth 2 token that will be used to make more complex GET requests and to make
        POST requests. This can either be generated using the library's oauth2 functions
        or through the mod.io website. This is referred as an access token in the rest of
        the documentation. If an access token is supplied it will be used for all requests.
    lang : Optional[str]
        The mod.io API provides localization for a collection of languages. To specify 
        responses from the API to be in a particular language, simply provide the lang 
        parameter with an ISO 639 compliant language code. Else the language of the authenticated
        user will be used, default is US English.
    test : Optional[bool]
        Whether or not to use the mod.io test environment. If not included will default to False.
    version : Optional[str]
        An optional keyword argument to allow you to pick a specific version of the API to query,
        usually you shouldn't need to change this. This cannot be changed once set apart by forcibly
        overwriting BASE_PATH

    Attributes
    -----------
    rate_limit : int
        Number of requests that can be made using the supplied API Key/access token.
    rate_remain : int
        Number of requests remaining. Once this number hits 0 the requests will become 
        rejected and the library will sleep until the limit resets then raise 429 TooManyRequests.
    rate_retry : int
        Number of seconds until the rate limits are reset for this API Key/access token.
        Is 0 until the rate_remain is 0 and becomes 0 again once the rate limit is reset. 
    """

    def __init__(self, **fields):
        self.api_key = fields.pop("api_key", None)
        self.access_token = fields.pop("auth", None)
        self.lang = fields.pop("lang", "en")
        self.version = fields.pop("version", "v1")
        self.rate_limit = None
        self.rate_remain = None
        self.rate_retry = 0
        self.BASE_PATH = f"https://api.test.mod.io/{self.version}" if fields.pop("test", False) else f"https://api.mod.io/{self.version}"

        #check o auth 2 token
        if self.access_token:
            try:
                self.get_my_user()
            except Forbidden:
                raise Forbidden("O Auth 2 token invalid")
        else:
            #check api key if no o auth 2
            try:
                self.get_games()
            except Forbidden:
                raise Forbidden("API key invalid")

    def __repr__(self):
        return f"<modio.Client rate_limit={self.rate_limit} rate_retry={self.rate_retry} rate_remain={self.rate_remain}>"
    
    def _error_check(self, r):
        """Updates the rate-limit attributes and check validity of the request."""
        self.rate_limit = r.headers.get("X-RateLimit-Limit", self.rate_limit)
        self.rate_remain = r.headers.get("X-RateLimit-Remaining", self.rate_remain)
        self.rate_retry = r.headers.get("X-Ratelimit-RetryAfter", 0)

        try:
            request_json = r.json()
        except json.JSONDecoderError:
            return r

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
                if "errors" in request_json["error"]:
                    errors = request_json["error"]["errors"]
                else:
                    errors = None
                raise UnprocessableEntity(msg, errors)
            elif code == 429:
                time.sleep(self.rate_retry) #feeble attempt at handling rate limits
                raise TooManyRequests(msg, self.rate_retry)
                self.rate_retry = 0
            else:
                raise modioException(msg)
        else:
            return request_json

    def _get_request(self, url, **fields):
        filter = (fields.pop("filter") if fields.get("filter") else Filter()).__dict__.copy()
        extra = {**filter, **fields}

        if not self.access_token:
            headers = {
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }

            r = requests.get(self.BASE_PATH + url, params={
              'api_key': self.api_key,
              **extra
            }, headers = headers)
        else:
            headers = {
              'Accept': 'application/json',
              'Authorization': "Bearer " + self.access_token,
              'Accept-Language': self.lang
            }

            r = requests.get(self.BASE_PATH + url, headers = headers, params=extra)

        return self._error_check(r)

    def _define_headers(self, h_type):
        if h_type == 0:
            headers = {
              'Authorization': 'Bearer ' + self.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }
        elif h_type == 1:
            headers = {
              'Authorization': 'Bearer ' + self.access_token,
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }
        elif h_type == 2:
            headers = {
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }

        return headers

    def _post_request(self, url, *, h_type=0, **fields):
        if not self.access_token:
            fields["api_key"] = self.api_key
            h_type = 2

        r = requests.post(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        r = self._error_check(r)

        return r

    def _put_request(self, url, *, h_type=0, **fields):
        if not self.access_token:
            fields["api_key"] = self.api_key
            h_type = 2

        r = requests.put(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        r = self._error_check(r)

        return r

    def _delete_request(self, url, *, h_type=0, **fields):
        if not self.access_token:
            fields["api_key"] = self.api_key
            h_type = 2

        r = requests.delete(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        r = self._error_check(r)

        return r

    def get_game(self, id : int):
        """Queries the mod.io API for the given game ID and if found returns it as a 
        modio.Game instance. If not found raises NotFound

        Parameters
        -----------
        id : int
            The ID of the game to query the API for

        Raises
        -------
        NotFound
            A game with the supplied id was not found.

        Returns
        --------
        :class: `Game`
            The game with the given ID
        
        """
        game_json = self._get_request(f'/games/{id}')
        return Game(client=self, **game_json)

    def get_games(self, *, filter=None):
        """Gets all the games available on mod.io. Takes filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list
            A list of modio.Game instances
               
        """
        game_json = self._get_request('/games', filter=filter)
        return [Game(client=self, **game) for game in game_json["data"]]

    def get_user(self, id : int):
        """Gets a user with the specified ID.

        Parameters
        -----------
        id : int
            The ID of the user to query the API for

        Raises
        -------
        NotFound
            A user with the supplied id was not found.

        Returns
        --------
        :class: `User`
            The user with the given ID

        """
        user_json = self._get_request(f"/users/{id}")
        return User(**user_json)

    def get_users(self, *, filter=None):
        """Gets all the users availaible on mod.io. Takes filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list
            A list of modio.User instances
               
        """
        user_json = self._get_request("/users", filter=filter)
        return [User(**user) for user in user_json["data"]]

    def get_my_user(self):
        """Gets the authenticated user's details (aka the user who created the API key/access token)
        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        User
            The authenticated user
        
        """
        me_json = self._get_request("/me")
        return User(**me_json)

    def get_my_subs(self, *, filter=None):
        """Gets all the mods the authenticated user is subscribed to.  Takes
        filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        list
            A list of modio.Mod instances representing all mods the user is subscribed to
        """
        mod_json = self._get_request("/me/subscribed", filter=filter)
        return [Mod(client=self, **mod) for mod in mod_json["data"]]

    def get_my_events(self, *, filter=None):
        """Get events that have been fired specifically for the authenticated user. Takes
        filtering argmuments

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list : Events
            list of events related to the user
        """
        events_json = self._get_request("/me/events", filter=filter)
        return [Event(**event) for event in events_json["data"]]

    def get_my_games(self, filter=None):
        """Get all the games the authenticated user added or is a team member of. Takes
        filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        list
            A list of modio.Game instances representing all games the user is added or is team member of
        """
        game_json = self._get_request("/me/games", filter=filter)
        return [Game(client=self, **game) for game in game_json["data"]]

    def get_my_mods(self, *, filter=None):
        """Get all the mods the authenticated user added or is a team member of. Takes
        filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        list
            A list of modio.Mod instances representing all mods the user is added or is team member of
        """
        mod_json = self._get_request("/me/mods", filter=filter)
        return [Mod(client=self, **mod) for mod in mod_json["data"]]

    def get_my_modfiles(self, *, filter=None):
        """Get all the mods the authenticated user uploaded. The returned modfile objects cannot be
        edited or deleted and do not have a `game_id` attribute. Takes filtering arguments.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        list
            A list of modio.ModFile instances representing all modfiles the user added.
        """
        files_json = self._get_request("/me/files", filter=filter)
        return [ModFile(**file, client=self) for file in files_json["data"]]
        
    def email_request(self, email : str):
        """Posts an email request for an OAuth2 token. A code will be sent to the given email address
        which can then be entered into :func:`email_exchange`.
        
        Parameters
        ----------
        email : str
            A valid email to which the 5-digit code will be sent

        """

        headers = {
          'Accept': 'application/json',
          'Content-Type': "application/x-www-form-urlencoded"
        }

        r = requests.post(self.BASE_PATH + "/oauth/emailrequest", params={
          'api_key': self.api_key,
          'email' : email
        }, headers = headers)

        return Message(**self._error_check(r))

    def email_exchange(self, code : int):
        """Exchanges the given 5-digit code for an OAuth2 token.

        Parameters
        ----------
        code : int
            A 5-digit code received by email less than 15 minutes ago

        Raises
        -------
        Unauthorized
            Invalid security code
        ValueError
            Security code was not 5 digits long

        Returns
        --------
        str
            The access code. The access code will also be added directly to the Client's `access_token` 
            attribute.
        """
        headers = {
          'Accept': 'application/json',
          'Content-Type': "application/x-www-form-urlencoded"
        }

        if len(code) != 5:
            raise ValueError("Security code must be 5 digits")

        r = requests.post(self.BASE_PATH + "/oauth/emailexchange", params={
          'api_key': self.api_key,
          'security_code' : code
        }, headers = headers)

        r = self._error_check(r)
        self.access_token = r["access_token"]

        return r["access_token"]

    def report(self, *, resource : Union[Game, User, Mod, Object], type : int = 0, name : str, summary : str):
        """Used to report for any resource on mod.io. Make sure to read mod.io's ToU to understand
        what is and isn't acceptable

        Parameters
        -----------
        resource : Union[modio.Game, modio.User, modio.Mod, modio.Object]
            The resource to report, if it is an instance of a modio.Object it must have an `id`
            attribute (the id of the resource) and a `resource_name`  atttribute which can be either 
            'games', 'mods' or 'users'
        type : int
            0 : Generic Report
            1 : DMCA Report
        name : str
            Name of the report
        summary : str
            Detailed description of your report. Make sure you include all relevant information and 
            links to help moderators investigate and respond appropiately.

        Raises
        -------
        modioException
            Resource not 'game', 'mod' or 'user'

        Returns
        -------
        Message
            :class: `Message` 


        """
        resource_name = resource.__class__.__name__.lower()

        fields = {
            "id" : resource.id,
            "resource" :  resource_name + "s" if resource_name != "object" else resource.resource_name,
            "name" : name,
            "type" : type,
            "summary" : summary
        }

        if fields["resource"] not in ["games", "mods", "users"]:
            raise modioException("You cannot report this type of resources")

        msg = self._post_request('/report', data = fields)

        return Message(**msg)
        
