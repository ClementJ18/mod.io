.. currentmodule:: modio

Filtering, Sorting and Pagination
----------------------------------
This library supports the filtering and sorting under the form of the Filter object which can be instantiated and
edited in order to fine tune the returned results. First instantiate the filter with or without parameters and then
call any of the various help methods attached to the object to add additional paramaters. In addition to filtering, the object supports three sorting methods: sort, offset and limit. All three are explained in depth in the Filter section of the docs.


:: 

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

In addition, this library also supports and extends the pagination metadata provided by modio in the form of the Pagination object. The pagination object can be used both to gather additional data on the pagination, such as if you've reached the last page, or what page you are on. In addition, it can be passed to the Filter.offset() of the Filter instance you used to obtain the results to get the next page of results easily by simply passing the edited filter instance. For example if we want to get the next page of results we can simply do:
:: 

    import modio

    client = modio.Client(api_key="api key goes here")
    filters = modio.Filter()
    filters.text("The Lord of the Rings")
    games, pagination = client.get_games(filter=filters)

    filters.offset(pagination.next_page())
    games, pagination = client.get_games(filter=filters)
