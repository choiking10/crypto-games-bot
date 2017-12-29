import random
import copy

from crypto_games.handler import CryptoHandler
from crypto_games.betting_info import Betting


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


class KooHandler(CryptoHandler):
    def __init__(self, coin_kind, base_rate=0.001, base_payout=1.1, base_pump=10,
                 seed_money=None,
                 priority=10000, probability=0.5):
        super(KooHandler, self).__init__(priority=priority,
                                         probability=probability)
        self.coin_kind = coin_kind
        self.base_rate = base_rate
        self.base_payout = base_payout
        self.base_pump = base_pump
        self.seed_money = None
        self.accum = 0

    def place_base_bet(self, place_money, under_over):
        return Betting(
            payout=self.base_payout,
            under_over=under_over,
            bet=place_money,
            coin_kind=self.coin_kind,
            additional=KooHandler
        )

    def execution_probability(self, bet_log):
        if len(bet_log) < 3:
            return 0

        return super(KooHandler, self).execution_probability(bet_log)

    def place_bet(self, bet_log, budget):
        check_under = 0
        check_over = 0
        if self.seed_money is None:
            self.seed_money=budget

        for i in range(0, 3):
            if 5 <= bet_log[i].roll <= 45:
                check_under += 1
            else:
                check_under -= 2

            if 60 <= bet_log[i].roll <= 95:
                check_over += 1
            else:
                check_over -= 2

        place_money = self.seed_money * self.base_rate * \
                      (self.base_pump ** self.accum)
        if check_under >= 2:
            return self.place_base_bet(place_money, True)
        if check_over >= 2:
            return self.place_base_bet(place_money, False)

        return None

    def after_bet(self, bet_result, budget):
        if bet_result.profit < 0:
            self.accum += 1
        else:
            self.accum = 0
        super(KooHandler, self).after_bet(bet_result, budget)
