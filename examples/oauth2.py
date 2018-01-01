#This example shows how to gain an OAuth 2 Access Token through the Email Authentication Flow to gain Write access
import modio_wrapper.client

client = client.Client(api_key="your api key here")

#request a security code be sent at this email adress
client.email_request("necro@mordor.com")

#check your email for the security code
code = input("Code: ")

oauth2 = client.email_exchange(code)["access_token"]

#your oauth2 token is now stored in the variable

#to save simply
file = open("oauth2.txt", "w")
file.write(oauth2)
file.close()

#and now the token is stored in oauth2.txt

