import pytest
import requests_mock
from bot_eil_online import Bot

class TestBotClass:
    @pytest.fixture
    def bot_class_instance(self):
        playerid = "default_playerid"
        access_token = "default_access_token"
        return Bot(playerid, access_token)

    def test_refresh_tokens_success(self, bot_class_instance, requests_mock):
        mock_response = {"bot": "mocked_data"}
        requests_mock.post("https://demo.com/api/online/session", json=mock_response)

        response = bot_class_instance.refresh_tokens()

        assert response == mock_response

    def test_refresh_tokens_failure(self, bot_class_instance, requests_mock):
        requests_mock.post("https://demo.com/api/online/session", status_code=500)

        with pytest.raises(Exception):
            bot_class_instance.refresh_tokens()