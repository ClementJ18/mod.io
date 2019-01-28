import unittest
import async_modio
import random

from .config import access_token
from .utils import run

class TestGame(unittest.TestCase):
    def setUp(self):
        self.client = async_modio.Client(auth=access_token, test=True)
        self.game = run(self.client.get_game(180))
        self.frozen_copy = run(self.client.get_game(180)) 

    def tearDown(self):
        run(self.client.close())

    def test_gets(self):
        mods = run(self.game.get_mods())
        run(self.game.get_mod(mods.results[0].id))

        run(self.game.get_mod_events())
        run(self.game.get_tag_options())
        run(self.game.get_stats())

        run(self.game.get_owner())

    def test_edit(self):
        name = f"PyWrapper TestGame {random.randint(1, 34534)}"
        community = random.choice(list(async_modio.Community))
        maturity = random.choice(list(async_modio.MaturityOptions))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "community": community, "maturity_options": maturity, "name_id": name_id}

        run(self.game.edit(**fields))
        fields["maturity_options"] = maturity.value
        new_fields = {"name": self.game.name, "community": self.game.community, "maturity_options": self.game.maturity_options, "name_id": self.game.name_id}

        self.assertEqual(fields, new_fields)

    def test_add_media(self):
        logo = 'test/media/logo.png'
        header = 'test/media/header.png'
        icon = 'test/media/icon.png'

        run(self.game.add_media(logo=logo, header=header, icon=icon))

    def test_add_tag_options(self):
        run(self.game.add_tag_options(
            "pywrappertest", 
            tags=["this", "is", "a", "test"], 
            type=random.choice(("dropdown", "checkboxes")),
            hidden=random.choice((False, True))
        ))

    def test_report(self):
        run(self.game.report("pywrappertestreport", "pywrappertestreportsummary",  async_modio.Report.generic))

    def test_add_mod(self):
        newmod = async_modio.NewMod(
            name=f"pywrappertestnewmod{random.randint(1, 700000)}",
            summary = "pywrappertestnewmodsummary",
            description=f"pywrappertestnewmoddescription{'ha' * 50}",
            homepage="http://edain.wikia.com/",
            metadata_blob="yes,yes,yes,yes",
            stock=random.randint(0, 700000),
            visible=async_modio.Visibility.hidden,
            maturity=async_modio.Maturity.drugs | async_modio.Maturity.explicit,
            logo="test/media/logo.png"
        )

        newmod.add_tags("modification", "345")

        run(self.game.add_mod(newmod))

        newmod.name = "ToDeleteMod"
        run(self.game.add_mod(newmod))

    def test_delete_tag_options(self):
        run(self.game.delete_tag_options("pywrappertest", tags=["this", "test"]))
        run(self.game.delete_tag_options("pywrappertest"))

