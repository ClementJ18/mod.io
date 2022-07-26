import unittest

import pytest
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
        params = {
            "id": 13,
            "mod_id": 13,
            "user_id": 13,
            "date_added": 1499846132,
            "event_type": "MODFILE_CHANGED",
        }

        event = modio.entities.Event(
            **params
        )

        assert event.type is modio.EventType.file_changed

        params["event_type"] = "USER_TEAM_JOIN"
        event = modio.entities.Event(
            **params
        )

        assert event.type is modio.EventType.team_join


class TestComment(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=True)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.comment = self.mod.get_comments().results[0]

    def tearDown(self):
        run(self.client.close())

    def test_edit(self):
        self.comment.edit("test edit")

    def test_async_edit(self):
        run(self.comment.async_edit("test edit async"))

    def test_karma(self):
        self.comment.add_positive_karma()
        self.comment.add_negative_karma()

    def test_async_karma(self):
        run(self.comment.async_add_positive_karma())
        run(self.comment.async_add_negative_karma())

    def test_delete(self):
        comments = self.mod.get_comments().results
        if comments:
            comments[0].delete()

    def test_async_delete(self):
        comments = run(self.mod.async_get_comments()).results
        if comments:
            run(comments[0].async_delete())


class TestModFile(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=True)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.file = self.mod.get_files().results[0]

    def tearDown(self):
        run(self.client.close())

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

    def test_edit_my_modfiles(self):
        file = self.client.get_my_modfiles().results[0]

        with pytest.raises(modio.modioException):
            file.edit()

        with pytest.raises(modio.modioException):
            run(file.async_edit())

        with pytest.raises(modio.modioException):
            file.delete()

        with pytest.raises(modio.modioException):
            run(file.async_delete())

    def test_delete(self):
        self.mod.get_files().results[0].delete()

    def test_async_delete(self):
        run(self.mod.get_files().results[0].async_delete())

class TestRating(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=True)
        run(self.client.start())

        self.rating = self.client.get_my_ratings().results[0]

    def tearDown(self):
        run(self.client.close())

    def test_add_positive_rating(self):
        self.rating.add_positive_rating()

    def test_add_negative_rating(self):
        self.rating.add_negative_rating()

    def test_async_add_positive_rating(self):
        run(self.rating.async_add_positive_rating())

    def test_async_add_negative_rating(self):
        run(self.rating.async_add_negative_rating())


class TestStats(unittest.TestCase):
    def test_stats(self):
        client = modio.Client(access_token=access_token, test=True)
        run(client.start())

        game = client.get_game(game_id)
        stat = game.get_mods_stats().results[0]
        stat.is_stale()
        run(client.close())


class TestTeamMember(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=True)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.member = self.mod.get_team(filters=modio.Filter().equals(id=10610)).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_mute(self):
        self.member.mute()
        self.member.unmute()

    def test_async_mute(self):
        run(self.member.async_mute())
        run(self.member.async_unmute())


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
