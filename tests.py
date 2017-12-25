from crypto_games.base import CryptoGames
from crypto_games.looper import Looper
from crypto_games.bet import Betting

default = Betting(coin_kind="BTC",
                  bet=0.00000001,
                  payout=1.1,
                  under_over=False,
                  client_seed=None)

mylooper = Looper("secret_api_key", default)
mylooper.run()
