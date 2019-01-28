import enum

class Status(enum.Enum):
    """
    Status of the game:
        * 0 : Not accepted
        * 1 : Accepted (default)
        * 2 : Archived (default)
        * 3 : Deleted
    """
    not_accepted = 0
    accepted     = 1
    archived     = 2
    deleted      = 3

class Presentation(enum.Enum):
    """
    Presentation style used on the mod.io website:
        * 0 : Display mods for that game in a grid on mod.io
        * 1 : Display mods for that game in a table on mod.io
    """
    grid  = 0
    table = 1

class Submission(enum.Enum):
    """
    Submission process modders must follow:
        * 0 : Mod uploads must occur via a tool created by the game developers
        * 1 : Mod uploads can occur from anywhere, including the website and API
    """
    restricted   = 0
    unrestricted = 1

class Curation(enum.Enum):
    """
    Curation process used to approve mods:
        * 0 : No curation: Mods are immediately available to play
        * | 1 : Paid curation: Mods are immediately available to play unless 
          | they choose to receive donations. These mods must be accepted to be listed
        * 2 : Full curation: All mods must be accepted by someone to be listed
    """
    no_curation   = 0
    paid_curation = 1
    full_curation = 2

class Community(enum.IntFlag):
    """
    Community features enabled on the mod.io website:
        * 0 : All of the options below are disabled
        * 1 : Discussion board enabled
        * 2 : Guides and news enabled
        * | ? : Above options can be added together to create custom settings (e.g 3 : 
          | discussion board, guides and news enabled)
    """
    disabled          = 0
    discussion_boards = 1
    guides_news       = 2

class Revenue(enum.IntFlag):
    """
    Revenue capabilities mods can enable:
        * 0 : All of the options below are disabled
        * 1 : Allow mods to be sold
        * 2 : Allow mods to receive donations
        * 4 : Allow mods to be traded
        * 8 : Allow mods to control supply and scarcity
        * | ? : Above options can be added together to create custom settings (e.g 3 :
          | allow mods to be sold and receive donations)
    """
    disabled     = 0
    sold         = 1
    donations    = 2
    traded       = 4
    full_control = 5

class APIAccess(enum.IntFlag):
    """
    Level of API access allowed by this game:
        * 0 : All of the options below are disabled
        * 1 : Allow 3rd parties to access this games API endpoints
        * | 2 : Allow mods to be downloaded directly (if disabled all download URLs will contain a frequently 
          | changing verification hash to stop unauthorized use)
        * | ? : Above options can be added together to create custom settings (e.g 3 : 
          | allow 3rd parties to access this games API endpoints and allow mods to be
          | downloaded directly)
    """
    disabled         = 0
    third_party      = 1
    direct_downloads = 2

class MaturityOptions(enum.Enum):
    """
    If the game allows developers to flag mods as containing mature content:
        * | 0 : Don't allow mod developpers to decide whether or not to flag their mod as
          | containing mature content (if game devs wish to handle it)
        * 1 : Allow mod developpers to decide whether or not to flag their mod as containing mature content
    """
    forbidden = 0
    allowed   = 1

class Maturity(enum.IntFlag):
    """
    Maturity options flagged by the mod developer, this is only relevant if the parent game allows 
    mods to be labelled as mature:

        * 0 : None
        * 1 : Alcohol
        * 2 : Drugs
        * 4 : Violence
        * 8 : Explicit
        * | ? : Above options can be added together to create custom settings (e.g 3 : 
          | alcohol and drugs present)
    """
    none     = 0
    alcohol  = 1
    drugs    = 2
    violence = 4
    explicit = 8

class VirusStatus(enum.Enum):
    """
    Current virus scan status of the file. For newly added files that have yet to 
    be scanned this field will change frequently until a scan is complete:

        * 0 : Not scanned
        * 1 : Scan complete
        * 2 : In progress
        * 3 : Too large to scan
        * 4 : File not found
        * 5 : Error Scanning
    """
    not_scanned   = 0
    scan_complete = 1
    in_progress   = 2
    too_large     = 3
    not_found     = 4
    error         = 5

class Visibility(enum.Enum):
    """
    Visibility of the mod (see status and visibility for details):
        * 0 : Hidden
        * 1 : Public
    """
    hidden = 0
    public = 1

class Level(enum.Enum):
    """
    Level of permission the user has:
        * 1 : Moderator (can moderate comments and content attached)
        * | 4 : Creator (moderator access, including uploading builds and edit all settings except 
          | supply and team members)
        * 8 : Administrator (full access, including editing the supply and team)
    """
    moderator = 1
    creator   = 4
    admin     = 8

class Report(enum.Enum):
    """
    The type of report you are submitting. Must be one of the following values:
        * 0 : Generic Report
        * 1 : DMCA Report
    """
    generic   = 0
    dmca      = 1

class EventType(enum.Enum):
    """
    An enum to render all event types easy to compare:
        * 0  : Primary file changed
        * 1  : Mod is marked as accepted and public
        * 2  : Mod is marked as not accepted, deleted or hidden
        * 3  : The mod was updated (triggered when any column value changes)
        * 4  : The mod has been permanently erased. This is an orphan record, looking up this id will return no data
        * 5  : A user has joined or left the mod team
        * 6  : A user has joined the mod team
        * 7  : A user has left the mod team
        * 8  : A mod has been subscribed to
        * 9  : A mod has been unsubscribed to
        * 10 : An event has occured which is not supported by this enum
    """
    file_changed  = 0
    available     = 1
    unavailable   = 2
    edited        = 3
    deleted       = 4
    team_changed  = 5
    team_join     = 6
    team_leave    = 7
    subscribe     = 8
    unsubscribe   = 9
    other         = 10   

class RatingType(enum.Enum):
    """
    The type of rating submitted (good, bad, neutral):
            * -1 : Negative ratings
            *  0 : Delete the rating
            *  1 : Positive rating
    """
    bad     = -1
    neutral =  0
    good    =  1
