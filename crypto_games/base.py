import requests
import json
import random

from .exceptions import CryptoException


def make_random(length):
    choi = [str(i) for i in range(0, 10)]
    for i in range(0, 26):
        choi.append(chr(ord('a') + i))
        choi.append(chr(ord('A') + i))

    ret = ""
    for i in range(length):
        ret += random.choice(choi)

    return ret


class CryptoGames:
    """
    api href : https://api.crypto-games.net

    """
    BASE = "https://api.crypto-games.net"
    VERSION = "v1"
    API_KEY = None

    def __init__(self, key):
        self.API_KEY = key

    def _response_process(self, res):
        if res.status_code != 200:
            result = ""
            try:
                result = json.loads(res.content.decode("utf-8"))["Message"]
            except ValueError:
                result = "[{}]json can not decode".format(res.status_code)
            raise CryptoException(result)

        try:
            return json.loads(res.content.decode("utf-8"))
        except ValueError:
            result = "[{}]json can not decode".format(res.status_code)
            raise CryptoException(result)

    def _get_request(self, api_name, coin_kind=None,
                     api_key=None, param=None, bet_id=None, **kwargs):
        url = '/'.join([self.BASE, self.VERSION, api_name])
        if coin_kind:
            url = '/'.join([url, coin_kind])

        if bet_id:
            url = '/'.join([url, str(bet_id)])

        if api_key:
            url = '/'.join([url, api_key])

        count = 0
        res = None
        while count < 10:
            try:
                res = requests.get(url, params=param, timeout=10, **kwargs)
                break
            except requests.exceptions.Timeout as e:
                count += 1

        if res is None:
            raise CryptoException("timeout exception!")

        return self._response_process(res)

    def _post_request(self, api_name, coin_kind=None,
                      api_key=None, data=None, **kwargs):
        url = '/'.join([self.BASE, self.VERSION, api_name])

        if coin_kind:
            url = '/'.join([url, coin_kind])

        if api_key:
            url = '/'.join([url, api_key])

        count = 0
        res = None
        while count < 10:
            try:
                res = requests.post(url, json=data, timeout=10, **kwargs)
                break
            except requests.exceptions.Timeout as e:
                count += 1

        if res is None:
            raise CryptoException("timeout exception!")

        return self._response_process(res)

    def place_bat(self, coin_kind, bet: float, payout: float,
                  under_over=True, client_seed=None):

        if client_seed is None:
            client_seed = make_random(40)

        data = {
            "Bet": bet,
            "Payout": payout,
            "UnderOver": under_over,
            "ClientSeed": client_seed
        }

        return self._post_request("placebet", coin_kind,
                                  api_key=self.API_KEY, data=data)

    def settings(self, coin_kind):
        return self._get_request("settings", coin_kind)

    def stats(self, coin_kind):
        return self._get_request("coinstats", coin_kind)

    def balance(self, coin_kind):
        return self._get_request("balance",
                                 coin_kind=coin_kind,
                                 api_key=self.API_KEY)

    def user(self, coin_kind):
        return self._get_request("user",
                                 coin_kind=coin_kind,
                                 api_key=self.API_KEY)

    def next_seed(self, coin_kind):
        return self._get_request("nextseed",
                                 coin_kind=coin_kind,
                                 api_key=self.API_KEY)

    def bet_info(self, bet_id):
        return self._get_request("bet",
                                 bet_id=bet_id)
