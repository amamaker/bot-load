import pytest
from bot_eil_online import Bot

class FakeResponseSuccess:
    def raise_for_status(self):
        pass

    def json(self):
        return {"status": "success"}

    def post(self, url, params):
        return self

fake_session = None

@pytest.mark.parametrize("fake_session", [None])
def test_add_credit_success(fake_session):
    bot_class_instance = Bot(playerid="playerid", access_token="access_token", session=fake_session)
    bot_class_instance.session = FakeResponseSuccess()

    result = bot_class_instance.add_credit(100)

    if result["status"] == "success":
        assert True
    else:
        assert False, f"Unexpected result: {result}"
