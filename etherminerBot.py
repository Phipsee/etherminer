import discord
from discord.ext import commands, tasks
import etherminerAPI
from itertools import cycle


HEX_MINER = '#####token####'
BOT_TOKEN = '####bottoken###'

client = commands.Bot(command_prefix='.')

client.used_channel = 0


@client.event
async def on_ready():
    print('Bot is ready.')
    game = discord.Game("Ethercraft")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('finished init')


@client.command(aliases=['MARCO', 'Marco'])
async def marco(ctx):
    await ctx.send('POLO!')


@client.command(aliases=['Hello there!'])
async def hello(ctx):
    await ctx.send('General @Rehkitz')


@client.command(aliases=['useThis'])
async def useMeDaddy(ctx):
    client.used_channel = ctx.channel.id
    await ctx.send('Now using this channel for rich bitch notifications.')
    minerInfo.start()


@tasks.loop(seconds=10)
async def minerInfo():
    print('invoked minerInfo')
    if client.used_channel == 0:
        print('no valid channel '+str(client.used_channel))
        return
    channel = client.get_channel(client.used_channel)
    print(client.used_channel)
    msg = etherminerAPI.get_info(HEX_MINER)

    await channel.send(msg)


client.run(BOT_TOKEN)
