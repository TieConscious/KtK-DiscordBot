import discord
import os
import asyncio

from dotenv import load_dotenv
from writeToSheets import recordNewPlaytester, checkNewPlaytester, findSteamKey
from datetime import date, datetime

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)

async def playtestCommand(message):
    user = message.author

    if (checkNewPlaytester(user.name + '#' + user.discriminator) == False):
        return await user.send("It looks like you've already joined the Guild, " + user.name + ".")

    role_id = 780498456938545242 # playtester role id
    guild_id = 775937500643721218 # server id
    user_answers = [datetime.now().strftime("%m/%d/%Y %H:%M"), user.name + '#' + user.discriminator]
    opening = "Hello, traveller! Welcome to the Guild.\nIn this dark time, we're happy to have more allies.\nBut, before we can give you a key, you must answer some questions."
    user_timeout_msg = "I see you're still unsure of whether to join or not. Come again when you're ready.\n"
    closing = "You'll be a powerful ally, " + user.name + ". We take pride in you joining us. Here's your key: "

    questions = [
        'First, a simple question. Are you able to use SteamVR?',
        'Next, what headset do you use with SteamVR?',
        'Last, how did you find out about "Kill the King"?'
    ]

    await user.send(opening)

    # Ask questions and save responses
    for question in questions:
        def user_responded(m):
            return m.author == user

        await user.send(question)

        try:
            a = await client.wait_for('message', check=user_responded, timeout=45.0)
        except asyncio.TimeoutError:
            return await user.send(user_timeout_msg)
        
        if a:
            user_answers.append(a.content)
        else:
            return await user.send(user_timeout_msg)

    print(user_answers)

    # Assign playtester role and record answers to GSheets
    guild = client.get_guild(guild_id)
    if guild is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    try:
        member = guild.get_member(user.id)
        await member.add_roles(role)
        steam_key = recordNewPlaytester(user_answers)
        await user.send(closing + steam_key)
    except discord.HTTPException:
        print("didn't work")
        pass

async def resendSteamKey(message):
    user = message.author
    key = findSteamKey(user.name + '#' + user.discriminator)
    if key == None:
        await user.send("Looks like you'll have to join the Guild first. Try using !playtest.")
    else:
        await user.send("Aye, " + user.name + ", don't go around misplacing this. Ya never know who might steal it.\nKey: " + key)

@client.event
async def on_ready():
    print('We are the Swarm')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('!playtest'):
        await playtestCommand(message)
    elif message.content == ('!key'):
        await resendSteamKey(message)


client.run(os.environ.get('TOKEN'))


