import modio

client = modio.Client(api_key="api key goes here")
filters = modio.Filter()

filters.text("The Lord of the Rings")
#This will return every result where the name column contains any of 
#the following words: 'The', 'Lord', 'of', 'the', 'Rings'

filters.equal(id=10)
# Get all results where the id column value is 10.

filters.like(name="The Witcher*")
#Get all results where 'The Witcher' is succeeded by any value

filters.not_like(name="*Asset Pack")
#Get all results where Asset Pack NOT is proceeded by any value.

filters.values_in(id=[3,11,16,29])
#Get all results where the id column value is 3, 11, 16 and 29.

filters.sort("name")
#Sort name in ascending order

filters.sort("id", reverse=True)
#Sort id in descending order

filters.limit(20)
#limit to 20 results

filters.offset(5)
#skip the first five results

games, pagination_metadata = client.get_games(filter=filters)
#returns all the result that meet the above criteria
