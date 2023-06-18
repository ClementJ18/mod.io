import unittest

import pytest
import modio
import random

from modio.enums import Community, EventType, TargetPlatform
from modio.errors import modioException
from modio.utils import _convert_date

try:
    from .config import access_token, game_id, mod_id
except ModuleNotFoundError:
    import os

    access_token = os.environ["ACCESS_TOKEN"]
    game_id = os.environ["GAME_ID"]
    mod_id = os.environ["MOD_ID"]

from .utils import run, use_test_env

event_params = {
    "id": 13,
    "mod_id": 13,
    "user_id": 13,
    "date_added": 1499846132,
    "event_type": "MODFILE_CHANGED",
}


class TestEvent(unittest.TestCase):
    def test_type(self):
        event = modio.entities.Event(**event_params)

        assert event.type is modio.EventType.file_changed

        event_params["event_type"] = "USER_TEAM_JOIN"
        event = modio.entities.Event(**event_params)

        assert event.type is modio.EventType.team_join


class TestComment(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)

    def tearDown(self):
        run(self.client.close())

    def test_comment(self):
        comments = self.mod.get_comments().results
        if not comments:
            return
        
        comment = comments[0]

        comment.edit("test edit")

        if comment.karma < 2:
            comment.add_positive_karma()
            comment.add_negative_karma()
        else:
            comment.add_negative_karma()
            comment.add_positive_karma()

        comment.delete()

    def test_async_comment(self):
        comments = run(self.mod.async_get_comments()).results
        if not comments:
            return
        
        comment = comments[0]

        run(comment.async_edit("test edit async"))

        if comment.karma < 2:
            run(comment.async_add_positive_karma())
            run(comment.async_add_negative_karma())
        else:
            run(comment.async_add_negative_karma())
            run(comment.async_add_positive_karma())

        run(comment.async_delete())


class TestModFile(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
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
        self.mod.get_files().results[-1].delete()

    def test_async_delete(self):
        run(self.mod.get_files().results[-1].async_delete())


class TestRating(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
        run(self.client.start())

        self.mod = self.client.get_my_mods(filters=modio.Filter().equals(id=mod_id)).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_rating(self):
        self.mod.add_negative_rating()

        rating = self.client.get_my_ratings().results[0]
        rating.add_positive_rating()
        rating.add_negative_rating()
        rating.delete()

    def test_async_rating(self):
        self.mod.add_negative_rating()

        rating = self.client.get_my_ratings().results[0]
        run(rating.async_add_positive_rating())
        run(rating.async_add_negative_rating())
        run(rating.async_delete())


class TestStats(unittest.TestCase):
    def test_stats(self):
        client = modio.Client(access_token=access_token, test=use_test_env)
        run(client.start())

        game = client.get_game(game_id)
        stat = game.get_mods_stats().results[0]
        stat.is_stale()
        run(client.close())


class TestTeamMember(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)
        self.member = self.mod.get_team(filters=modio.Filter().equals(id=10610)).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_mute(self):
        with pytest.raises(modioException):
            self.member.mute()
    
        self.member.unmute()

    def test_async_mute(self):
        with pytest.raises(modioException):
            run(self.member.async_mute())
    
        run(self.member.async_unmute())


class TestFilter(unittest.TestCase):
    def test_filter_event(self):
        filters = modio.Filter().equals(event_type=EventType.comment_added)
        event_params["event_type"] = filters.__dict__["event_type"]
        event = modio.entities.Event(**event_params)

        assert event.type is EventType.comment_added

        filters = modio.Filter().equals(event_type=EventType.team_join)
        event_params["event_type"] = filters.__dict__["event_type"]
        event = modio.entities.Event(**event_params)

        assert event.type is EventType.team_join

    def test_filter_datetime(self):
        filters = modio.Filter().equals(tico=_convert_date(event_params["date_added"]))

        assert filters.__dict__["tico"] == event_params["date_added"]

    def test_filter_enums(self):
        filters = modio.Filter().equals(tico=TargetPlatform.android)

        assert filters.__dict__["tico"] == TargetPlatform.android.value

    def test_filter_methods(self):
        filters = modio.Filter()

        filters.text("tico")
        filters.equals(tico="tico")
        filters.not_equals(tico="tico")
        filters.like(tico="tico")
        filters.not_like(tico="tico")
        filters.values_in(tico=["tico"])
        filters.values_not_in(tico=["tico"])
        filters.max(tico=3)
        filters.min(tico=5)
        filters.smaller_than(tico=2)
        filters.greater_than(tico=3)
        filters.bitwise(tico=Community.disabled | Community.guides_news)

        filters.sort("tico", reverse=True)
        filters.limit(56)
        filters.offset(49)

        client = modio.Client(access_token=access_token, test=use_test_env)
        client.get_my_mods(filters=filters)


class TestPagination(unittest.TestCase):
    def test_pagination(self):
        client = modio.Client(access_token=access_token, test=use_test_env)
        mods = client.get_my_mods()
        pagination = mods.pagination

        pagination.max()
        pagination.min()
        pagination.next()
        pagination.previous()
        pagination.page()


class TestObject(unittest.TestCase):
    def test_instantiate(self):
        fields = {"id": 1499, "tico": "test", "maturity_option": "bork"}

        obj = modio.Object(**fields)
        assert fields == obj.__dict__
