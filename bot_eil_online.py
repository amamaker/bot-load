import random
from ctypes import windll
from datetime import datetime
import time
from requests import Session
import uuid
from requests.exceptions import HTTPError


class Bot:
    URL = "https://demo.com"
    BASE_URL = "https://demo.com"

    def __init__(self, playerid, access_token, session=None):
        self.session = session or Session()
        self.session.trust_env = False
        self.uuid = str(uuid.uuid4())[-8:]
        self.access_token = None
        self.refresh_token = None
        self.bets = None
        self.random_game_id = 0
        self.random_bet_id = 0
        self.timing = 0.1
        self.deposit_amount = 1000000
    def first_auth(self):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "username": self.uuid
        }
        api = "/api/develop/session"
        try:
            request = self.session.get(f"{self.URL}{api}", headers=headers, params=params)
            request.raise_for_status()
            response = request.json()
            response_time = request.elapsed.total_seconds()
            return response, int(response_time * 1000)
        except Exception as error:
            return None, 0

    def refresh_tokens(self):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "refreshToken": self.refresh_token
        }
        api = "/api/online/session"
        try:
            request = self.session.post(f"{self.URL}{api}", headers=headers, json=data)
            request.raise_for_status()
            response = request.json()
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
            raise
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            raise
        else:
            response_time = request.elapsed.total_seconds()
            print(f"{self.get_current_time()} -- Refresh in {int(response_time * 1000)} ms")
            return response

    def get_lot(self):
        api = "/api/develop/lot"
        params = {
            "username": self.uuid
        }
        try:
            request = self.session.get(f"{self.URL}{api}", params=params)
            request.raise_for_status()
            response = request.json()
            response_time = request.elapsed.total_seconds()
            print(f"{self.get_current_time()} -- Get bets in {int(response_time*1000)} ms")
            return response
        except Exception as error:
            print(error)
            raise

    def get_balance(self):
        api = "/api/online/balance"
        headers = {
            "playerid": self.uuid,
            "username": self.uuid,
            "session": self.access_token
        }
        try:
            request = self.session.get(f"{self.URL}{api}", headers=headers)
            request.raise_for_status()
            response = request.json()
            return response
        except Exception as error:
            raise RuntimeError(f"Failed to get balance: {error}")

    def add_credit(self, amount):
        api = "/api/develop/deposit"
        params = {
            "amount": amount,
            "userId": self.uuid
        }
        try:
            request = self.session.post(f"{self.URL}{api}", params=params)
            request.raise_for_status()
            response = request.json()
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
            return {"status": "error", "error_message": str(http_error)}
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            return {"status": "error", "error_message": str(error)}
        else:
            return {"status": "success", "response": response}
    def init_play(self):
        api = "/api/online/init/"
        headers = {
            "playerid": self.uuid,
            "username": self.uuid,
            "session": self.access_token
        }
        try:
            request = self.session.get(f"{self.URL}{api}{self.random_bet_id}", headers=headers)
            request.raise_for_status()
            response = request.json()
        except Exception as error:
            print(error)
        else:
            response_time = request.elapsed.total_seconds()
            print(f"{self.get_current_time()} -- Init in {int(response_time*1000)} ms")
            return response

    def play(self):
        api = "/api/online/bet/"
        headers = {
            "playerid": self.uuid,
            "username": self.uuid,
            "session": self.access_token
        }
        try:
            request = self.session.post(f"{self.URL}{api}{self.random_bet_id}", headers=headers)
            request.raise_for_status()
            response = request.json()
        except Exception as error:
            print(error)
        else:
            response_time = request.elapsed.total_seconds()
            print(f"{self.get_current_time()} -- Buy ticket in {int(response_time*1000)} ms")
            return response

    def collect(self):
        api = "/api/online/collect"
        headers = {
            "playerid": self.uuid,
            "username": self.uuid,
            "session": self.access_token
        }
        try:
            request = self.session.post(f"{self.URL}{api}", headers=headers)
            request.raise_for_status()
            response = request.json()
        except Exception as error:
            print(error)
        else:
            response_time = request.elapsed.total_seconds()
            print(f"{self.get_current_time()} -- Collect in {int(response_time*1000)} ms")
            return response

    def get_current_time(self):
        return str(datetime.now())[:-3]

if __name__ == "__main__":
    playerid = Bot.init_play["playerid"]
    access_token = Bot.init_play["session"]
    bot = Bot(playerid, access_token, session=None)
    print("Serial Number:", bot.uuid)

    first_auth = bot.first_auth()
    bot.access_token = first_auth["access_token"]
    bot.refresh_token = first_auth["refresh_token"]
    bot.add_credit(bot.deposit_amount)
    while True:
        print("=" * 50)
        new_tokens = bot.refresh_tokens()
        bot.access_token = new_tokens["access_token"]
        bot.refresh_token = new_tokens["refresh_token"]

        print("=" * 50)
        bot.bets = bot.get_lot()

        random_game = random.choice(bot.bets.get("bets"))
        bot.random_game_id = random_game.get("id")

        random_bet = random.choice(random_game.get("bets"))
        bot.random_bet_id = random_bet.get("id")

        bot.init_play()

        range_plays = (1, 10)
        random_number = random.randint(*range_plays)
        print("=" * 50)
        print("Game:", random_game.get("name"))
        print("Bet:", random_bet.get("value"))
        print("Tickets to play:", random_number)
        print("=" * 50)
        windll.kernel32.SetConsoleTitleW(
            f'{bot.URL} -- {bot.uuid} -- {random_game.get("name")} -- Bet: {random_bet.get("value")}')

        if bot.get_balance().get("realBalance") < random_bet.get("value"):
            print("Денег не хватает!")
            bot.add_credit(bot.deposit_amount)

        for i in range(random_number):
            play = bot.play()
            collect = bot.collect()
            time.sleep(bot.timing)
