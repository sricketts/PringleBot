from discord.ext import commands
import discord
import os
from collections import defaultdict
from keep_alive import keep_alive
from replit import db
import coins

bot = commands.Bot(command_prefix='$')

coinPrices = coins.CoinPrices()

@bot.event 
async def on_ready():
    print('Logged in as {0.user.name}'.format(bot))

@bot.command(brief="Gets the price of a coin.")
async def price(ctx, sym):
  price = coinPrices.get_price(sym)
  if price is not None:
    reply = '{0} price is ${1}'.format(sym, price)
  else:
    reply = "I don't know %s" % sym
  await ctx.message.reply(reply)

@bot.command(brief="Gets the price ratio of two coins.")
async def ratio(ctx, sym1, sym2):
  price1 = coinPrices.get_price(sym1)
  price2 = coinPrices.get_price(sym2)
  if price1 is not None:
    if price2 is not None:
      ratio = price1 / price2
      reply = '1 {0} is {1} {2}'.format(sym1, ratio, sym2)
    else:
      reply = "I don't know %s" % sym2
  else:
    reply = "I don't know %s" % sym1
  await ctx.message.reply(reply)

@bot.command(brief="Gets the top poster leaderboard for this channel.")
async def top(ctx):
  limit = 100
  count = defaultdict(int)
  async for message in ctx.channel.history(limit=limit):
    count[message.author.name] += 1
  reply = "```\n"
  reply += "Top authors in this channel over the last %d messages:\n\n" % limit
  rank = 1
  for author in sorted(count, key=count.get, reverse=True):
    reply += "%d. %s: %s\n" % (rank, author, count[author])
    rank += 1
  reply += "```"
  print(reply)
  await ctx.message.reply(reply)

HALL_OF_FAME_THRESH = 10
HALL_OF_FAME_CHAN_NAME = "hall-of-fame"

# This could break if we try to run this on multiple discord servers at the same time,
# because message IDs might collide.
def update_hof_db(msg_id):
  if "hof" in db.keys():
    hof = db["hof"].append(msg_id)
    db["hof"] = hof
  else:
    db["hof"] = [msg_id]

def already_hof(msg_id):
  if "hof" in db.keys():
    return msg_id in db["hof"]
  else:
    return False

@bot.event
async def on_reaction_add(reaction, user):
  msg = reaction.message
  if len(msg.reactions) >= HALL_OF_FAME_THRESH:
    if not already_hof(msg.id):
      update_hof_db(msg.id)
      ctx = await bot.get_context(msg)
      channel = discord.utils.get(ctx.guild.channels, name=HALL_OF_FAME_CHAN_NAME)
      credit = "hall-of-fame message by %s in channel %s" % (msg.author.mention, msg.channel.mention)
      await channel.send(credit + ": " + msg.jump_url)

keep_alive()

bot.run(os.getenv('TOKEN'))