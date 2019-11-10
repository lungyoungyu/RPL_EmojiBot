import discord
from discord.ext import commands
import os
import sys
import random

client = commands.Bot(command_prefix='!')


# runs code when bot is ready
@client.event
async def on_ready():
    print('Bot is online and active')


# Use on_message so the bot runs on every message sent. Also checks if certain commands were entered
@client.event
async def on_message(message):

    # Splits user input by whitespace
    wholeString = message.content.split()
    command = wholeString[0]
    command = command.lower()

    channel_reacts = {}

    if command == "!help":
        await channel.send("Emoji Bot Commands:\n !reacts #channel_name: View number of reacts for each react in #channel_name, defaults to current channel if no #channel_name is included."
    elif command == "!reacts":
        # Default: get reacts for current channel
        channel = message.channel
        if len(message.channel_mentions) > 0:
            count = 0
            channel = message.channel

            channel = message.channel_mentions[0]

        # await channel.send("Tallying up reacts is hard work.")
        async for message in channel.history(limit=None):
            for react in message.reactions:
                count += 1
                if react in channel_reacts:
                    channel_reacts[react] += react.count
                else:
                    channel_reacts[react] = react.count
        if count == 0:
            await channel.send("The unimaginable is reality. There are no reacts in this channel!")
        else:
            printCount = 0
            content = ""
            for react in channel_reacts.keys():
                printCount += channel_reacts[react]
                content += str(react) + ": " + str(channel_reacts[react])
                if printCount < count:
                    content += " | "

            await channel.send(content)

       


# -------------------------------------------------------------------------------------------------------------
# Code to run before the discord bot goes online

# Give the location of the file
local = os.path.dirname(os.path.realpath(__file__))

# Reads token and server id from txt file
try:
    file = open(local + '/token.txt', 'r')
    info = file.readlines()
except:
    print("Cant find file \"" + local + "/token.txt\"")
    print("Either it doesnt exist or this program doesnt have permission to access it")
    sys.exit(0)

TOKEN = info[0].rstrip()
client.run(TOKEN) 
