import unittest
import modio
import random

try:
    from .config import access_token, game_id
except ModuleNotFoundError:
    import os

    access_token = os.environ["ACCESS_TOKEN"]
    game_id = os.environ["GAME_ID"]

from .utils import run, use_test_env


class TestGame(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.frozen_copy = self.client.get_game(game_id)

    def tearDown(self):
        run(self.client.close())

    def test_gets(self):
        mods = self.game.get_mods().results

        if mods:
            self.game.get_mod(mods[0].id)

        self.game.get_mod_events()
        self.game.get_tag_options()
        self.game.get_stats()
        self.game.get_mods_stats()

        self.game.get_owner()

    def test_add_media(self):
        logo = "tests/media/logo.png"
        header = "tests/media/header.png"
        icon = "tests/media/icon.png"

        self.game.add_media(logo=logo, header=header, icon=icon)

    def test_tag_options(self):
        self.game.add_tag_options(
            "pywrappertest",
            tags=["this", "is", "a", "test"],
            tag_type=random.choice(("dropdown", "checkboxes")),
            hidden=random.choice((False, True)),
        )

        self.game.delete_tag_options("pywrappertest", tags=["this", "test"])
        self.game.delete_tag_options("pywrappertest")

    # def test_report(self):
    #     self.game.report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic)

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
            logo="tests/media/logo.png",
        )

        newmod.add_tags("modification", "345")

        self.game.add_mod(newmod)

        newmod.name = "ToDeleteMod"
        self.game.add_mod(newmod)

    def test_async_gets(self):
        mods = run(self.game.async_get_mods()).results

        if mods:
            run(self.game.async_get_mod(mods[0].id))

        run(self.game.async_get_mod_events())
        run(self.game.async_get_tag_options())
        run(self.game.async_get_stats())
        run(self.game.async_get_mods_stats())

        run(self.game.async_get_owner())

    def test_async_add_media(self):
        logo = "tests/media/logo.png"
        header = "tests/media/header.png"
        icon = "tests/media/icon.png"

        run(self.game.async_add_media(logo=logo, header=header, icon=icon))

    def test_async_tag_options(self):
        run(
            self.game.async_add_tag_options(
                "pywrappertest",
                tags=["this", "is", "a", "test"],
                tag_type=random.choice(("dropdown", "checkboxes")),
                hidden=random.choice((False, True)),
            )
        )

        run(self.game.async_delete_tag_options("pywrappertest", tags=["this", "test"]))
        run(self.game.async_delete_tag_options("pywrappertest"))

    # def test_async_report(self):
    #     run(self.game.async_report("pywrappertestreport", "pywrappertestreportsummary", modio.Report.generic))

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
            logo="tests/media/logo.png",
        )

        newmod.add_tags("modification", "345")

        run(self.game.async_add_mod(newmod))

        newmod.name = "ToDeleteMod"
        run(self.game.async_add_mod(newmod))
