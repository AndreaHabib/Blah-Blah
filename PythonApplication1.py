import discord
import youtube_dl
import asyncio
import threading
import re
from random import randint
from time import gmtime, strftime
from discord.ext.commands import Bot
import random
from discord import Game
from discord import Emoji, Message
from discord.voice_client import VoiceClient
BOT_PREFIX = ("?", "!")
TOKEN = "token"
client = Bot(command_prefix=BOT_PREFIX)
#client = discord.Client()
#channel = client.get_channel("id")
@client.command(name = 'test', description = 'Only for test purposes', brief = 'Test', pass_context = True)
async def test(context):
   possible_responses = [
       'Test', 'Testing', 'Hey', 'Nice'
       ]
   await client.say(random.choice(possible_responses) + " " + context.message.author.mention)
@client.command(name = 'kick', description = 'To kick someone', brief = 'Kick', pass_context = True)
async def kick(ctx, member : discord.User, *, reason = None):
    await client.kick(member)
    await client.say("KICKED!")
@client.command(name = 'ban', description = 'To ban someone', brief = 'Ban', pass_context = True)
async def ban(ctx, member : discord.User, *, reason = None):
    await client.ban(member)
    await client.say("BANNED!")
@client.command(name = 'unban', description = 'To unban someone', brief = 'Unban', pass_context = True)
async def unban(ctx, *, member):
    ban_list = await client.get_bans(ctx.message.server)
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
        await client.say("Ban list is empty.")
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say("Unbanned user: `{}`".format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say("I do not have permission to unban.")
        return
    except discord.HTTPException:
        await client.say("Unban failed.")
        return
@client.command(pass_context = True, brief = 'To clear messages')
async def clear(ctx, msglimit : int):
        deleted = await client.purge_from(ctx.message.channel, limit=msglimit)
        await client.say("Cleared **{}** Messages".format(len(deleted)))
@client.command(pass_context = True, brief = 'change nickname')
async def nickname(ctx, member : discord.User, nickname):
    await client.change_nickname(member, nickname)
@client.command(pass_context = True)
async def join(ctx):
    channel = client.get_channel("id")
    await client.join_voice_channel(channel)
@client.command(pass_context = True)
async def leave(ctx):
    channel = client.get_channel("id")
    print("Sorry, it takes me a while to leave!")
    server = ctx.message.server
    voice_client = await client.join_voice_channel(channel)
    await voice_client.disconnect()
@client.command(pass_context = True)
async def play(ctx, url):
    voice_channel = ctx.message.author.voice.voice_channel
    voice_client = await client.join_voice_channel(voice_channel)

    url = 'https://www.youtube.com/watch?v=7ysFgElQtjI'
    player = await voice_client.create_ytdl_player(url)
    player.start()

@client.event
async def on_ready():
    await client.change_presence(game=Game(name= "Joker", type=3)) #3 watch - 2 listen - 1 stream - 0 play
    print("-----------------------------------------")
    print("Logged in " + client.user.name)
    print("-----------------------------------------")

        
client.run(TOKEN)
