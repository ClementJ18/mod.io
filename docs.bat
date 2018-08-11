@echo off
python -m pydoc -w modio
xcopy /y modio.html docs\index.html
move modio.html docs\modio.html
python -m pydoc -w modio.client
move modio.client.html docs\modio.client.html
python -m pydoc -w modio.game
move modio.game.html docs\modio.game.html
python -m pydoc -w modio.mod
move modio.mod.html docs\modio.mod.html
python -m pydoc -w modio.objects
move modio.objects.html docs\modio.objects.html
python -m pydoc -w modio.errors
move modio.errors.html docs\modio.errors.html