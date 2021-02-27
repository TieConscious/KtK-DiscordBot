import discord
import os
import asyncio

from dotenv import load_dotenv
from writeToSheets import getNewestPlaytesters, findSteamKey
from datetime import date, datetime

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)

guild_id = 775937500643721218 # server id


@client.event
async def on_ready():
    print('We are the Swarm')
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('!#resendKeys'):
        user_list = open("resendKeys.txt").read().splitlines()
        guild = client.get_guild(guild_id)
        for user in user_list:
            key = findSteamKey(user)
            msg = guild.get_member_named(user)
            try:
                await msg.send("Apologies, " + user + ", we're having some issues and wanted to make sure you got your key. If you happened to receive two of them, please DM CaptainBang.\nKey: " + key)
                print(user)
            except Exception as e:
                print("Error with " + user + ": " + str(e))

# try:
#     client.run(os.environ.get('LOCAL'))
#     print('local testing')
# except:
client.run(os.environ.get('TOKEN'))
print('deployed')