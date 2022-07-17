import unittest
import modio
import random

try:
    from .config import access_token
except ModuleNotFoundError:
    import os

    access_token = os.environ["ACCESS_TOKEN"]

from .utils import run


class TestGame(unittest.TestCase):
    def setUp(self):
        client = modio.Client(auth=access_token, test=True)
        self.game = client.get_game(180)
        self.frozen_copy = client.get_game(180)

    def test_gets(self):
        mods = self.game.get_mods()
        self.game.get_mod(mods.results[0].id)

        self.game.get_mod_events()
        self.game.get_tag_options()
        self.game.get_stats()

        self.game.get_owner()

    def test_edit(self):
        name = f"PyWrapper TestGame {random.randint(1, 34534)}"
        community = random.choice(list(modio.Community))
        maturity = random.choice(list(modio.MaturityOptions))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "community": community, "maturity_options": maturity, "name_id": name_id}

        self.game.edit(**fields)
        fields["maturity_options"] = maturity.value
        new_fields = {
            "name": self.game.name,
            "community": self.game.community,
            "maturity_options": self.game.maturity_options,
            "name_id": self.game.name_id,
        }

        self.assertEqual(fields, new_fields)

    def test_add_media(self):
        logo = "test/media/logo.png"
        header = "test/media/header.png"
        icon = "test/media/icon.png"

        self.game.add_media(logo=logo, header=header, icon=icon)

    def test_add_tag_options(self):
        self.game.add_tag_options(
            "pywrappertest",
            tags=["this", "is", "a", "test"],
            tag_type=random.choice(("dropdown", "checkboxes")),
            hidden=random.choice((False, True)),
        )

    def test_report(self):
        self.game.report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic)

    def test_add_mod(self):
        newmod = modio.NewMod(
            name=f"pywrappertestnewmod{random.randint(1, 700000)}",
            summary="pywrappertestnewmodsummary",
            description=f"pywrappertestnewmoddescription{'ha' * 50}",
            homepage="http://edain.wikia.com/",
            metadata_blob="yes,yes,yes,yes",
            stock=random.randint(0, 700000),
            visible=modio.Visibility.hidden,
            maturity=modio.Maturity.drugs | modio.Maturity.explicit,
            logo="test/media/logo.png",
        )

        newmod.add_tags("modification", "345")

        self.game.add_mod(newmod)

        newmod.name = "ToDeleteMod"
        self.game.add_mod(newmod)

    def test_delete_tag_options(self):
        self.game.delete_tag_options("pywrappertest", tags=["this", "test"])
        self.game.delete_tag_options("pywrappertest")

    def test_async_gets(self):
        mods = run(self.game.async_get_mods())
        run(self.game.async_get_mod(mods.results[0].id))

        run(self.game.async_get_mod_events())
        run(self.game.async_get_tag_options())
        run(self.game.async_get_stats())

        run(self.game.async_get_owner())

    def test_async_edit(self):
        name = f"PyWrapper TestGame {random.randint(1, 34534)}"
        community = random.choice(list(modio.Community))
        maturity = random.choice(list(modio.MaturityOptions))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "community": community, "maturity_options": maturity, "name_id": name_id}

        run(self.game.async_edit(**fields))
        fields["maturity_options"] = maturity.value
        new_fields = {
            "name": self.game.name,
            "community": self.game.community,
            "maturity_options": self.game.maturity_options,
            "name_id": self.game.name_id,
        }

        self.assertEqual(fields, new_fields)

    def test_async_add_media(self):
        logo = "test/media/logo.png"
        header = "test/media/header.png"
        icon = "test/media/icon.png"

        run(self.game.async_add_media(logo=logo, header=header, icon=icon))

    def test_async_add_tag_options(self):
        run(
            self.game.async_add_tag_options(
                "pywrappertest",
                tags=["this", "is", "a", "test"],
                tag_type=random.choice(("dropdown", "checkboxes")),
                hidden=random.choice((False, True)),
            )
        )

    def test_async_report(self):
        run(self.game.async_report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic))

    def test_async_add_mod(self):
        newmod = modio.NewMod(
            name=f"pywrappertestnewmod{random.randint(1, 700000)}",
            summary="pywrappertestnewmodsummary",
            description=f"pywrappertestnewmoddescription{'ha' * 50}",
            homepage="http://edain.wikia.com/",
            metadata_blob="yes,yes,yes,yes",
            stock=random.randint(0, 700000),
            visible=modio.Visibility.hidden,
            maturity=modio.Maturity.drugs | modio.Maturity.explicit,
            logo="test/media/logo.png",
        )

        newmod.add_tags("modification", "345")

        run(self.game.async_add_mod(newmod))

        newmod.name = "ToDeleteMod"
        run(self.game.async_add_mod(newmod))

    def test_async_delete_tag_options(self):
        run(self.game.async_delete_tag_options("pywrappertest", tags=["this", "test"]))
        run(self.game.async_delete_tag_options("pywrappertest"))
