import unittest
import async_modio
import random

from .config import access_token
from .utils import run

class TestEvent(unittest.TestCase):
    def test_type(self):
        event = async_modio.objects.Event(**{
            "id": 13,
            "mod_id": 13,
            "user_id": 13,
            "date_added": 1499846132,
            "event_type": "MODFILE_CHANGED"
        })

        self.assertIsInstance(event.type, async_modio.EventType)

class TestComment(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.mod = run(self.game.get_mod(1251))

    def tearDown(self):
        run(self.client.close())

    def test_delete(self):
        run(run(self.mod.get_comments()).results[0].delete())

class TestModFile(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.mod = run(self.game.get_mod(1251))
        self.file = run(self.mod.get_files()).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_get_owner(self):
        run(self.file.get_owner())

    def test_edit(self):
        version = f"0.{random.randint(1, 54564)}.2"
        changelog = "New changes"
        active = True

        run(self.file.edit(version=version, changelog=changelog, active=active))

    def test_url_is_expired(self):
        self.assertFalse(self.file.url_is_expired())

class TestRating(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.rating = run(self.client.get_my_ratings()).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_add_positive_rating(self):
        run(self.rating.add_positive_rating())

    def test_add_negative_rating(self):
        run(self.rating.add_negative_rating())

    # def test_delete(self):
    #     self.rating.delete()

class TestStats(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.stat = run(self.game.get_stats()).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_is_stale(self):
        self.assertFalse(self.stat.is_stale())

class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.user = run(self.client.get_my_user())

    def tearDown(self):
        run(self.client.close())

    def test_report(self):
        run(self.user.report("pywrappertestreport", "pywrappertestreportsummary",  async_modio.Report.generic))

class TestTeamMember(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.mod = run(self.game.get_mod(1251))
        self.member = run(self.mod.get_team(filter=async_modio.Filter().text("TestNecro"))).results[0]

    def tearDown(self):
        run(self.client.close())

    def test_edit(self):
        run(self.member.edit(level=async_modio.Level.moderator))

    def test_delete(self):
        run(self.member.delete())

class TestFilter(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)

    def tearDown(self):
        run(self.client.close())

class TestPagination(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)

    def tearDown(self):
        run(self.client.close())

class TestObject(unittest.TestCase):
    def test_instantiate(self):
        fields = {
            "id": 1499,
            "tico": "test",
            "maturity_option": "bork"
        }

        obj = async_modio.Object(**fields)
        self.assertEqual(fields, obj.__dict__)
