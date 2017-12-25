import random

from .base import CryptoGames
from .bet import Betting, BettingResult
from .handler import CryptoHandler

class Looper:
    def __init__(self, api_key, default_bet: Betting):
        self.games = CryptoGames(api_key)
        self.default_bet = default_bet
        self.handlers = dict()
        self.bet_log = []

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
        while True:
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
                        bet = h.place_bet(self.bet_log)

                        if bet is not None:
                            result = self.betting(bet)
                            h.after_bet(result)

            if result is None:
                result = self.betting(self.default_bet)

            self.bet_log.insert(0, result)

