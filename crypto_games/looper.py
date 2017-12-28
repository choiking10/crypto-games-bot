import random

from .base import CryptoGames
from .bet import Betting, BettingResult
from .handler import CryptoHandler

class Looper:
    def __init__(self, api_key, default_bet: Betting, budget):
        self.games = CryptoGames(api_key)
        self.default_bet = default_bet
        self.handlers = dict()
        self.bet_log = []
        self.budget = budget
        if self.budget == 0:
            self.budget = self.games.balance(default_bet.coin_kind)

    def add_handler(self, handler: CryptoHandler):
        pri = -handler.get_priority()
        if pri not in self.handlers:
            self.handlers[pri] = []

        self.handlers[pri].append(handler)

    def betting(self, bet: Betting):
        data = self.games.place_bat(
            coin_kind=bet.coin_kind,
            under_over=bet.under_over,
            bet=bet.bet,
            payout=bet.payout,
            client_seed=bet.client_seed
        )
        return BettingResult(data, betting=bet)

    def run(self):
        while self.budget > 0:
            result = None
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
                            result = self.betting(bet)
                            self.budget += result.profit
                            h.after_bet(result, self.budget)

            if result is None:
                result = self.betting(self.default_bet)
                self.budget += result.profit

            self.bet_log.insert(0, result)

