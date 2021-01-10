from discord.ext import commands
import os
from pycoingecko import CoinGeckoAPI

bot = commands.Bot(command_prefix='$')
cg = CoinGeckoAPI()

def build_coins_dict(coins_list):
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
    "xrp" : "xrp",
    "aave" : "aave"
  }

  # Fill in everything else. If it's already there, skip it.
  for coin in coins_list:
    symbol = coin['symbol']
    if symbol not in d.keys():
      d[symbol] = coin['id']
    else:
      print('warning: {0} is already mapped to {1}, cannot be used for {2}'.format(symbol, d[symbol], coin['id']))

  return d

coins_dict = build_coins_dict(cg.get_coins_list())

def get_price(id, currency='usd'):
  return cg.get_price(ids=id, vs_currencies=currency)[id][currency]

@bot.event 
async def on_ready():
    print('Logged in as {0.user.name}'.format(bot))

@bot.command(brief="Gets the price of a coin.")
async def price(ctx, sym):
  if sym in coins_dict.keys():
    price = get_price(coins_dict[sym])
    reply = '{0} price is ${1}'.format(sym, price)
  else:
    reply = "I don't know %s" % sym
  await ctx.message.reply(reply)

@bot.command(brief="Gets the price ratio of two coins.")
async def ratio(ctx, sym1, sym2):
  if sym1 in coins_dict.keys():
    if sym2 in coins_dict.keys():
      price1 = get_price(coins_dict[sym1])
      price2 = get_price(coins_dict[sym2])
      ratio = price1 / price2
      reply = '1 {0} is {1} {2}'.format(sym1, ratio, sym2)
    else:
      reply = "I don't know %s" % sym2
  else:
    reply = "I don't know %s" % sym1
  await ctx.message.reply(reply)

bot.run(os.getenv('TOKEN'))