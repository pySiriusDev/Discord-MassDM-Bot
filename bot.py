import discord
from discord.ext import commands
from discord import errors as error
from rgb import rgbprint as printc
from rgb import colorize as cor
from os import system
from time import sleep
from random import randrange as rng
from datetime import datetime
import json

system('cls')

# Configuration
token = 'OTY2NTM0MzgxMjkwMjcwNzQw.YmDJSQ.2VTP9e8RrjoWRzT6VpyYeFxXi_c'
prefix = 'sb.'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
msg = 'Oi bb, que tal trabalhar em casa ganhando mais de 400 reais por semana, hein? 😈\nTopa? Então entra nesse servidor aqui 💕\nhttps://media.discordapp.net/attachments/937898760095293460/937907459111145552/GIF-220131_235303.gif\nhttps://discord.gg/EsBCDq8JKN'
dt = datetime.now()
dtFormated = dt.strftime('%d/%m/%Y - %H:%M')
taskID = ''

# Color Pallete
green = '#0df246'
red = '#e52e2e'
blue = '#4EC5F1'
yellow = '#ecf457'
l_red = '#ff6161'

@client.event
async def on_ready():
    printc('Bot is ready!', green)

@client.command(name='dm')
async def dm(ctx, x):
    # Update the taskID
    with open('task.json') as config:
        taskID = json.load(config)['taskID']
    taskIDup = taskID+1
    data = {
        "taskID":taskIDup
    }
    with open('task.json', 'w') as config:
        json.dump(data, config)

    # Scrap the channel name and message author name
    for channel in ctx.guild.text_channels:
        async for message in channel.history(limit=1, oldest_first=None):
            if (prefix+'dm' in message.content):
                channelName = channel.name
                cmd_author = message.author
    cmd_info = f'Command [{prefix + ctx.command.name} {x}] used.\nServer: {ctx.guild.name}\nChannel: {channelName}\nDate: {dtFormated}\nTask ID: {taskIDup}\n'
    cmd_info2 = f'**Command [{prefix + ctx.command.name} {x}] used.**\n**Server:** {ctx.guild.name}\n**Channel: **{channelName}\n**Date: **{dtFormated}\n**Task ID: **{taskIDup}\n'
    printc(cmd_info, blue)
    await cmd_author.send(content='>>> '+cmd_info2)
    i = 0
    if (x == 'all'):
        y = 9999999
    else:
        y = int(x)

    # Send dm to all members out of blacklist.txt and adds the new received in blacklist.txt
    try:
        members = ctx.guild.fetch_members()
        async for member in members:
            if (i < y):
                memberBL = False
                if (member.bot == False):
                    with open('Input/blacklist.txt', 'r') as file:
                        blacklist = file.readlines()
                        for line in blacklist:
                            if (str(member.id) in line):
                                memberBL = True
                                printc(f'[{member}] is on the blacklist!', l_red)
                    if (memberBL == False):
                        try:
                            await member.send(content=member.mention+'\n'+msg)
                            printc(f'[{member}] - Message sent!', green)
                            await cmd_author.send(content='**['+member.discriminator+']** - Message sent!')
                            i += 1
                            with open('Input/blacklist.txt', 'a') as bl:
                                try:
                                    bl.write(str(member.id)+'\n')
                                    printc('⮡ Member added to blacklist', blue)
                                    await cmd_author.send(content='**⮡ Member added to blacklist**')
                                except:
                                    printc(f'⮡ Error adding member to blacklist', l_red)
                                    await cmd_author.send(content='**⮡ Error adding member to blacklist**')
                        except error.Forbidden as fe:
                            printc(f'(Error code: {fe.code}) | You don\'t have permission to send DMs!', yellow)
                        except error.HTTPException as httpe:
                            printc(f'(Error code: {httpe.code}) | [{member}] - Error sending message!', red)
                        except:
                            printc('Unknown error!', red)
                        sleep(rng(3,10))
                if (i == 29):
                    sleep(600,900)
            else:
                return
    except:
        printc('Error scraping members!', red)
        return
    printc(f'\n⮡ Task [{taskIDup} by: {cmd_author}] ended!\n', green)
    await cmd_author.send(content='**⮡ Task ['+str(taskIDup)+' by: '+cmd_author.discriminator+'] ended!**')

client.run(token)