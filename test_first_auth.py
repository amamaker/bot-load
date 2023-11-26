import pytest
from unittest.mock import MagicMock, patch
from bot_eil_online import Bot

class Test_Bot_Class:
    @pytest.fixture
    def bot_class_instance(self):
        with patch('bot_eil_online.Session') as mock_session:
            playerid = "default_playerid"
            access_token = "default_access_token"
            instance = Bot(playerid, access_token)
            instance.session = mock_session()
            return instance

    def test_first_auth_success(self, bot_class_instance):
        mock_response = MagicMock()
        mock_response.json.return_value = {'some_key': 'some_value'}
        mock_response.elapsed.total_seconds.return_value = 0.1
        bot_class_instance.session.get.return_value = mock_response

        response, time_taken = bot_class_instance.first_auth()

        assert response == {'some_key': 'some_value'}
        assert time_taken > 0

    def test_first_auth_failure(self, bot_class_instance):
        bot_class_instance.session.get.side_effect = Exception('Exception')

        response, time_taken = bot_class_instance.first_auth()

        assert response is None
        assert time_taken == 0
