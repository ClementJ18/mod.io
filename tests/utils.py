import asyncio

import modio

use_test_env = False


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class FakeRequest(modio.Object):
    def json(self):
        return self.json_data
