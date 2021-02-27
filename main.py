import discord
import os
import asyncio
import sys

from dotenv import load_dotenv
from writeToSheets import recordNewPlaytester, checkNewPlaytester, findSteamKey, needMoreKeys, rainCheckKey, whoNeedsKeys
from datetime import date, datetime, timedelta

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(prefix='!',intents=intents)

noKeys = False
guild_id = 775937500643721218 # server id
playtest_signup = 781353033467559946

async def playtestCommand(message):
    user = message.author

    if (checkNewPlaytester(user.name + '#' + user.discriminator) == False):
        return await user.send("It looks like you've already joined the Guild, " + user.name + ".")

    if message.channel.id == playtest_signup:
        dm = await user.send("Excuse me for a moment...")
    else:
        dm = message
    
    async for check in dm.channel.history(limit=5,before=dm):
        if check.author == user and check.content == "!playtest" and check.created_at > datetime.utcnow() - timedelta(minutes=10):
            print(check.created_at)
            print(datetime.utcnow() - timedelta(minutes=10))
            return 

    role_id = 780498456938545242 # playtester role id
    user_answers = [datetime.now().strftime("%m/%d/%Y %H:%M"), user.name + '#' + user.discriminator]
    opening = "Hello, traveller! Welcome to the Guild.\nIn this dark time, we're happy to have more allies.\nBut, before we can give you a key, you must answer some questions."
    user_timeout_msg = "I see you're still unsure of whether or not to join. Come again when you're ready.\n"
    closing = "You'll be a powerful ally, " + user.name + ". We take pride in you joining us. Here's your key: \n"
    noKeys = "We're out of keys right now, but we'll get ye' one as soon as we can. Thanks for waitin'."
    steam_activation_instructons = "(For activating instructions: https://support.steampowered.com/kb_article.php?ref=5414-tfbn-1352)"
    
    questions = [
        'First, a simple question. Have you wishlisted "Kill the King?" (https://store.steampowered.com/app/1537280/Kill_the_King/)',
        'Next, what aspect of "Kill the King" is most exciting to you?',
        'Last, how did you find out about "Kill the King"?'
    ]

    dm = await user.send(opening)

    # Ask questions and save responses
    for question in questions:
        def user_responded(m):
            return m.author == user and m.channel.id == dm.channel.id and m.content != "!playtest"

        await user.send(question)

        try:
            a = await client.wait_for('message', check=user_responded, timeout=180.0)
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


async def trollUser(message):
    user = message.author
    count = 0
    async for check in message.channel.history(limit=20,before=message):
        if check.author == user and check.created_at > datetime.utcnow() - timedelta(minutes=1):
            count += 1
    if count >= 10:
        return await user.send("Oy, if you keep spamming me, I'm going to have to test the physics on this BAN HAMMER.")
    return await user.send("If you don't need anything from me, go bother Quentin or CaptainBang.")


async def needKeys():
    # QuantumBois channel = 750884937531523162
    while True:
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
                    try:
                        await msg.send("We found a key for you! Thank you for joining us!\nKey: " + key)
                        print(user + " : " + key)
                    except:
                        print("Error")
        await asyncio.sleep(3600)


@client.event
async def on_ready():
    print('We are the Swarm')
    


@client.event
async def on_message(message):
    # playtest-signup channel id == 781353033467559946
    signup_channel = playtest_signup
    if message.author == client.user:
        return

    if message.content == ('!playtest') and (message.channel.type is discord.ChannelType.private or message.channel.id == signup_channel):
        await playtestCommand(message)
    elif message.content == ('!#givepeoplekeys'):
        await needKeys()
    elif message.content == ('!key'):
        await resendSteamKey(message)
    # elif message.channel.type is discord.ChannelType.private:
    #     await trollUser(message)
    

def main():
    # if "LOCAL" in os.environ:
    #     print('local testing')
    #     client.run(os.environ.get('LOCAL'))
    # else:
        print('hosted')
        client.run(os.environ.get('TOKEN'))

if __name__ == "__main__":
    main()