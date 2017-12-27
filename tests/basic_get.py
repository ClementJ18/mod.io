import moddb_wrapper

client = moddb_wrapper.Client(api_key="5d6afb3b1395ecd4dc3c3a614d92ce0c")

def get_game(id):
    """Test ability to retrieve and convert to game object"""
    game = client.get_game(id)

    assert isistance(game, moddb_wrapper.Game())
    assert game.id == id
    

