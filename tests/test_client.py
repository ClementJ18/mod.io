from unittest import mock

import pytest
import modio
from modio.errors import modioException

try:
    from .config import game_api_key, access_token
except ModuleNotFoundError:
    import os

    game_api_key = os.environ["GAME_API_KEY"]
    access_token = os.environ["ACCESS_TOKEN"]

from .utils import FakeRequest, run, use_test_env


class TestClient:
    def test_paths(self):
        client = modio.Client(api_key="fake key", test=use_test_env)
        # pylint: disable=W0212
        assert use_test_env == ("test" in client.connection._base_path)

        client.connection.test = not use_test_env
        # pylint: disable=W0212
        assert use_test_env != ("test" in client.connection._base_path)

    def test_oauth_access(self):
        client = modio.Client(access_token=access_token, test=use_test_env)

        client.get_my_user()
        client.get_my_subs()
        client.get_my_events()
        client.get_my_games()
        client.get_my_mods()
        client.get_my_modfiles()
        client.get_my_ratings()
        client.get_my_mutes()

    def test_api_token(self):
        client = modio.Client(api_key=game_api_key, test=use_test_env)
        games = client.get_games().results

        if games:
            client.get_game(games[0].id)

    def test_async_oauth_access(self):
        client = modio.Client(access_token=access_token, test=use_test_env)
        run(client.start())

        run(client.async_get_my_user())
        run(client.async_get_my_subs())
        run(client.async_get_my_events())
        run(client.async_get_my_games())
        run(client.async_get_my_mods())
        run(client.async_get_my_modfiles())
        run(client.async_get_my_ratings())
        run(client.async_get_my_mutes())

        run(client.close())

    def test_async_api_token(self):
        client = modio.Client(api_key=game_api_key, test=use_test_env)
        with pytest.raises(AttributeError):
            run(client.async_get_games())

        run(client.start())

        games = run(client.async_get_games()).results

        if games:
            run(client.async_get_game(games[0].id))

        run(client.close())

    def test_platform(self):
        client = modio.Client(api_key=game_api_key, test=use_test_env)

        assert client.connection.platform is None

        client.set_platform(modio.enums.TargetPlatform.linux)

        assert client.connection.platform is modio.enums.TargetPlatform.linux

        headers = client.connection._define_headers(2)

        assert "X-Modio-Platform" in headers
        assert headers["X-Modio-Platform"] is modio.enums.TargetPlatform.linux.value

    def test_portal(self):
        client = modio.Client(api_key=game_api_key, test=use_test_env)

        assert client.connection.portal is None

        client.set_portal(modio.enums.TargetPortal.facebook)

        assert client.connection.portal is modio.enums.TargetPortal.facebook

        headers = client.connection._define_headers(2)

        assert "X-Modio-Portal" in headers
        assert headers["X-Modio-Portal"] is modio.enums.TargetPortal.facebook.value

    @pytest.mark.parametrize(
        "retry_after, max_sleep, expected", [(60, 0, False), (60, 60, True), (0, 60, True), (60, 3600, True)]
    )
    @mock.patch("time.sleep")
    def test_ratelimit(self, sleep_mock, retry_after, max_sleep, expected):
        client = modio.Client(access_token=access_token, test=use_test_env, ratelimit_max_sleep=max_sleep)
        with pytest.raises(modioException):
            client.connection._post_process(
                FakeRequest(
                    status_code=429,
                    headers={"retry-after": retry_after},
                    json_data={"error": {"code": "", "message": "", "error_ref": ""}},
                )
            )
            assert sleep_mock.called == expected
