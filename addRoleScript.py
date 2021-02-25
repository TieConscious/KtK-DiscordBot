import discord
import os
import asyncio

from dotenv import load_dotenv
from writeToSheets import getNewestPlaytesters
from datetime import date, datetime

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)

guild_id = 775937500643721218 # server id
role_id = 780498456938545242 # playtester role id


@client.event
async def on_ready():
    print('We are the Swarm')
    non_user = []
    user_list = getNewestPlaytesters()
    guild = client.get_guild(guild_id)
    role = guild.get_role(role_id)
    for user in user_list:
        member = guild.get_member_named(user[0])
        if member == None:
            print("User not in server: " + user[0])
            non_user.append(user[0])
        else:
            if role not in member.roles:
                await member.add_roles(role)
                try:
                    await member.send("Welcome to the Guild, and thank you for joining us, " + member.name + ". You now have the playtester role.\nWe'll hopefully start the multiplayer testing next week, but if you'd like to see the original, prototype build of Kill the King, you can find it in the #ktk-playtesters channel under the pinned message.")
                    print("User now has playtester role: " + member.name)
                except:
                    print("User cannot receive messages: " + member.name)
                    continue
            else:
                print("User already has role: " + user[0])

    print('Completed adding Roles')

try:
    client.run(os.environ.get('LOCAL'))
    print('local testing')
except:
    client.run(os.environ.get('TOKEN'))
    print('deployed')