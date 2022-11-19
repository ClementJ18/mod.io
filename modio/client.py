"""The Client object is the base class from which all the requests are made,
this is where you can get your  games, authentify and get the models for
your authenticated user.
"""
import asyncio
import datetime
import logging
import time
import aiohttp
import requests

from .errors import modioException
from .entities import Event, Message, ModFile, Rating, User
from .objects import Pagination, Returned, Filter
from .game import Game
from .mod import Mod


class Connection:
    """Class handling under the hood requests and ratelimits."""

    def __init__(self, api_key, access_token, lang, version, test):
        self.test = test
        self.version = version
        self.access_token = access_token
        self.api_key = api_key
        self.lang = lang

        self.rate_limit = None
        self.rate_remain = None
        self.retry_after = 0

        self.session = requests.Session()
        self._async_session = None

    @property
    def async_session(self):
        if self._async_session is None:
            raise AttributeError("No async session found, did you forget to use Client.start?")

        return self._async_session

    @async_session.setter
    def async_session(self, session):
        self._async_session = session

    @property
    def _base_path(self):
        if self.test:
            return f"https://api.test.mod.io/{self.version}"

        return f"https://api.mod.io/{self.version}"

    def __repr__(self):
        return f"<Connection retry_after={self.retry_after}>"

    async def close(self):
        """Close session"""
        await self.async_session.close()

    async def start(self):
        """Start session"""
        self.async_session = aiohttp.ClientSession()

    def enforce_ratelimit(self):
        if self.retry_after > 0:
            logging.info("Ratelimited, sleeping for %s seconds", self.retry_after)
            time.sleep(self.retry_after)

    async def async_enforce_ratelimit(self):
        if self.retry_after > 0:
            logging.info("Ratelimited, sleeping for %s seconds", self.retry_after)
            await asyncio.sleep(self.retry_after)

    def _error_check(self, resp, request_json):
        """Updates the rate-limit attributes and check validity of the request."""
        self.retry_after = resp.headers.get("retry-after", 0)
        code = getattr(resp, "status_code", getattr(resp, "status", None))

        if code == 204:
            return resp

        if "error" in request_json:
            error_code = request_json["error"]["code"]
            msg = request_json["error"]["message"]
            ref = request_json["error"]["error_ref"]
            errors = request_json["error"].get("errors", {})

            raise modioException(msg, error_code, ref, errors)

        return request_json

    def _define_headers(self, h_type):
        if h_type == 0:
            # regular O auth 2 header when submitting data
            headers = {
                "Authorization": "Bearer " + self.access_token,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Accept-Language": self.lang,
            }
        elif h_type == 1:
            # o auth 2 header for submitting multipart/data, had to remove Content-Type
            # because it is already added by the requests lib when defining a files parameter
            headers = {
                "Authorization": "Bearer " + self.access_token,
                "Accept": "application/json",
                "Accept-Language": self.lang,
            }
        elif h_type == 2:
            # header to use when making calls using the api key, the key itself is added in
            # the parameters in the methods below
            headers = {
                "Accept": "application/json",
                "Accept-Language": self.lang,
                "Content-Type": "application/x-www-form-urlencoded",
            }

        return headers

    def _post(self, resp):
        try:
            resp_json = resp.json()
        except requests.JSONDecodeError:
            resp_json = {}

        try: 
            data = self._error_check(resp, resp_json)
        except modioException as e:
            if e.code == 429:
                self.enforce_ratelimit()
            
            raise e

        return data

    def get_request(self, url, *, h_type=0, **fields):
        filters = fields.pop("filters", None)
        filters = (filters or Filter()).get_dict()

        extra = {**fields, **filters}

        if not self.access_token:
            extra["api_key"] = self.api_key
            h_type = 2

        resp = self.session.get(self._base_path + url, headers=self._define_headers(h_type), params=extra)
        return self._post(resp)

    def post_request(self, url, *, h_type=0, **fields):
        resp = self.session.post(self._base_path + url, headers=self._define_headers(h_type), **fields)
        return self._post(resp)

    def put_request(self, url, *, h_type=0, **fields):
        resp = self.session.put(self._base_path + url, headers=self._define_headers(h_type), **fields)
        return self._post(resp)

    def delete_request(self, url, *, h_type=0, **fields):
        resp = self.session.delete(self._base_path + url, headers=self._define_headers(h_type), **fields)
        return self._post(resp)

    async def _async_post(self, resp):
        try:
            resp_json = await resp.json()
        except aiohttp.ContentTypeError:
            resp_json = {}


        try: 
            data = self._error_check(resp, resp_json)
        except modioException as e:
            if e.code == 429:
                await self.async_enforce_ratelimit()
            
            raise e

        return data

    async def async_get_request(self, url, *, h_type=0, **fields):
        filters = fields.pop("filters", None)
        filters = (filters or Filter()).get_dict()

        extra = {**fields, **filters}

        if not self.access_token:
            extra["api_key"] = self.api_key
            h_type = 2

        async with self.async_session.get(
            self._base_path + url, headers=self._define_headers(h_type), params=extra
        ) as resp:
            return await self._async_post(resp)

    async def async_post_request(self, url, *, h_type=0, **fields):
        files = fields.pop("files", {})
        data = fields.pop("data", {})

        form = aiohttp.FormData()
        for key, value in data.items():
            if value is None:
                continue

            form.add_field(key, str(value))

        for key, value in files.items():
            if value is None:
                continue

            if isinstance(value, tuple):
                form.add_field(key, value[1], filename=value[0], content_type="multipart/form-data")
            else:
                form.add_field(key, value, content_type="multipart/form-data")

        async with self.async_session.post(
            self._base_path + url, headers=self._define_headers(h_type), data=form
        ) as resp:
            return await self._async_post(resp)

    async def async_put_request(self, url, *, h_type=0, **fields):
        async with self.async_session.put(
            self._base_path + url, headers=self._define_headers(h_type), **fields
        ) as resp:
            return await self._async_post(resp)

    async def async_delete_request(self, url, *, h_type=0, **fields):
        async with self.async_session.delete(
            self._base_path + url, headers=self._define_headers(h_type), **fields
        ) as resp:
            return await self._async_post(resp)


