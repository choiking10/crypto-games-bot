import random

from .exceptions import CryptoException
from .base import CryptoGames
from .handler import CryptoHandler
from .betting_info import Betting, BettingResult

class Looper:
    def __init__(self, api_key, default_betting: Betting, budget=0, target=10.0**15):
        self.games = CryptoGames(api_key)
        self.default_betting = default_betting
        self.handlers = dict()
        self.bet_log = []
        self.budget = budget
        self.target = target

        if self.budget == 0:
            self.budget = self.games.balance(default_betting.coin_kind)

    def add_handler(self, handler: CryptoHandler):
        pri = -handler.get_priority()
        if pri not in self.handlers:
            self.handlers[pri] = []

        self.handlers[pri].append(handler)

    def place_bat(self, betting: Betting):
        data = self.games.place_bat(
            coin_kind=betting.coin_kind,
            under_over=betting.under_over,
            bet=betting.bet,
            payout=betting.payout,
            client_seed=betting.client_seed
        )
        return BettingResult(data, betting=betting)

    def run(self):
        while 0 < self.budget < self.target:
            result = None

            try:
                for _, hs in self.handlers.items():
                    if result is not None:
                        break

                    random.shuffle(hs)
                    for h in hs:
                        if result is not None:
                            break
                        if (
                                random.uniform(0.0, 1.0) <=
                                h.execution_probability(self.bet_log)
                            ):
                            bet = h.place_bet(self.bet_log, self.budget)

                            if bet is not None:
                                if bet.bet > self.budget:
                                    return self.budget

                                result = self.place_bat(bet)
                                self.budget += result.profit
                                h.after_bet(result, self.budget)

                if result is None:

                    if self.default_betting.bet > self.budget:
                        return self.budget
                    result = self.place_bat(self.default_betting)
                    self.budget += result.profit

                self.bet_log.insert(0, result)

            except CryptoException as e:
                print(e.message)

        return self.budget

