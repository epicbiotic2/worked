import os
import discord
from discord.ext import commands
import random
import requests
import asyncio
from bs4 import BeautifulSoup
from datetime import timedelta
import threading
from googletrans import Translator

TOKEN = ('MTIzNjU1NDg3Njc2NzY5OTAxNQ.GNBN7t.A_aCs5GuCUIBYDwihrd2NLKPAVx-72drWMDeN4')

if TOKEN is None:
    print('Error: DISCORD_TOKEN environment variable not found.')
    exit()

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)
translator = Translator()
helpers = [1003183616232280135, 870681645328531477, 630545094789038108]
owner = [1003183616232280135]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
        try:
            detected_language = translator.detect(message.content[len(client.command_prefix):]).lang
            if detected_language!= 'en':
                translated_message = translator.translate(message.content[len(client.command_prefix):], dest='en').text
                author_display_name = translator.translate(message.author.display_name, dest='en').text
                await message.channel.send(f"{author_display_name}: {translated_message}")
            else:
                await client.process_commands(message)
        except translator.exceptions.RequestError as e:
            print(f"Translator request error: {e}")
        except translator.exceptions.LanguageDetectionError as e:
            print(f"Language detection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



@client.command()
@commands.check(lambda ctx: ctx.author.id in helpers)
async def tag(ctx, user: discord.Member, times: int, *, msg: str = ''):
    await ctx.message.delete()
    """Tags a user multiple times."""
    if times is None or times > 5:
        await ctx.send("You must provide a number between 1 and 5 for the number of times to tag the user!")
        return
    for i in range(times):
        await ctx.send(f"{user.mention} {msg}" if msg else user.mention)


@client.command()
@commands.check(lambda ctx: ctx.author.id in owner)
async def teg(ctx, user: discord.Member,times: int = None, *,msg: str = ''):
    await ctx.message.delete()
    """Tags a user multiple times."""
    if times is None:
        await ctx.send("You must provide the number of times to tag the user!")
        return
    for i in range(times):
        await ctx.send(f"{user.mention} {msg}" if msg else user.mention)




@client.command()
async def rxn(ctx):
    correct_emoji = random.choice(['👍', '👎', '😂', '😢', '👏', '😴'])
    message = await ctx.send(f'Get ready...')
    await asyncio.sleep(1)
    await message.edit(content=f'Get ready in 2...')
    await asyncio.sleep(1)
    await message.edit(content=f'React to this message to win!')
    for emoji in ['👍', '👎', '😂', '😢', '👏', '😴']:
        await message.add_reaction(emoji)

    disqualified_users = set()

    def early_reaction_check(reaction, user):
        return user!= client.user

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=2.0, check=early_reaction_check)
        disqualified_users.add(user)
    except asyncio.TimeoutError:
        pass

    await ctx.send(f'The emoji you have to react is...')
    await asyncio.sleep(0.5)
    await ctx.send(f'The correct emoji is {correct_emoji}')

    def check(reaction, user):
        return user!= client.user and user not in disqualified_users and str(reaction.emoji) == correct_emoji

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="Reaction Game", description="No one reacted in time!", color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Reaction Game", description=f"Congratulations, {user.mention}! You were the first to react with the correct emoji! The correct emoji was {correct_emoji}", color=discord.Color.random())
        await ctx.send(embed=embed)


@client.command()
async def coinflip(ctx):
    side = random.choice(['heads', 'tails'])
    await ctx.send(f'**Coin Flip:** {side}')

#ping you getting ig
@client.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''
    latency = round(client.latency, 2)
    await ctx.send(f'{ctx.message.author.mention} - Pong!!!:softball: ->>> `{latency}`ms')

@client.event
async def on_message(message):
    # If the bot is mentioned in the message, respond with a custom message
    if client.user.mentioned_in(message):
        owner_id = helpers
        if message.author.id in owner_id:
            sweet_messages = [
                "Aww, thanks for pinging me, owner! :heart:",
                "Hi, owner! I'm here to help! :smile:",
                "What's up, owner? Need something? :wink:",
                "You're the best, owner! Thanks for checking in!",
                "Owner, you're amazing! I'm so glad you pinged me!",
                "Hey, owner! I've got your back! What do you need?",
                "Owner, you're the real MVP! Thanks for the ping!",
                "I'm all ears, owner! What's on your mind?"]
            respond = random.choice(sweet_messages)
        else:
            harsh_messages = [
                "Don't Ping me I am Busy!! :middle_finger:",
                ":middle_finger: :middle_finger: :middle_finger: :middle_finger:",
                "Why the Hell are you pinging Me?? :rage:",
                "Get Lost Out of here!!!!!!",
                "Can't you see I'm busy? Stop pinging me!",
                "What's your problem, dude? Can't you see I'm occupied?",
                "Ugh, stop pinging me! I'm not your personal assistant!",
                "Don't bother me with your pings, I'm not interested!",
                "Ping me again and I'll mute you!"]
            respond = random.choice(harsh_messages)

        embed = discord.Embed(
            title=respond,
            color=discord.Color.purple()
        )
        await message.channel.send(embed=embed)

    # Run the default on_message() event to handle commands and other events
    await client.process_commands(message)

client.run(TOKEN)
