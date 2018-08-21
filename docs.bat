@echo off
python -m pydoc -w modio
move modio.html raw_docs\index.html
python -m pydoc -w modio.client
move modio.client.html raw_docs\modio.client.html
python -m pydoc -w modio.game
move modio.game.html raw_docs\modio.game.html
python -m pydoc -w modio.mod
move modio.mod.html raw_docs\modio.mod.html
python -m pydoc -w modio.objects
move modio.objects.html raw_docs\modio.objects.html
python -m pydoc -w modio.errors
move modio.errors.html raw_docs\modio.errors.html
python -m pydoc -w modio.utils
move modio.utils.html raw_docs\modio.utils.html