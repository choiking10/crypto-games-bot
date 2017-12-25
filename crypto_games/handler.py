from . import bet


class CryptoHandler:
    def get_priority(self):
        return 0

    def execution_probability(self, bet_log):
        return 1.0

    def place_bet(self, bet_log) -> bet.Betting:
        """
            bet_log is a param which contains BettingResults

            None means not bet
            or
            must return Betting object
        """
        raise NotImplementedError("please write the place_bet function")

    def after_bet(self, bet_result):
        pass