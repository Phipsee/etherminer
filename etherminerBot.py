import discord
from discord.ext import commands, tasks
import etherminerAPI
import globals
from itertools import cycle
import logging
import os

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.join(
    os.path.dirname(__file__), 'test.log'), 'w', 'utf-8')
root_logger.addHandler(handler)

HEX_MINER = globals.TOKEN_HEX_MINER
BOT_TOKEN = globals.TOKEN_DISCORD_BOT

client = commands.Bot(command_prefix='.')

client.used_channel = 0


@ client.event
async def on_ready():
    logging.info('Bot is ready.')
    game = discord.Game("Ethercraft")
    await client.change_presence(status=discord.Status.online, activity=game)
    logging.info('finished init')
    minerInfo.start()


@ client.command(aliases=['MARCO', 'Marco'])
async def marco(ctx):
    await ctx.send('POLO!')


@ client.command(aliases=['Hello there!'])
async def hello(ctx):
    alija_id = '<@348811957614411776>'
    await ctx.send('General %s' % alija_id)


@ client.command(aliases=['useThis'])
async def useMeDaddy(ctx):
    client.used_channel = ctx.channel.id
    client.used_guild = ctx.guild.id
    etherminerAPI.doSaveChannelGuild(ctx.guild.id, ctx.channel.id)
    await ctx.send('Now using this channel for rich bitch notifications.')


@ tasks.loop(seconds=60*60)
async def minerInfo():
    logging.info('invoked minerInfo')
    msg = etherminerAPI.get_info(HEX_MINER)

    for ch in etherminerAPI.doRetrieveChannels():
        logging.info(ch)
        channel = client.get_channel(ch)
        if (channel == None):
            continue

        await channel.send(msg)


client.run(BOT_TOKEN)
