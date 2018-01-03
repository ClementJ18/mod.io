# mod.io

A WIP wrapper for the mod.io API in Python. 

## Getting an OAuth 2 Access Token
To perform writes, you will need to authenticate your users via OAuth 2. To make this easy this library provides you with two functions to use in order to obtain your Access Token. You will need an API Key and an email adress to which you have access in order for this to work. Once you have both, follow the example below, you can either run this in a REPL or as a Python script. Don't forget to edit the script to add your own api key and email adress.

```py
import modio

client = modio.Client(api_key="your api key here")

#request a security code be sent at this email adress
client.email_request("necro@mordor.com")

#check your email for the security code
code = input("Code: ")

oauth2 = client.email_exchange(code)["access_token"]

#your oauth2 token is now stored in the variable

#to save into a file simply
file = open("oauth2.txt", "w")
file.write(oauth2)
file.close()

#and now the token is stored in oauth2.txt
```
