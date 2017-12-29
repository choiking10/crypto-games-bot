
from crypto_games.looper import Looper
from crypto_games.betting_info import Betting
from YHbot.handler import MyHandler, KooHandler

default = Betting(coin_kind="BTC",
                  bet=0.00000001,
                  payout=1.15,
                  under_over=False,
                  client_seed=None)

while True:
    mylooper = Looper("secret",
                      default, 0.00001000)
    mylooper.add_handler(KooHandler(coin_kind="BTC", base_rate=0.01))
    try:
        mylooper.run()
    except BaseException as e:
        print(e)
