from moontracker.markets import *


def test_all_markets():
  markets = [BitfinexMarket, CoinbaseMarket, GdaxMarket, GeminiMarket]
  for Market in markets:
    mrkt = Market()
    mrkt.get_spot_price('btc-usd')


