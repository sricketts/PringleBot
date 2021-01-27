from pycoingecko import CoinGeckoAPI

class CoinPrices():

  def __init__(self):
    self.cg = CoinGeckoAPI()
    self.coins_dict = self.build_coins_dict(self.cg.get_coins_list())

  def build_coins_dict(self, coins_list):
    # Ticker symbols are not unique. But we want the user to 
    # be able to ask for a price based on ticker symbol. So we
    # initialize the dict with some protected mappings and then
    # fill in everything else in whatever order the list is in,
    # skipping any symbol we've already seen.

    # Initialize with mappings we know we want
    d = {
      "btc" : "bitcoin",
      "eth" : "ethereum",
      "yfi" : "yearn-finance",
      "xrp" : "ripple",
      "aave" : "aave",
      "uni" : "uniswap",
      "mir" : "mirror-protocol"
    }

    # Fill in everything else. If it's already there, skip it.
    for coin in coins_list:
      symbol = coin['symbol']
      if symbol not in d.keys():
        d[symbol] = coin['id']
      else:
        print('warning: {0} is already mapped to {1}, cannot be used for {2}'.format(symbol, d[symbol], coin['id']))

    return d

  def get_price(self, sym, currency='usd'):
    sym_lower = sym.lower()
    if sym_lower in self.coins_dict.keys():
      id = self.coins_dict[sym_lower]
      return self.cg.get_price(ids=id, vs_currencies=currency)[id][currency]
    else:
      return None