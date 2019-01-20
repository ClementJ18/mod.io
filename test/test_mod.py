import unittest
import modio
import random

from .test_config import access_token

class TestMod(unittest.TestCase):
    def setUp(self):
        client = modio.Client(auth=access_token, test=True)
        self.game = client.get_game(180)
        self.mod = self.game.get_mod(1251)

    def tearDown(self):
        pass

    def test_gets(self):
        files = self.mod.get_files().results
        self.mod.get_file(files[0].id)

        self.mod.get_events()
        self.mod.get_tags()
        self.mod.get_metadata()
        self.mod.get_dependencies()
        self.mod.get_team()
        self.mod.get_comments()
        self.mod.get_stats()
        self.mod.get_owner()

    def test_add_file(self):
        new_file = modio.NewModFile(version="1.231", changelog="It works now", active=False)
        new_file.add_file('test/files/file.zip')

        self.mod.add_file(new_file)

    def test_edit(self):
        name = f"PyWrapper TestMod {random.randint(1, 34534)}"
        maturity = random.choice(list(modio.Maturity))
        visible = random.choice(list(modio.Visibility))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "maturity": maturity, "name_id": name_id}

        self.mod.edit(**fields)
        new_fields = {"name": self.mod.name, "maturity": self.mod.maturity, "name_id": self.mod.name_id}

        self.assertEqual(fields, new_fields)

    def test_add_media(self):
        logo = 'test/media/logo.png'
        image_1 = 'test/media/icon.png'
        image_2 = 'test/media/header.png'
        youtube = ["https://www.youtube.com/watch?v=Z3OLwDNn_Ps", "https://www.youtube.com/watch?v=THSMkcuMF0U", "https://www.youtube.com/watch?v=c5ITerV5dIg", "https://www.youtube.com/watch?v=stlHQNWAYbk"]
        sketchfab = ["https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26", "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a", "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3"]

        self.mod.add_media(logo=logo, images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab)

        images = 'test/media/images.zip'
        self.mod.add_media(images=images)

    def test_delete_media(self):
        image_1 = 'icon.png'
        image_2 = 'header.png'
        youtube = ["https://www.youtube.com/watch?v=Z3OLwDNn_Ps", "https://www.youtube.com/watch?v=THSMkcuMF0U", "https://www.youtube.com/watch?v=c5ITerV5dIg", "https://www.youtube.com/watch?v=stlHQNWAYbk"]
        sketchfab = ["https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26", "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a", "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3"]

        self.mod.delete_media(images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab)

    def test_subscribe(self):
        self.mod.subscribe()

    def test_unsubscribe(self):
        self.mod.unsubscribe()

    def test_add_tags(self):
        self.mod.add_tags('total convert', '345', 'what am i doign')

    def test_delete_tags(self):
        self.mod.delete_tags('total convert', '345', 'what am i doign')

    def test_add_positive_rating(self):
        self.mod.add_positive_rating()

    def test_add_negative_rating(self):
        self.mod.add_negative_rating()

    def test_add_metadata(self):
        self.mod.add_metadata(test=["mega_damage", "tork"], seven=['sortk'])

    def test_delete_metadata(self):
        self.mod.delete_metadata(test=["mega_damage", 'tork'], seven=['sortk'])

    def test_add_dependencies(self):
        mods = self.game.get_mods().results
        obj = mods[:7]
        ids = [x.id for x in mods[8:9]]
        self.mod.add_dependencies([*obj, *ids])

    def test_delete_dependencies(self):
        self.mod.delete_dependencies(list(self.mod.get_dependencies().results.keys()))

    def test_add_team_member(self):
        self.mod.add_team_member("juliacj@cardiff.ac.uk", modio.Level.creator, position="Lord of Tests")

    def test_report(self):
        self.mod.report("pywrappertestreport", "pywrappertestreportsummary",  modio.Report.generic)

    def test_delete(self):
        mod = self.game.get_mods(filter=modio.Filter().text("ToDeleteMod")).results[0]
        mod.delete()
