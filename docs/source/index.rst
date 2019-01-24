.. modio documentation master file, created by
   sphinx-quickstart on Wed Dec 26 17:51:05 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. currentmodule:: modio

Welcome to modio's documentation!
=================================

modio.py is a wrapper package for the mod.io API.

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

   pip install -U git+git://github.com/ClementJ18/mod.io.git@0.2


.. toctree::
   :maxdepth: 2
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
