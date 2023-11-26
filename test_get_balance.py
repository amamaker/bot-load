import pytest
from bot_eil_online import Bot

class TestBotClass:
    @pytest.fixture
    def instance(self):
        return Bot(playerid="fake_uuid", access_token="fake_token")

    def test_get_balance(self, instance, mocker):
        mocker.patch.object(instance.session, 'get', side_effect=Exception("Fake error"))

        with pytest.raises(RuntimeError, match="Failed to get balance: Fake error"):
            instance.get_balance()