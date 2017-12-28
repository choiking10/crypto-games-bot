import random
import copy

from crypto_games.handler import CryptoHandler
from crypto_games.bet import Betting


class MyHandler(CryptoHandler):

    def __init__(self):
        self.maxi = []
        super(MyHandler, self).__init__(priority=1000, probability=1)

    def place_bet(self, bet_log, budget):
        idx = 0
        tmp = []
        while idx < len(bet_log) and bet_log[idx].profit > 0:
            tmp.append(bet_log[idx].id)
            idx += 1

        if len(self.maxi) < len(tmp):
            self.maxi = tmp
            print(len(self.maxi), self.maxi)

            with open("yh_result.txt", "w") as f:
                f.write(str(len(self.maxi)) + "\n")
                for i in self.maxi:
                    f.write(str(i) + "\n")

                f.close()
        if len(bet_log) > 0:
            p_bet = copy.deepcopy(bet_log[0].betting)

            p_bet.under_over = random.choice([True, False])
            return p_bet
        return None

    def after_bet(self, bet_result, budget):
        pass