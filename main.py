import discord
import os
import asyncio

from dotenv import load_dotenv
from writeToSheets import recordNewPlaytester
from datetime import date, datetime

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)


@client.event
async def on_ready():
    print('We are the Swarm')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('!playtest'):
        user = message.author
        role_id = 780498456938545242 # playtester role id
        guild_id = 775937500643721218 # server id
        user_answers = [datetime.now().strftime("%m/%d/%Y %H:%M"), user.name + '#' + user.discriminator]
        opening = "Hello, traveller! Welcome to the Guild.\nIn this dark time, we're happy to have more allies\nBut... before we can accept you, you must pass a test."
        user_timeout_msg = "I see you're still unsure of whether to join or not. Come again when you're ready.\n"
        closing = "I suppose you pass, " + user.name + "."

        questions = [
            'First, a simple question. Are you able to use SteamVR?',
            'Too easy I see.\nNext, what headset do you use with SteamVR?',
            'Last, how did you find out about "Kill the King"?'
        ]

        await user.send(opening)

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
        await user.send(closing)
        

        # assign playtester role
        guild = client.get_guild(guild_id)
        if guild is None:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        try:
            member = guild.get_member(user.id)
            await member.add_roles(role)
            recordNewPlaytester(user_answers)
        except discord.HTTPException:
            print("didn't work")
            pass

client.run(os.environ.get('TOKEN'))


