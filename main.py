import discord
import os
import asyncio

from dotenv import load_dotenv
from writeToSheets import recordNewPlaytester, checkNewPlaytester, findSteamKey, needMoreKeys, rainCheckKey, whoNeedsKeys
from datetime import date, datetime

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)

noKeys = False
guild_id = 775937500643721218 # server id

async def playtestCommand(message):
    user = message.author

    if (checkNewPlaytester(user.name + '#' + user.discriminator) == False):
        return await user.send("It looks like you've already joined the Guild, " + user.name + ".")

    role_id = 780498456938545242 # playtester role id
    user_answers = [datetime.now().strftime("%m/%d/%Y %H:%M"), user.name + '#' + user.discriminator]
    opening = "Hello, traveller! Welcome to the Guild.\nIn this dark time, we're happy to have more allies.\nBut, before we can give you a key, you must answer some questions."
    user_timeout_msg = "I see you're still unsure of whether to join or not. Come again when you're ready.\n"
    closing = "You'll be a powerful ally, " + user.name + ". We take pride in you joining us. Here's your key: \n"
    noKeys = "We're out of keys right now, but we'll get yer one as soon as we can. Look out for a raven, it'll deliver it to ya."
    steam_activation_instructons = "(For activating instructions: https://support.steampowered.com/kb_article.php?ref=5414-tfbn-1352)"
    
    questions = [
        'First, a simple question. Have you wishlisted "Kill the King?" (https://store.steampowered.com/app/1537280/Kill_the_King/)',
        'Next, what aspect of "Kill the King" is most exciting to you?',
        'Last, how did you find out about "Kill the King"?'
    ]

    await user.send(opening)

    # Ask questions and save responses
    for question in questions:
        def user_responded(m):
            return m.author == user

        await user.send(question)

        try:
            a = await client.wait_for('message', check=user_responded, timeout=300.0)
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
        if steam_key == None:
            await user.send(noKeys)
        else:    
            await user.send(closing + steam_key)
            await user.send(steam_activation_instructons)
    except discord.HTTPException:
        print("didn't work")
        pass

async def resendSteamKey(message):
    noKeys = "We're out of keys right now, but we'll get yer one as soon as we can. Look out for a raven, it'll deliver it to ya."
    user = message.author
    key = findSteamKey(user.name + '#' + user.discriminator)
    
    if key == None:
        await user.send("Looks like you'll have to join the Guild first. Try using !playtest.")
    elif key == "unavailable":
        await user.send(noKeys)
    else:
        await user.send("Aye, " + user.name + ", don't go around misplacing this. Ya never know who might steal it.\nKey: " + key)


async def needKeys():
    # QuantumBois channel = 750884937531523162
    while True:
        print("beep boop")
        noKeys = needMoreKeys()
        if noKeys == True:
            moo = client.get_user(150477278709678080)
            await moo.send('Need more keys')
        else:
            user_list = whoNeedsKeys()
            guild = client.get_guild(guild_id)
            for user in user_list:
                key = rainCheckKey(user)
                if key != None:
                    msg = guild.get_member_named(user)
                    await msg.send("We found a key for you! Thank you for joining us!\nKey: " + key)
        await asyncio.sleep(3600)


@client.event
async def on_ready():
    print('We are the Swarm')
    await needKeys()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('!playtest'):
        await playtestCommand(message)
    elif message.content == ('!key'):
        await resendSteamKey(message)


client.run(os.environ.get('TOKEN'))

