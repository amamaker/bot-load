import pytest
from bot_eil_online import Bot

@pytest.fixture
def session_mock(mocker):
    return mocker.MagicMock()

@pytest.fixture
def bot_instance(session_mock):
    playerid = "default_playerid"
    access_token = "default_access_token"
    bot = Bot(playerid, access_token)
    bot.session = session_mock
    return bot

def test_get_lot_success(bot_instance, mocker):
    response_mock = mocker.MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json.return_value = {"key": "value"}
    response_mock.elapsed.total_seconds.return_value = 0.123

    with mocker.patch.object(bot_instance.session, 'get', return_value=response_mock):
        with mocker.patch.object(bot_instance, 'get_current_time', return_value="2020-01-01 12:00:00"):
            result = bot_instance.get_lot()

    assert result == {"key": "value"}

def test_get_lot_failure(bot_instance, mocker):
    response_mock = mocker.MagicMock()
    response_mock.raise_for_status.side_effect = Exception("Error")

    with mocker.patch.object(bot_instance.session, 'get', return_value=response_mock):
        with mocker.patch.object(bot_instance, 'get_current_time', return_value="2020-01-01 12:00:00"):
            with pytest.raises(Exception, match="Error"):
                bot_instance.get_lot()
