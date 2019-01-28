import unittest
import modio

from .config import user_api_key, game_api_key, access_token

class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_oauth_access(self):
        client = modio.Client(auth=access_token, test=True)
        
        client.get_my_user()
        client.get_my_subs()
        client.get_my_events()
        client.get_games()
        client.get_my_mods()
        client.get_my_modfiles()
        client.get_my_ratings()

    def test_api_token(self):
        client = modio.Client(api_key=game_api_key, test=True)
        games = client.get_games()
        client.get_game(games.results[0].id)

        client = modio.Client(api_key=user_api_key, test=True)
        users = client.get_users()
        # client.get_user(users.results[0].id)
        
