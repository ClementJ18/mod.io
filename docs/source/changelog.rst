.. currentmodule:: modio

Changelog
==========
The page attempt to keep a clear list of breaking/non-breaking changes and new features made to the libary.

.. contents:: Table of Contents
   :local:
   :backlinks: none

v0.6.0
------
This patch adds support for targetting platforms and portals

New Features
#############
* The behavior of the library when being ratelimited can now be customised with the `Client.ratelimit_max_sleep` parameter. 

v0.5.0
------
This patch adds support for targetting platforms and portals

New Features
#############
* New `platform` and `portal` parameters for `Client`
* New `Client.set_portal` and `Client.set_platform` methods
* New `TargetPortal` to represent portals
* Library will now retry any ratelimited requests once after sleeping

Bugs Fixed
###########
* Fixed ratelimit sleep not being enforced properly


v0.4.3
-------

New Features
#############
* `Platform` object has been split into `GamePlatform`, `ModPlatform` and `ModFilePlatform` to better reflect the API models
* New `Mod.platforms` attribute
* `Game.platforms`is now a `List[GamePlatform]`, different class but same attributes

Bugs Fixed
###########
* `Modfile.platforms` fixed, now a `List[ModFilePlatforms]` with correct attributes

v0.4.2
-------

New Features
##############
* `ModFile` now has a `platforms` attribute

Bugs Fixed
###########
* `Game` now properly has a `platforms` attribute
* `Filter.max` no longer overflows

v0.4.1
-------
Small dependency bugfix

v0.4.0
--------
This patch focuses on making sure none of the new attributes of the mod.io API models slip through the
cracks and that they are all being parsed and added to the correct library models.

New Features
#############
* `Client.email_exchange` now supports `date_expire`
* New object `Platform`
* `Stats` renamed to `ModStats`, new `GameStats` object
* New enum `TargetPlatform`
* New attributes for Game: `stats`, `other_urls`, `platforms`
* `expires` attribute renamed to `date_expires`
* New methods `Comment.add_positive_karma` and `Comment.add_negative_karma` and async equivalents
* Added comment added/deleted event support
* `Game.get_stats` renamed to `Game.get_mods_stats`
* New function `Game.get_stats` that gets stats for the game rather than for the mods of the game
* New example `examples/polling_events` showing how to use the filter class to only get the latest attributes
* `Game.add_tag_options` now supports the `locked` option
* New attribute for TagOption: `locked`
* `Rating.mod` renamed to `Rating.mod_id`
* Library is now typed, making it easier to use with IDEs

Removed Features
##################
* `Comment.mod` is now deprecated and removed, replaced with `Comment.resource_id`
* `Comment.karma_guest` is deprecated and has been removed


v0.3.1
--------
This version of the library represents a major rework. The most important is the merge of the async and 
sync library. They now form a single library in which blocking methods have a async equivalent with the
same name but prefixed with `async_`

New Features
#############
* Ratelimits are now enforced by the library
* `filter` parameters of functions renamed to `filters`
* `Mod.game` and `ModFile.game` renamed to `game_id`
* Muting/unmuting users and getting mutes now supported
* Editing/adding/deleting comments now supported
* `Game.submitter` is now optional
* Many methods that used to take `id` now take `{entity}_id` where {entity} is something like `mod` or `game`
* Entities no longer update themselves but rather return the updated entity where possible.


Removed Features
#################
* Many of exceptions have been removed, the library now uses the base exception for most errors
* Removed the account links support, looking into a better implementation
* Many removed endpoints have had their method also removed
