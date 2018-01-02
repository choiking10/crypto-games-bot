import copy
import random

from .betting_info import Betting, BettingResult


class CryptoHandler:
    total_profit = 0

    def __init__(self, priority=0, probability=1.0):
        self.priority = priority
        self.probability = probability

    def get_priority(self):
        return self.priority

    def execution_probability(self, bet_log):
        return self.probability

    def place_bet(self, bet_log, budget) -> Betting:
        """
            bet_log is a param which contains BettingResults

            must return Betting object or None
            None means not bet
        """
        raise NotImplementedError("please write the place_bet function")

    def after_bet(self, bet_result: BettingResult, budget):
        colors = ["\033[31m", "\033[32m"]
        select = colors[0]
        if bet_result.profit > 0:
            select = colors[1]
        self.total_profit += bet_result.profit

        print(select, end="")
        print(type(self).__name__,
              "bet:", "{0:.8f}".format(bet_result.betting.bet),
              "roll:", bet_result.roll,
              "target:", bet_result.target,
              "profit:", "{0:.8f}".format(bet_result.profit),
              "total_profit:", "{0:.8f}".format(self.total_profit))
        print("\033[0m", end="")


class CrisisDetectHandler(CryptoHandler):
    def __init__(self, recent_count, under, over, limit, betting=None,
                 priority=99, probability=1.0):
        self.recent_count = recent_count
        self.under = under
        self.over = over
        self.limit = limit
        self.betting = betting
        super(CrisisDetectHandler, self).__init__(priority, probability)

    def execution_probability(self, bet_log):
        if len(bet_log) < 1:
            return 0
        count = 0
        for re in range(0, min(len(bet_log), self.recent_count)):
            if bet_log[re].roll <= self.under or bet_log[re].roll >= self.over:
                count += 1
        if count >= self.limit:
            return self.probability
        return 0

    def place_bet(self, bet_log, budget):
        return self.betting


class TwiceStrategyHandler(CryptoHandler):
    def __init__(self, min_bet, max_bet, times, priority=100, probability=1.0):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.times = times
        super(TwiceStrategyHandler, self).__init__(priority, probability)

    def execution_probability(self, bet_log):
        if len(bet_log) <= 0:
            return 0

        if bet_log[0].profit <= 0:
            return 1
        return 0

    def place_bet(self, bet_log, budget):
        p_betting = copy.deepcopy(bet_log[0].betting)
        p_betting.under_over = random.choice([True, False])
        p_betting.payout = self.times
        p_betting.bet = -bet_log[0].profit * self.times

        if p_betting.bet >= self.max_bet:
            return None

        return p_betting

