import modio

client = modio.Client(api_path="api path goes here (eg. g-123 or u-123)", api_key="api key goes here")
game = client.get_game(947)

MOD_ID = 9084
mod = game.get_mod(MOD_ID)
events = mod.get_events()

# some time later we only want
# to get the latest events

filters = modio.Filter().min(id=events.results[0].id + 1)
new_events = mod.get_events(filters=filters)
