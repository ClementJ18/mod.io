import time
import unittest

import pytest
import modio
import random

from modio.errors import modioException

try:
    from .config import access_token, game_id, mod_id
except ModuleNotFoundError:
    import os

    access_token = os.environ["ACCESS_TOKEN"]
    game_id = os.environ["GAME_ID"]
    mod_id = os.environ["MOD_ID"]

from .utils import run, use_test_env


class TestMod(unittest.TestCase):
    def setUp(self):
        self.client = modio.Client(access_token=access_token, test=use_test_env)
        run(self.client.start())

        self.game = self.client.get_game(game_id)
        self.mod = self.game.get_mod(mod_id)

    def tearDown(self):
        run(self.client.close())

    def test_gets(self):
        files = self.mod.get_files().results
        if files:
            self.mod.get_file(files[0].id)

        self.mod.get_events()
        self.mod.get_tags()
        self.mod.get_metadata()
        self.mod.get_dependencies()
        self.mod.get_team()
        self.mod.get_comments()
        self.mod.get_stats()
        self.mod.get_owner()

    def test_add_comment(self):
        time.sleep(3)
        c = self.mod.add_comment("This is a test comment")
        time.sleep(3)
        self.mod.add_comment("This is a test reply", reply=c)

    def test_add_file(self):
        new_file = modio.NewModFile(version="1.231", changelog="It works now", active=False)
        new_file.add_file("tests/files/file.zip")

        self.mod.add_file(new_file)

    def test_edit(self):
        name = f"PyWrapper TestMod {random.randint(1, 34534)}"
        maturity = random.choice(list(modio.Maturity))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "maturity": maturity, "name_id": name_id}

        self.mod.edit(**fields)

    def test_add_media(self):
        logo = "tests/media/logo.png"
        image_1 = "tests/media/icon.png"
        image_2 = "tests/media/header.png"
        youtube = [
            "https://www.youtube.com/watch?v=Z3OLwDNn_Ps",
            "https://www.youtube.com/watch?v=THSMkcuMF0U",
            "https://www.youtube.com/watch?v=c5ITerV5dIg",
            "https://www.youtube.com/watch?v=stlHQNWAYbk",
        ]
        sketchfab = [
            "https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26",
            "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a",
            "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3",
        ]

        self.mod.add_media(logo=logo, images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab)

        images = "tests/media/images.zip"
        self.mod.add_media(images=images)

    def test_delete_media(self):
        image_1 = "icon.png"
        image_2 = "header.png"
        youtube = [
            "https://www.youtube.com/watch?v=Z3OLwDNn_Ps",
            "https://www.youtube.com/watch?v=THSMkcuMF0U",
            "https://www.youtube.com/watch?v=c5ITerV5dIg",
            "https://www.youtube.com/watch?v=stlHQNWAYbk",
        ]
        sketchfab = [
            "https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26",
            "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a",
            "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3",
        ]

        self.mod.delete_media(images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab)

    def test_subscribe(self):
        self.mod.subscribe()

    def test_unsubscribe(self):
        self.mod.unsubscribe()

    def test_add_tags(self):
        self.mod.add_tags("true")

    def test_delete_tags(self):
        self.mod.delete_tags("true")

    def test_add_rating(self):
        self.mod.add_negative_rating()
        self.mod.add_positive_rating()

    def test_add_metadata(self):
        self.mod.add_metadata(test=["mega_damage", "tork"], seven=["sortk"])

    def test_delete_metadata(self):
        self.mod.delete_metadata(test=["mega_damage", "tork"], seven=["sortk"])

    def test_add_dependencies(self):
        mod = self.game.get_mod(3096610)
        self.mod.add_dependencies([mod.id])

    def test_delete_dependencies(self):
        dependencies = list(self.mod.get_dependencies().results.keys())

        with pytest.raises(modioException):
            self.mod.delete_dependencies([])

        if dependencies:
            self.mod.delete_dependencies(dependencies)

    def test_add_team_member(self):
        try:
            self.mod.add_team_member("juliacj@cardiff.ac.uk", modio.Level.creator, position="Lord of Tests")
        except modioException as e:
            if e.code != 403:
                raise e from e

    def test_delete(self):
        mod = self.client.get_my_mods(filters=modio.Filter().text("ToDeleteMod")).results

        if mod:
            mod[0].delete()

    def test_async_gets(self):
        files = run(self.mod.async_get_files()).results
        if files:
            run(self.mod.async_get_file(files[0].id))

        run(self.mod.async_get_events())
        run(self.mod.async_get_tags())
        run(self.mod.async_get_metadata())
        run(self.mod.async_get_dependencies())
        run(self.mod.async_get_team())
        run(self.mod.async_get_comments())
        run(self.mod.async_get_stats())
        run(self.mod.async_get_owner())

    def test_async_add_comment(self):
        time.sleep(3)
        c = run(self.mod.async_add_comment("This is a test async comment"))
        time.sleep(3)
        run(self.mod.async_add_comment("This is a test async reply", reply=c))

    def test_async_add_file(self):
        new_file = modio.NewModFile(version="1.231", changelog="It works now", active=False)
        new_file.add_file("tests/files/file.zip")

        run(self.mod.async_add_file(new_file))

    def test_async_edit(self):
        name = f"PyWrapper TestMod {random.randint(1, 34534)}"
        maturity = random.choice(list(modio.Maturity))
        name_id = name.lower().replace(" ", "-")[:80]
        fields = {"name": name, "maturity": maturity, "name_id": name_id}

        run(self.mod.async_edit(**fields))

    def test_async_add_media(self):
        logo = "tests/media/logo.png"
        image_1 = "tests/media/icon.png"
        image_2 = "tests/media/header.png"
        youtube = [
            "https://www.youtube.com/watch?v=Z3OLwDNn_Ps",
            "https://www.youtube.com/watch?v=THSMkcuMF0U",
            "https://www.youtube.com/watch?v=c5ITerV5dIg",
            "https://www.youtube.com/watch?v=stlHQNWAYbk",
        ]
        sketchfab = [
            "https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26",
            "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a",
            "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3",
        ]

        run(
            self.mod.async_add_media(
                logo=logo, images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab
            )
        )

        images = "tests/media/images.zip"
        run(self.mod.async_add_media(images=images))

    def test_async_delete_media(self):
        image_1 = "icon.png"
        image_2 = "header.png"
        youtube = [
            "https://www.youtube.com/watch?v=Z3OLwDNn_Ps",
            "https://www.youtube.com/watch?v=THSMkcuMF0U",
            "https://www.youtube.com/watch?v=c5ITerV5dIg",
            "https://www.youtube.com/watch?v=stlHQNWAYbk",
        ]
        sketchfab = [
            "https://sketchfab.com/models/d77426cd387c48e2a7a2c410f76b0c26",
            "https://sketchfab.com/models/3bba1fa0e50d48d3a4a52e97732c9c7a",
            "https://sketchfab.com/models/227a01a3d24b444e9605470b0b78c0e3",
        ]

        run(self.mod.async_delete_media(images=[image_1, image_2], youtube=youtube, sketchfab=sketchfab))

    def test_async_subscribe(self):
        run(self.mod.async_subscribe())

    def test_async_unsubscribe(self):
        run(self.mod.async_unsubscribe())

    def test_async_add_tags(self):
        run(self.mod.async_add_tags("true"))

    def test_async_delete_tags(self):
        run(self.mod.async_delete_tags("true"))

    def test_async_add_rating(self):
        run(self.mod.async_add_negative_rating())
        run(self.mod.async_add_positive_rating())

    def test_async_add_metadata(self):
        run(self.mod.async_add_metadata(test=["mega_damage", "tork"], seven=["sortk"]))

    def test_async_delete_metadata(self):
        run(self.mod.async_delete_metadata(test=["mega_damage", "tork"], seven=["sortk"]))

    def test_async_add_dependencies(self):
        mod = self.game.get_mod(3096610)
        run(self.mod.async_add_dependencies([mod.id]))

    def test_async_delete_dependencies(self):
        dependencies = list(run(self.mod.async_get_dependencies()).results.keys())

        with pytest.raises(modioException):
            run(self.mod.async_delete_dependencies([]))

        if dependencies:
            run(self.mod.async_delete_dependencies(dependencies))

    def test_async_add_team_member(self):
        try:
            run(
                self.mod.async_add_team_member(
                    "juliacj@cardiff.ac.uk", modio.Level.creator, position="Lord of Tests"
                )
            )
        except modioException as e:
            if e.code != 403:
                raise e from e

    def test_async_delete(self):
        mod = run(self.client.async_get_my_mods(filters=modio.Filter().text("ToDeleteMod"))).results

        if mod:
            run(mod[0].async_delete())
