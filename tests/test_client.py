import unittest
import modio

try:
    from .config import game_api_key, access_token
except ModuleNotFoundError:
    import os

    game_api_key = os.environ["GAME_API_KEY"]
    access_token = os.environ["ACCESS_TOKEN"]

from .utils import run


class TestClient(unittest.TestCase):
    def test_oauth_access(self):
        client = modio.Client(access_token=access_token, test=True)

        client.get_my_user()
        client.get_my_subs()
        client.get_my_events()
        client.get_my_games()
        client.get_my_mods()
        client.get_my_modfiles()
        client.get_my_ratings()

    def test_api_token(self):
        client = modio.Client(api_key=game_api_key, test=True)
        games = client.get_games()
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

        run(client.close())

    def test_async_api_token(self):
        client = modio.Client(api_key=game_api_key, test=True)
        run(client.start())

        games = run(client.async_get_games())
        run(client.async_get_game(games.results[0].id))
        run(client.close())
