import requests
import json
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
        parameter with an ISO 639 compliant language code. Default is US English.
    test : Optional[bool]
        Whether or not to use the mod.io test environment. If not included will default to False.
    version : Optional[str]
        An optional keyword argument to allow you to pick a specific version of the API to query,
        usually you shouldn't need to change this. Default is the latest supported version.

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
        self._test = fields.pop("test", False)
        
        #check o auth 2 token
        if self.access_token:
            self.get_my_user()
        else:
            #check api key if no o auth 2
            self.get_games()

    @property
    def BASE_PATH(self):
        if self._test:
            return f"https://api.test.mod.io/{self.version}"
        else:
            f"https://api.mod.io/{self.version}"

    def __repr__(self):
        return f"<modio.Client rate_limit={self.rate_limit} rate_retry={self.rate_retry} rate_remain={self.rate_remain}>"
    
    def _error_check(self, r):
        """Updates the rate-limit attributes and check validity of the request."""
        self.rate_limit = r.headers.get("X-RateLimit-Limit", self.rate_limit)
        self.rate_remain = r.headers.get("X-RateLimit-Remaining", self.rate_remain)
        self.rate_retry = r.headers.get("X-Ratelimit-RetryAfter", 0)

        if r.status_code == 204:
            return r

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
                if "errors" in request_json["error"]:
                    errors = request_json["error"]["errors"]
                else:
                    errors = None
                raise UnprocessableEntity(msg, errors)
            elif code == 429:
                raise TooManyRequests(msg, self.rate_retry)
                self.rate_retry = 0
            else:
                raise modioException(msg)
        else:
            return request_json

    def _define_headers(self, h_type):
        if h_type == 0:
            #regular O auth 2 header when submitting data
            headers = {
              'Authorization': 'Bearer ' + self.access_token,
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }
        elif h_type == 1:
            #o auth 2 header for submitting multipart/data, had to remove Content-Type
            #because it is already added by the requests lib when defining a files parameter
            headers = {
              'Authorization': 'Bearer ' + self.access_token,
              'Accept': 'application/json',
              'Accept-Language': self.lang
            }
        elif h_type == 2:
            #header to use when making calls using the api key, the key itself is added in
            #the parameters in the methods below
            headers = {
              'Accept': 'application/json',
              'Accept-Language': self.lang,
              'Content-Type': 'application/x-www-form-urlencoded'
            }

        return headers

    def _get_request(self, url, *, h_type=0, **fields):
        filter = (fields.pop("filter") if fields.get("filter") else Filter()).__dict__.copy()
        extra = {**filter, **fields}

        if not self.access_token:
            extra["api_key"] = self.api_key
            h_type = 2

        r  = requests.get(self.BASE_PATH + url, headers=self._define_headers(h_type), params=extra)
        return self._error_check(r)

    def _post_request(self, url, *, h_type=0, **fields):
        r = requests.post(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        return self._error_check(r)

    def _put_request(self, url, *, h_type=0, **fields):
        r = requests.put(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        return self._error_check(r)

    def _delete_request(self, url, *, h_type=0, **fields):
        r = requests.delete(self.BASE_PATH + url, headers=self._define_headers(h_type), **fields)
        return self._error_check(r)

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
        Game
            The game with the given ID
        
        """
        game_json = self._get_request(f'/games/{id}')
        return Game(client=self, **game_json)

    def get_games(self, *, filter=None):
        """Gets all the games available on mod.io. Takes filtering arguments. Returns a 
        named tuple with parameters results and pagination.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.Game]
            A list of modio.Game instances
        modio.Pagination
            Pagination data       
        """
        game_json = self._get_request('/games', filter=filter)
        return Returned([Game(client=self, **game) for game in game_json["data"]], Pagination(**game_json))

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
        User
            The user with the given ID

        """
        user_json = self._get_request(f"/users/{id}")
        return User(client=self, **user_json)

    def get_users(self, *, filter=None):
        """Gets all the users availaible on mod.io. Takes filtering arguments. Returns 
        a named tuple with parameters results and pagination.

        Parameters
        -----------
        filter : Optional[modio.Filter]
            A instance of modio.Filter to be used for filtering, paginating and sorting 
            results

        Returns
        --------
        list[modio.User]
            A list of modio.User instances
        modio.Pagination
            Pagination data
               
        """
        user_json = self._get_request("/users", filter=filter)
        return Returned([User(client=self, **user) for user in user_json["data"]], Pagination(**user_json))
    
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
        return User(client=self, **me_json)

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
        list[modio.Mod]
            A list of modio.Mod instances representing all mods the user is subscribed to
        modio.Pagination
            Pagination data
        """
        mod_json = self._get_request("/me/subscribed", filter=filter)
        return Returned([Mod(client=self, **mod) for mod in mod_json["data"]], Pagination(**mod_json))

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
        list[modio.Events]
            list of events related to the user
        modio.Pagination
            Pagination data
        """
        events_json = self._get_request("/me/events", filter=filter)
        return Returned([Event(**event) for event in events_json["data"]], Pagination(**events_json))

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
        list[modio.Game]
            A list of modio.Game instances representing all games the user is added or is team member of
        modio.Pagination
            Pagination data
        """
        game_json = self._get_request("/me/games", filter=filter)
        return Returned([Game(client=self, **game) for game in game_json["data"]], Pagination(**game_json))

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
        list[modio.Mod]
            A list of modio.Mod instances representing all mods the user is added or is team member of
        modio.Pagination
            Pagination data
        """
        mod_json = self._get_request("/me/mods", filter=filter)
        return Returned([Mod(client=self, **mod) for mod in mod_json["data"]], Pagination(**mod_json))

    def get_my_modfiles(self, *, filter=None):
        """Get all the mods the authenticated user uploaded. The returned modfile objects cannot be
        edited or deleted and do not have a `game_id` attribute. Takes filtering arguments. Returns 
        a named tuple with parameters results and pagination.

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
        list[modio.ModFile]
            A list of modio.ModFile instances representing all modfiles the user added.
        modio.Pagination
            Pagination data
        """
        files_json = self._get_request("/me/files", filter=filter)
        return Returned([ModFile(**file, client=self) for file in files_json["data"]], Pagination(**files_json))

    def get_my_ratings(self, *, filter=None):
        """Get all the ratings the authentitated user has submitted. Takes filtering arguments. Returns a named
        with parameter results and pagination.

        Paramaters
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
        list[modio.Rating]
            A list of modio.Rating instances representing all ratings the user added.
        modio.Pagination
            Pagination data
        """

        ratings = self._get_request("/me/ratings", filter=filter)
        return Returned([Rating(**rating, client=self) for rating in ratings["data"]], Pagination(**ratings))
        
    def email_request(self, email : str):
        """Posts an email request for an OAuth2 token. A code will be sent to the given email address
        which can then be entered into :func:`email_exchange`.
        
        Parameters
        ----------
        email : str
            A valid email to which the 5-digit code will be sent

        """

        r = self._post_request("/oauth/emailrequest", params={'email' : email, 'api_key': self.api_key}, h_type = 2)
        return Message(**r)

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

        if len(code) != 5:
            raise ValueError("Security code must be 5 digits")

        r = self._post_request("/oauth/emailexchange", params={'security_code' : code, "api_key":self.api_key}, h_type=2)
        self.access_token = r["access_token"]

        return r["access_token"]        
        
