class Object():
    def __init__(self,):


class Game():
    def __init__(self,):
        self.id = id #int, game ID
        self.submitter = submitter #User, user who submitted the game
        self.date_added = date_added #int, unix timestamp
        self.date_updated = date_updated #int, unix timestamp
        self.date_live = date_live #int, unix timestamp
        self.presentation = presentation #int, determines presentation style. 0-1
        self.community = community #int, determines right of community members with the game. 0-3
        self.submission = submission #int, determines submission process. 0-1
        self.curation = curation #int, determines the curation process. 0-2
        self.revenue = revenue #int, determines revenue capabilities. combination of 1, 2, 4, 8
        self.api = api #int, determines 