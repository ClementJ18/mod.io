.. modio documentation master file, created by
   sphinx-quickstart on Wed Dec 26 17:51:05 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. currentmodule:: modio

Welcome to modio's documentation!
=================================
.. image:: https://readthedocs.org/projects/modio/badge/?version=latest
   :target: https://modio.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: Licence: MIT

.. image:: https://img.shields.io/github/issues/ClementJ18/mod.io.svg
   :target: https://github.com/ClementJ18/mod.io/issues
   :alt: Open Issues

.. image:: https://img.shields.io/github/issues-pr/ClementJ18/mod.io.svg
   :target: https://github.com/ClementJ18/mod.io/pulls
   :alt: Open PRs

.. image:: https://img.shields.io/github/release/ClementJ18/mod.io.svg
   :alt: Latest Release

.. image:: https://img.shields.io/github/stars/ClementJ18/mod.io.svg?label=Stars&style=social 
   :target: https://github.com/ClementJ18/mod.io

.. image:: https://img.shields.io/discord/389039439487434752.svg
   :target: https://discord.gg/Hkq7X7n

.. image:: https://img.shields.io/github/commits-since/ClementJ18/mod.io/latest.svg
    :target: https://github.com/ClementJ18/mod.io/releases/latest

modio.py is a wrapper package for the mod.io API. Most blocking methods have both a synchronous version and async method
for use within async applications.

Basic Usage
-----------------
:: 

   import modio

   client = modio.Client(
      api_key="your api key here", 
      auth="your o auth 2 token here"
   )

   game = client.get_game(345)
   #gets the game with id 345

   print(game.name)
   #prints the name of the game

   mod = game.get_mod(231)
   #gets the mod for that game with id 231

Getting an OAuth 2 Access Token
--------------------------------

To perform writes, you will need to authenticate your users via OAuth 2. To make this easy this library provides you with two functions to use in order to obtain your Access Token. You will need an API Key and an email adress to which you have access in order for this to work. Once you have both, follow the example below, you can either run this in a REPL or as a Python script. Don't forget to edit the script to add your own api key and email adress.

Example
-----------
:: 

   import modio

   client = modio.Client(api_key="your api key here")

   #request a security code be sent at this email adress
   client.email_request("necro@mordor.com")

   #check your email for the security code
   code = input("Code: ")

   oauth2 = client.email_exchange(code)
   #your oauth2 token is now stored in the variable

   #to save into a file simply
   file = open("oauth2.txt", "w")
   file.write(oauth2)
   file.close()

   #and now the token is stored in oauth2.txt

Installation
-------------
::

   pip install mod.io

Uninstalling
-------------
::

   pip uninstall modio


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   client
   game
   mod
   objects
   filtering&sorting
   async
   utils
   enums
   errors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
