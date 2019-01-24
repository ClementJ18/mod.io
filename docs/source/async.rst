.. currentmodule:: modio

.. _async-version:

Asynchronous mod.io
=====================
With the rising demand for async-friendly libraries, this library will install an async version alongside the regular sync library. It is a clone in everyway, with the only difference being that functions that interact with the mod.io API are now coroutines. Due to the very little difference between the two wrappers, the same documentation is used with methods that become corouties in the async version being marked with:

        |coro|

and async exclusive elements being marked with:

        |async|

Basic Usage
-----------------
:: 

    import async_modio as modio
    import asyncio

    async def example():
        client = modio.Client(api_key="your api key here", auth="your o auth 2 token here")

        game = await client.get_game(345)
        #gets the game with id 345

        print(game.name)
        #prints the name of the game

        mod = await game.get_mod(231)
        #gets the mod for that game with id 231

        await client.close()
        #cleans up the client to gracefully shut down, client will have to be 
        #re initialized if other queries are to be made

    def main():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(example())
        loop.close()

    if __name__ == '__main__':
          main()  

Getting an OAuth 2 Access Token
--------------------------------

To perform writes, you will need to authenticate your users via OAuth 2. To make this easy this library provides you with two functions to use in order to obtain your Access Token. You will need an API Key and an email adress to which you have access in order for this to work. Once you have both, follow the example below, you can either run this in a REPL or as a Python script. Don't forget to edit the script to add your own api key and email adress.

Example
-----------
:: 

    import async_modio as modio
    import asyncio

    async def auth()
        client = modio.Client(api_key="your api key here")

        #request a security code be sent at this email adress
        await client.email_request("necro@mordor.com")

        #check your email for the security code
        code = input("Code: ")

        oauth2 = await client.email_exchange(code)

        #your oauth2 token is now stored in the variable

        #to save simply
        with open("oauth2.txt", "w") as f:
            f.write(oauth2)

        #and now the token is stored in oauth2.txt

    def main():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(auth())
        loop.close()

    if __name__ == '__main__':
          main() 

Installation
-------------
::

   pip install -U git+git://github.com/ClementJ18/mod.io.git@0.2


