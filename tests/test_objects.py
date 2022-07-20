import unittest
import modio
import random

try:
    from .config import access_token, game_id, mod_id
except ModuleNotFoundError:
    import os

    access_token = os.environ["ACCESS_TOKEN"]
    game_id = os.environ["GAME_ID"]
    mod_id = os.environ["MOD_ID"]

from .utils import run


class TestEvent(unittest.TestCase):
    def test_type(self):
        event = modio.entities.Event(
            **{
                "id": 13,
                "mod_id": 13,
                "user_id": 13,
                "date_added": 1499846132,
                "event_type": "MODFILE_CHANGED",
            }
        )

        assert isinstance(event.type, modio.EventType)


class TestComment(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.game = client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)

    def test_delete(self):
        self.mod.get_comments().results[0].delete()


class TestModFile(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.game = client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.file = self.mod.get_files().results[0]

    def test_get_owner(self):
        self.file.get_owner()

    def test_edit(self):
        version = f"0.{random.randint(1, 54564)}.2"
        changelog = "New changes"
        active = True

        self.file.edit(version=version, changelog=changelog, active=active)

    def test_async_get_owner(self):
        run(self.file.async_get_owner())

    def test_async_edit(self):
        version = f"0.{random.randint(1, 54564)}.2"
        changelog = "New changes"
        active = True

        run(self.file.async_edit(version=version, changelog=changelog, active=active))

    def test_url_is_expired(self):
        assert not self.file.url_is_expired()


class TestRating(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.rating = client.get_my_ratings().results[0]

    def test_add_positive_rating(self):
        self.rating.add_positive_rating()

    def test_add_negative_rating(self):
        self.rating.add_negative_rating()

    def test_async_add_positive_rating(self):
        run(self.rating.async_add_positive_rating())

    def test_async_add_negative_rating(self):
        run(self.rating.async_add_negative_rating())


class TestStats(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.game = client.get_game(game_id)
        self.stat = self.game.get_stats().results[0]

    def test_is_stale(self):
        assert not self.stat.is_stale()


class TestUser(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.user = client.get_my_user()

    # def test_report(self):
    #     self.user.report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic)

    # def test_async_report(self):
        # run(self.user.async_report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic))

    def test_mute(self):
        self.user.mute()
        self.user.unmute()

    def test_async_mute(self):
        run(self.user.async_mute())
        run(self.user.async_unmute())


class TestTeamMember(unittest.TestCase):
    def setUp(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        self.game = client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.member = self.mod.get_team(filters=modio.Filter().text("TestNecro")).results[0]

    def test_edit(self):
        self.member.edit(level=modio.Level.moderator)

    def test_delete(self):
        self.member.delete()

    def test_async_edit(self):
        run(self.member.async_edit(level=modio.Level.moderator))

    def test_async_delete(self):
        run(self.member.async_delete())


# class TestFilter(unittest.TestCase):
#     def setUp(self):
#         client = modio.Client(access_token=access_token, test=True)


# class TestPagination(unittest.TestCase):
#     def setUp(self):
#         client = modio.Client(access_token=access_token, test=True)


class TestObject(unittest.TestCase):
    def test_instantiate(self):
        fields = {"id": 1499, "tico": "test", "maturity_option": "bork"}

        obj = modio.Object(**fields)
        assert fields == obj.__dict__
