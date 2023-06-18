import asyncio

use_test_env = False


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
