import modio

client = modio.Client(api_path="api path goes here (eg. g-123 or u-123)", access_token="oauth2 token goes here")
newmod = modio.NewMod(
    name="A LOTR Toilet Mod",
    name_id="lotr-toilets",
    summary="Embark on a fascinating journey through Middle Earth's most beautiful toilets.",
    description="<h1>It's a very good mod</h1><br><h2>You should play it</h2>",
    homepage="https://me.toilets.lotr",
    stock=400,
    maturity=11,  # alcohol, drugs, explicit
    metadata="toilets,lotr,hd,cool",
    logo="path/to/file/lotr_toilet.jpg"
)

newmod.add_tags("texture overhaul", "quality", "medium")

game = client.get_game(234)
mod = game.add_mod(newmod)

print(mod)
# <modio.Mod id=567 name=A LOTR Toilet Mod game_id=234>
