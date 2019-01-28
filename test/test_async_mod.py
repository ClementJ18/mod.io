import unittest
import async_modio
import random

from .config import access_token
from .utils import run

class TestMod(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.mod = run(self.game.get_mod(1251))

    def tearDown(self):
        run(self.client.close())

    def test_gets(self):
        files = run(self.mod.get_files()).results
        run(self.mod.get_file(files[0].id))

        run(self.mod.get_events())
        run(self.mod.get_tags())
        run(self.mod.get_metadata())
        run(self.mod.get_dependencies())
        run(self.mod.get_team())
        run(self.mod.get_comments())
        run(self.mod.get_stats())
        run(self.mod.get_owner())

    def test_add_file(self):
        new_file = async_modio.NewModFile(version="1.231", changelog="It works now", active=False)
        new_file.add_file('test/files/file.zip')

        run(self.mod.add_file(new_file))

    def test_edit(self):
        name = f"PyWrapper TestMod {random.randint(1, 34534)}"
        maturity = random.choice(list(async_modio.Maturity))
        visible = random.choice(list(async_modio.Visibility))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "maturity": maturity, "name_id": name_id}

        run(self.mod.edit(**fields))
        new_fields = {"name": self.mod.name, "maturity": self.mod.maturity, "name_id": self.mod.name_id}

        self.assertEqual(fields, new_fields)

    def test_add_media(self):
        logo = 'test/media/logo.png'
        image_1 = 'test/media/icon.png'
        image_2 = 'test/media/header.png'
        youtube = ["https://www.youtube.com/watch?v=Z3OLwDNn_Ps", "https://www.youtube.com/watch?v=THSMkcuMF0U", "https://www.youtube.com/watch?v=c5ITerV5dIg", "https://www.youtube.com/watch?v=stlHQNWAYbk"]
        sketchfab = ["https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26", "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a", "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3"]

        run(self.mod.add_media(logo=logo, images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab))

        images = 'test/media/images.zip'
        run(self.mod.add_media(images=images))

    def test_delete_media(self):
        image_1 = 'icon.png'
        image_2 = 'header.png'
        youtube = ["https://www.youtube.com/watch?v=Z3OLwDNn_Ps", "https://www.youtube.com/watch?v=THSMkcuMF0U", "https://www.youtube.com/watch?v=c5ITerV5dIg", "https://www.youtube.com/watch?v=stlHQNWAYbk"]
        sketchfab = ["https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26", "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a", "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3"]

        run(self.mod.delete_media(images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab))

    def test_subscribe(self):
        run(self.mod.subscribe())

    def test_unsubscribe(self):
        run(self.mod.unsubscribe())

    def test_add_tags(self):
        run(self.mod.add_tags('total convert', '345', 'what am i doign'))

    def test_delete_tags(self):
        run(self.mod.delete_tags('total convert', '345', 'what am i doign'))

    def test_add_positive_rating(self):
        run(self.mod.add_positive_rating())

    def test_add_negative_rating(self):
        run(self.mod.add_negative_rating())

    def test_add_metadata(self):
        run(self.mod.add_metadata(test=["mega_damage", "tork"], seven=['sortk']))

    def test_delete_metadata(self):
        run(self.mod.delete_metadata(test=["mega_damage", 'tork'], seven=['sortk']))

    def test_add_dependencies(self):
        mods = run(self.game.get_mods()).results
        obj = mods[:7]
        ids = [x.id for x in mods[8:9]]
        run(self.mod.add_dependencies([*obj, *ids]))

    def test_delete_dependencies(self):
        run(self.mod.delete_dependencies(list(run(self.mod.get_dependencies()).results.keys())))

    def test_add_team_member(self):
        run(self.mod.add_team_member("juliacj@cardiff.ac.uk", async_modio.Level.creator, position="Lord of Tests"))

    def test_report(self):
        run(self.mod.report("pywrappertestreport", "pywrappertestreportsummary",  async_modio.Report.generic))

    def test_delete(self):
        mod = run(self.game.get_mods(filter=async_modio.Filter().text("ToDeleteMod"))).results[0]
        run(mod.delete())
