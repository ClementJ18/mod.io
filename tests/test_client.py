import unittest

import pytest
import modio

try:
    from .config import game_api_key, access_token
except ModuleNotFoundError:
    import os

    game_api_key = os.environ["GAME_API_KEY"]
    access_token = os.environ["ACCESS_TOKEN"]

from .utils import run


class TestClient(unittest.TestCase):
    def test_paths(self):
        client = modio.Client(api_key="fake key", test=True)
        # pylint: disable=W0212
        assert "test" in client.connection._base_path

        client.test = False
        # pylint: disable=W0212
        assert "test" not in client.connection._base_path

    def test_oauth_access(self):
        client = modio.Client(access_token=access_token, test=True)

        client.get_my_user()
        client.get_my_subs()
        client.get_my_events()
        client.get_my_games()
        client.get_my_mods()
        client.get_my_modfiles()
        client.get_my_ratings()
        client.get_my_mutes()

    def test_api_token(self):
        client = modio.Client(api_key=game_api_key, test=True)
        games = client.get_games()

        if games:
            client.get_game(games.results[0].id)

    def test_async_oauth_access(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        run(client.async_get_my_user())
        run(client.async_get_my_subs())
        run(client.async_get_my_events())
        run(client.async_get_my_games())
        run(client.async_get_my_mods())
        run(client.async_get_my_modfiles())
        run(client.async_get_my_ratings())
        run(client.async_get_my_mutes())

        run(client.close())

    def test_async_api_token(self):
        client = modio.Client(api_key=game_api_key, test=True)
        with pytest.raises(AttributeError):
            run(client.async_get_games())

        run(client.start())

        games = run(client.async_get_games())

        if games:
            run(client.async_get_game(games.results[0].id))

        run(client.close())
