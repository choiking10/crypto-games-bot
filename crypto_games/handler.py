import copy
import random

from crypto_games import bet

class CryptoHandler:
    total_profit = 0

    def get_priority(self):
        return 0

    def execution_probability(self, bet_log):
        return 1.0

    def place_bet(self, bet_log) -> bet.Betting:
        """
            bet_log is a param which contains BettingResults

            must return Betting object or None
            None means not bet
        """
        raise NotImplementedError("please write the place_bet function")

    def after_bet(self, bet_result: bet.BettingResult):
        colors = ["\033[31m", "\033[32m"]
        select = colors[0]
        if bet_result.profit > 0:
            select = colors[1]
        self.total_profit += bet_result.profit

        print(select, end="")
        print("roll:", bet_result.roll,
              "target:", bet_result.target,
              "profit:", "{0:.8f}".format(bet_result.profit),
              "total_profit:", "{0:.8f}".format(self.total_profit))
        print("\033[0m", end="")


class CrisisDetectHandler(CryptoHandler):
    def __init__(self, recent_count, under, over, limit, betting):
        self.recent_count = recent_count
        self.under = under
        self.over = over
        self.limit = limit
        self.betting = betting

    def get_priority(self):
        return 99

    def execution_probability(self, bet_log):
        if len(bet_log) < 1:
            return 0
        count = 0
        for re in range(0, min(len(bet_log), self.recent_count)):
            if bet_log[re].roll <= self.under or bet_log[re].roll >= self.over:
                count += 1
        if count >= self.limit:
            return 1
        return 0

    def place_bet(self, bet_log):
        return self.betting


class TwiceStrategyHandler(CryptoHandler):
    def __init__(self, min_bet, max_bet, times):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.times = times

    def get_priority(self):
        return 100

    def execution_probability(self, bet_log):
        if len(bet_log) <= 0:
            return 0

        if bet_log[0].profit <= 0:
            return 1
        return 0

    def place_bet(self, bet_log):
        p_betting = copy.deepcopy(bet_log[0].betting)
        p_betting.under_over = random.choice([True, False])
        p_betting.payout = self.times
        p_betting.bet = -bet_log[0].profit * self.times

        if p_betting.bet >= self.max_bet:
            return None

        return p_betting

