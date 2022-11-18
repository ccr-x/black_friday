# bot.py
import os

from discord.ext import commands
import discord
from dotenv import load_dotenv
import time

from black_friday_scraper import black_friday, stop_black_friday as sbf

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Sets prefix for the usable commands
client = commands.Bot(command_prefix='.', intents=discord.Intents.default())

# Checking the login of bot
@client.event
async def on_ready():
    """ Outputs message to console and logs channel when the bot is online"""
    print(f"Logged in as \n {client.user.name}\n {client.user.id}\n at {time.asctime()}\n ------")

    #channel = client.get_channel(844546291904413706)
    #content = f"Logged in as \n {client.user.name}\n {client.user.id}\n at {time.asctime()}\n ------"
    
    #await channel.send(content)

@client.command
async def start_black_friday():
    black_friday()

@client.command
async def stop_black_friday():
    sbf()


client.run(TOKEN)