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
        channel = message.channel
        await channel.send("Emoji Bot Commands:\n")
        await channel.send("!reacts #channel_nameA, #channel_nameB, etc.: View number of reacts for each react in #channel_nameA, #channel_nameB, etc.; defaults to current channel if no #channel_names are included.")
        await channel.send("!react_king #channel_name: view message in #channel_name with most total reacts and see number of reacts for each react in message; defaults to current channel if no #channel_name is included.")
    elif command == "!reacts":
        # Get reacts for each channel mentioned
        if len(message.channel_mentions) > 0:
            count = 0
            currChannel = message.channel
            for mention in message.channel_mentions:
                channel = mention
                try: 
                    # await channel.send("Tallying up reacts is hard work.")
                    async for message in channel.history(limit=None):
                        for react in message.reactions:
                            count += 1
                            if react in channel_reacts:
                                channel_reacts[react] += react.count
                            else:
                                channel_reacts[react] = react.count
                    if count == 0:
                        await currChannel.send("There are no reacts in this channel! \U0001F62E")
                    else:
                        printCount = 0
                        content = ""
                        for react in channel_reacts.keys():
                            printCount += channel_reacts[react]
                            content += str(react) + ": " + str(channel_reacts[react])
                            if printCount < count:
                                content += " | "

                        await currChannel.send(str(channel) + " - " + content + "\n")
                except:
                    await currChannel.send("Error with accessing " + str(channel))
        # Default: get reacts for current channel
        else:
            count = 0
            channel = message.channel
            try:
                # await channel.send("Tallying up reacts is hard work.")
                async for message in channel.history(limit=None):
                    for react in message.reactions:
                        count += 1
                        if react in channel_reacts:
                            channel_reacts[react] += react.count
                        else:
                            channel_reacts[react] = react.count
                if count == 0:
                    await channel.send("There are no reacts in this channel! \U0001F62E")
                else:
                    printCount = 0
                    content = ""
                    for react in channel_reacts.keys():
                        printCount += channel_reacts[react]
                        content += str(react) + ": " + str(channel_reacts[react])
                        if printCount < count:
                            content += " | "

                    await channel.send(str(channel) + " - " + content)
            except:
                await currChannel.send("Error with accessing " + str(channel) + ".")
    elif command == "!react_king":
        # all_channels = message.guild.text_channels
        current_channel = message.channel
        # Specified channel
        if len(message.channel_mentions) == 1:
            channel = message.channel_mentions[0]
            total_message_reacts = {}
            reactExists = False
            async for message in channel.history(limit=None):
                numReacts = 0
                for react in message.reactions:
                    numReacts += react.count
                total_message_reacts[message] = numReacts
                if numReacts > 0:
                    reactExists = True

            if reactExists is True:
                message = max(total_message_reacts, key=total_message_reacts.get)
                content = "MESSAGE - " + str(message.content) + "\n" + "BY - " + str(message.author.nick) + "\n" + "REACTS - "
                reacts = message.reactions
                count = total_message_reacts[message]
                
                printCount = 0
                for react in reacts:
                    printCount += react.count
                    content += str(react.emoji) +  ": " + str(react.count)
                    if printCount < count:
                        content += " | "
                await current_channel.send(content)
            else:
                await current_channel.send("There are no reacts in this server! \U0001F62E")
        # Default channel
        elif len(message.channel_mentions) == 0:
            total_message_reacts = {}
            reactExists = False
            async for message in current_channel.history(limit=None):
                numReacts = 0
                for react in message.reactions:
                    numReacts += react.count
                total_message_reacts[message] = numReacts
                if numReacts > 0:
                    reactExists = True

            if reactExists is True:
                message = max(total_message_reacts, key=total_message_reacts.get)
                content = "MESSAGE: " + str(message.content) + "\n" + "BY: " + str(message.author.nick) + "\n" + "REACTS: "
                reacts = message.reactions
                count = total_message_reacts[message]
                
                printCount = 0
                for react in reacts:
                    printCount += react.count
                    content += str(react.emoji) +  ": " + str(react.count)
                    if printCount < count:
                        content += " | "
                await current_channel.send(content)
            else:
                await current_channel.send("There are no reacts in this server! \U0001F62E")
        else:
            await channel.send("Specify one channel or leave blank (default to current channel)")


            

            

    
       


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
