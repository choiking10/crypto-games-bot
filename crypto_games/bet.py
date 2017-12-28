
class Betting:
    def __init__(self, coin_kind, bet, payout, under_over, client_seed=None):
        self.coin_kind = coin_kind
        self.bet = bet
        self.payout = payout
        self.under_over = under_over
        self.client_seed = client_seed


class BettingResult:
    def __init__(self, data, betting=None):
        self.id = data["BetId"]
        self.roll = data["Roll"]
        self.target = data["Target"]
        self.profit = data["Profit"]
        self.server_seed = data["ServerSeed"]
        self.next_server_seed_hash = data["NextServerSeedHash"]
        self.betting = betting

    def __str__(self):
        return " ".join(["roll", str(self.roll),
                          "payout", str(self.betting.payout),
                          "profit", str(self.profit)])