class Client:
    """Represents an authenticated client to make requests to the mod.io API with. If you desire
    to make aysnc requests you must call :ref:`Client.start` before making any async request.

    Parameters
    -----------
    api_key : Optional[str]
        The api key that will be used to authenticate the bot while it makes most of
        its GET requests. This can be generated on the mod.io website. Optional if an access
        token is supplied.
    access_token : Optional[str]
        The OAuth 2 token that will be used to make more complex GET requests and to make
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
    retry_after : int
        Number of seconds until the rate limits are reset for this API Key/access token.
        Is 0 until the rate_remain is 0 and becomes 0 again once the rate limit is reset.
    """

    def __init__(self, *, api_key=None, access_token=None, lang="en", version="v1", test=False):
        self.lang = lang
        self.version = version
        self.test = test
        self.connection = Connection(
            test=test, api_key=api_key, access_token=access_token, version=version, lang=lang
        )

    def __repr__(self):
        return f"< Client version={self.version} test={self.test} >"

    @property
    def rate_limit(self):
        return self.connection.rate_limit

    @property
    def rate_remain(self):
        return self.connection.rate_remain

    @property
    def retry_after(self):
        return self.connection.retry_after

    async def close(self):
        """|async| This function is used to clean up the client in order to close the application that it uses gracefully.
        At the moment it is only used to close the client's Session.

        |coro|
        """
        await self.connection.close()

    async def start(self):
        """|async| This function is used to start up the async part of the client. This is required to avoid sync users
        from having to clean up stuff.

        |coro|
        """
        await self.connection.start()

    def get_game(self, game_id: int) -> Game:
        """Queries the mod.io API for the given game ID and if found returns it as a
        Game instance. If not found raises NotFound.

        |coro|

        Parameters
        -----------
        game_id : int
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
        game_json = self.connection.get_request(f"/games/{game_id}")
        return Game(connection=self.connection, **game_json)

    async def async_get_game(self, game_id: int) -> Game:
        game_json = await self.connection.async_get_request(f"/games/{game_id}")
        return Game(connection=self.connection, **game_json)

    def get_games(self, *, filters: Filter = None) -> Returned[Game]:
        """Gets all the games available on mod.io. Returns a
        named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filters : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Game], Pagination]
            The results and pagination tuple from this request
        """
        game_json = self.connection.get_request("/games", filters=filters)
        return Returned(
            [Game(connection=self.connection, **game) for game in game_json["data"]], Pagination(**game_json)
        )

    async def async_get_games(self, *, filters: Filter = None) -> Returned[Game]:
        game_json = await self.connection.async_get_request("/games", filters=filters)
        return Returned(
            [Game(connection=self.connection, **game) for game in game_json["data"]], Pagination(**game_json)
        )

    def get_my_user(self) -> User:
        """Gets the authenticated user's details (aka the user who created the API key/access token)

        |coro|

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        -------
        User
            The authenticated user

        """
        me_json = self.connection.get_request("/me")
        return User(connection=self.connection, **me_json)

    async def async_get_my_user(self) -> User:
        me_json = await self.connection.async_get_request("/me")
        return User(connection=self.connection, **me_json)

    def get_my_subs(self, *, filters: Filter = None) -> Returned[Mod]:
        """Gets all the mods the authenticated user is subscribed to. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[Mod], Pagination]
            The results and pagination tuple from this request
        """
        mod_json = self.connection.get_request("/me/subscribed", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    async def async_get_my_subs(self, *, filters: Filter = None) -> Returned[Mod]:
        mod_json = await self.connection.async_get_request("/me/subscribed", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    def get_my_events(self, *, filters: Filter = None) -> Returned[Event]:
        """Get events that have been fired specifically for the authenticated user. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Returns
        --------
        Returned[List[Event], Pagination]
            The results and pagination tuple from this request
        """
        events_json = self.connection.get_request("/me/events", filters=filters)
        return Returned([Event(**event) for event in events_json["data"]], Pagination(**events_json))

    async def async_get_my_events(self, *, filters: Filter = None) -> Returned[Event]:
        events_json = await self.connection.async_get_request("/me/events", filters=filters)
        return Returned([Event(**event) for event in events_json["data"]], Pagination(**events_json))

    def get_my_games(self, filters: Filter = None) -> Returned[Game]:
        """Get all the games the authenticated user added or is a team member of. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[Game], Pagination]
            The results and pagination tuple from this request
        """
        game_json = self.connection.get_request("/me/games", filters=filters)
        return Returned(
            [Game(connection=self.connection, **game) for game in game_json["data"]], Pagination(**game_json)
        )

    async def async_get_my_games(self, filters: Filter = None) -> Returned[Game]:
        game_json = await self.connection.async_get_request("/me/games", filters=filters)
        return Returned(
            [Game(connection=self.connection, **game) for game in game_json["data"]], Pagination(**game_json)
        )

    def get_my_mods(self, *, filters: Filter = None) -> Returned[Mod]:
        """Get all the mods the authenticated user added or is a team member of. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[Mod], Pagination]
            The results and pagination tuple from this request
        """
        mod_json = self.connection.get_request("/me/mods", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    async def async_get_my_mods(self, *, filters: Filter = None) -> Returned[Mod]:
        mod_json = await self.connection.async_get_request("/me/mods", filters=filters)
        return Returned(
            [Mod(connection=self.connection, **mod) for mod in mod_json["data"]], Pagination(**mod_json)
        )

    def get_my_modfiles(self, *, filters: Filter = None) -> Returned[ModFile]:
        """Get all the mods the authenticated user uploaded. The returned modfile objects cannot be
        edited or deleted and do not have a `game_id` attribute. Returns
        a named tuple with parameters results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[ModFile], Pagination]
            The results and pagination tuple from this request
        """
        files_json = self.connection.get_request("/me/files", filters=filters)
        return Returned(
            [ModFile(**file, connection=self.connection) for file in files_json["data"]],
            Pagination(**files_json),
        )

    async def async_get_my_modfiles(self, *, filters: Filter = None) -> Returned[ModFile]:
        files_json = await self.connection.async_get_request("/me/files", filters=filters)
        return Returned(
            [ModFile(**file, connection=self.connection) for file in files_json["data"]],
            Pagination(**files_json),
        )

    def get_my_ratings(self, *, filters: Filter = None) -> Returned[Rating]:
        """Get all the ratings the authentitated user has submitted. Returns a named
        with parameter results and pagination. |filterable|

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[Rating], Pagination]
            The results and pagination tuple from this request
        """

        ratings = self.connection.get_request("/me/ratings", filters=filters)
        return Returned(
            [Rating(**rating, connection=self.connection) for rating in ratings["data"]],
            Pagination(**ratings),
        )

    async def async_get_my_ratings(self, *, filters: Filter = None) -> Returned[Rating]:
        ratings = await self.connection.async_get_request("/me/ratings", filters=filters)
        return Returned(
            [Rating(**rating, connection=self.connection) for rating in ratings["data"]],
            Pagination(**ratings),
        )

    def get_my_mutes(self, *, filters: Filter = None) -> Returned[User]:
        """Get all users muted by this user

        |coro|

        Parameters
        -----------
        filter : Optional[Filter]
            A instance of Filter to be used for filtering, paginating and sorting
            results

        Raises
        -------
        Forbidden
            The access token is invalid/missing

        Returns
        --------
        Returned[List[User], Pagination]
            The results and pagination tuple from this request
        """

        users = self.connection.get_request("/me/users/muted", filters=filters)
        return Returned(
            [User(**user, connection=self.connection) for user in users["data"]], Pagination(**users)
        )

    async def async_get_my_mutes(self, *, filters: Filter = None) -> Returned[User]:
        users = await self.connection.async_get_request("/me/users/muted", filters=filters)
        return Returned(
            [User(**user, connection=self.connection) for user in users["data"]], Pagination(**users)
        )

    def email_request(self, email: str):  # pragma: no cover
        """Posts an email request for an OAuth2 token. A code will be sent to the given email address
        which can then be entered into :func:`email_exchange`.

        |coro|

        Parameters
        ----------
        email : str
            A valid email to which the 5-digit code will be sent

        """

        resp = self.connection.post_request(
            "/oauth/emailrequest", params={"email": email, "api_key": self.connection.api_key}, h_type=2
        )
        return Message(**resp)

    async def async_email_request(self, email: str):  # pragma: no cover
        resp = await self.connection.async_post_request(
            "/oauth/emailrequest", params={"email": email, "api_key": self.connection.api_key}, h_type=2
        )
        return Message(**resp)

    def email_exchange(self, code: int, *, date_expires: datetime.datetime = None) -> str:  # pragma: no cover
        """Exchanges the given 5-digit code for an OAuth2 token.

        |coro|

        Parameters
        ----------
        code : int
            A 5-digit code received by email less than 15 minutes ago
        date_expires : Optional[datetime.datetime]
            Datetime of when the token will expire. By default this
            is a year, value cannot be greater than a year.

        Raises
        -------
        Unauthorized
            Invalid security code
        ValueError
            Security code was not 5 digits long

        Returns
        --------
        str
            The access code.
        """

        if len(code) != 5:
            raise ValueError("Security code must be 5 digits")

        params = {"security_code": code, "api_key": self.connection.api_key}
        if date_expires is not None:
            params["date_expires"] = date_expires.timestamp()

        resp = self.connection.post_request(
            "/oauth/emailexchange",
            params=params,
            h_type=2,
        )

        return resp["access_token"]

    async def async_email_exchange(
        self, code: int, *, date_expires: datetime.datetime = None
    ) -> str:  # pragma: no cover
        if len(code) != 5:
            raise ValueError("Security code must be 5 digits")

        params = {"security_code": code, "api_key": self.connection.api_key}
        if date_expires is not None:
            params["date_expires"] = date_expires.timestamp()

        resp = await self.connection.async_post_request(
            "/oauth/emailexchange",
            params=params,
            h_type=2,
        )

        return resp["access_token"]
