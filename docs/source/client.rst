.. currentmodule:: modio

.. _Ratelimit Overview:

Ratelimits and Retries
------------------------
By default, when the library gets ratelimited, it will sleep for the duration required and then retry sending the request. This behavior
covers most cases as the library will only sleep for about 60 seconds or less. However this is not always desirable and as such
the library also provides you with the ability to decide when you want to sleep and when you want the library to raise the error
through the `Client.ratelimit_max_sleep` parameter. By default this parameter is set to infinity which means that the library will
always sleep the full duration. Be warned, if you are doing some heavy work using POST requests this could make you sleep for large durations
like one hour. If you want finer control, you can pass an int representing the maximum number of seconds to sleep. Passing 0 will mean
the libary will never sleep and always raise the error.

When letting the library raise the error, you can handle the rateliming yourself using the `Client.retry_after` attribute to know
how long you should wait before trying the request again. Some quick exmaples to make everything clear:

* `ratelimit_max_sleep` is 60 and you're ratelimited with `retry_after` being 60 -> library sleeps for 60 seconds
* `ratelimit_max_sleep` is 60 and you're ratelimited with `retry_after` being 3600 -> library raises the error
* `ratelimit_max_sleep` is infinity and you're ratelimited with `retry_after` being 60 -> library sleeps for 60 seconds
* `ratelimit_max_sleep` is 0 and you're ratelimited with `retry_after` being 3600 -> library raises the error
* `ratelimit_max_sleep` is 3600 and you're ratelimited with `retry_after` being 3600 -> library sleeps for 3600 seconds


Client
-------
.. automodule:: modio.client
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: Connection
