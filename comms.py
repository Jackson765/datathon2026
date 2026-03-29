import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import time
import sys
import time

# Load environment variables from .env file
load_dotenv()

# Access the variables
botKey = os.getenv("KEY")
channelID = os.getenv("CHANNEL")

cooldown = False
dangerTime = 0
# 1. Setup Intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
dangerValue = 0
dangerOfc = -1

async def inDanger():
    print(f'Logged in as {bot.user}')
    
    channel = bot.get_channel(int(channelID))
    
    if channel:
        file = discord.File("frame.jpg") 
        dangerString = ""
        if (dangerOfc == 1):
            dangerString = "Choking"
        if (dangerOfc == 2):
            dangerString = "Fell"
        if (dangerOfc == 3):
            dangerString = "Stroke"
        await channel.send("Someone is in danger: " + dangerString + "! ⚠️😬💀", file=file)

@bot.event
async def on_ready():
    global dangerValue, cooldown, dangerTime
    print("bot ready")
    cooldown = False
    while (True):
        if (dangerTime <= time.time()):
            cooldown = False
        if (dangerValue >= 10 and cooldown == False):
            print("Danger recieved")
            dangerValue = 0
            dangerTime = time.time() + 3
            cooldown = True
            await inDanger()
        await asyncio.sleep(1) 

def setDanger(dangerDecision):
    global dangerValue, dangerOfc
    dangerValue += 1
    dangerOfc = dangerDecision

def setDangerToZero():
    global dangerValue
    if (dangerValue > 0):
        dangerValue -= 1

def runBot():
    bot.run(botKey)