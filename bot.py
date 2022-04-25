import aiohttp
import discord
from discord.ext import commands
from discord import errors as error
from discord import Embed, Webhook, AsyncWebhookAdapter
from rgb import rgbprint as printc
from os import system
from random import randint as rng
from datetime import datetime
import json
import asyncio
from decouple import config

system('cls')

# Configuration
TOKEN = config("TOKEN")
prefix = '.'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
MSG = config("MSG")
dt = datetime.now()
dtFormated = dt.strftime('%d/%m/%Y - %H:%M')
taskID = ''

# Color Pallete
green = '#0df246'
red = '#e52e2e'
l_red = '#ff6161'
blue = '#4EC5F1'
yellow = '#ecf457'
purple = '#D237D2'
d_purple = '#6e0386'

@client.event
async def on_ready():
    printc('Bot is ready!', green)

@client.command(name='dm')
async def dm(ctx, x, wurl):
    await ctx.message.delete(delay=0)

    dmsCount = 0

    logUrl = 'https://discord.com/api/webhooks/966726227366907974/nxEQkU7JegD3KLRtt3UWuR4CSN2z2MmubHE87DY15LVfxEJR_9VxXwGm32iQ2JppMLOO'

    # Update the taskID
    with open('task.json') as config:
        taskID = json.load(config)['taskID']
    taskIDup = taskID+1
    data = {
        "taskID":taskIDup
    }
    with open('task.json', 'w') as config:
        json.dump(data, config)

    cmd_info = f'Command [{prefix + ctx.command.name} {x}] used.\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\nDate: {dtFormated}\nTask ID: {taskIDup}\n'

    """ Start to create embeds """
    embed_cmd = Embed(
        title = f'Command used: {prefix+ctx.command.name} {x}',
        color = 0xD237D2
    )
    embed_cmd.set_author(
        name = 'Dev by: Sirius Beck (Gabriel Viana) | >>>  CONTACT ME HERE  <<<',
        icon_url = 'https://cdn.discordapp.com/emojis/958870691074179082.webp?size=128&quality=lossless',
        url = 'https://discord.gg/DyWxxK7NHM'
    )
    embed_cmd.add_field(
        name = '📋 Task ID',
        value = f'```{taskIDup}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '👤 User',
        value = f'```{ctx.author.name}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '🌍 Server',
        value = f'```{ctx.guild.name}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '🗨️ Channel',
        value = f'```{ctx.channel.name}```',
        inline = False
    )
    embed_cmd.set_footer(
        text = dtFormated
    )
    """ End embeds creation """

    printc(cmd_info, blue)

    # Configuring webook and sending embed message
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
        webhookLog = Webhook.from_url(logUrl, adapter=AsyncWebhookAdapter(session))
        await webhook.edit(name = "Sirius Bot")
        await webhook.send(embed=embed_cmd)
        await webhookLog.send(embed=embed_cmd)

    # Limiter for send DMs (parameter x)
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
                                # ! Member is on the blacklist log
                                printc(f'[{member}] is on the blacklist!', l_red)
                                embed = Embed(title=f'[{member.name}] is on the blacklist!', color=0xff6161)
                                async with aiohttp.ClientSession() as session:
                                    webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                    await webhook.send(embed=embed)
                                    
                    if (memberBL == False):
                        try:
                            await member.send(content=member.mention+'\n'+MSG)
                            # . Message sent log
                            printc(f'[{member}] - Message sent!', green)
                            embed = Embed(title=f'[{member.name}] - Message sent!', color=0x0df246)
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                await webhook.send(embed=embed)

                            i += 1
                            dmsCount += 1

                            with open('Input/blacklist.txt', 'a') as bl:
                                try:
                                    bl.write(str(member.id)+'\n')
                                    # . Member added to blacklist log
                                    printc('⮡ Member added to blacklist', blue)
                                    embed = Embed(description='⮡  Member added to blacklist', color=0x4EC5F1)
                                    async with aiohttp.ClientSession() as session:
                                        webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                        await webhook.send(embed=embed)
                                except:
                                    # ! Error while adding member to blacklist log
                                    printc(f'⮡ Error adding member to blacklist', l_red)
                                    embed = Embed(description='⮡  Error adding member to blacklist', color=0xff6161)
                                    async with aiohttp.ClientSession() as session:
                                        webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                        await webhook.send(embed=embed)
                        except error.Forbidden as fe:
                            # ! Error with permissions log
                            printc(f'(Error code: {fe.code}) | You don\'t have permission to send DMs!', yellow)
                            embed = Embed(title=f'(Error code: {fe.code}) | You don\'t have permission to send DMs!', color=0xecf457)
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                await webhook.send(embed=embed)
                        except error.HTTPException as httpe:
                            # ! Error while send messages log
                            printc(f'(Error code: {httpe.code}) | [{member}] - Error sending message!', red)
                            embed = Embed(title=f'(Error code: {httpe.code}) | [{member.name}] - Error sending message!', color=0xe52e2e)
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                await webhook.send(embed=embed)
                        except:
                            # ! Unknown error log
                            printc('Unknown error!', red)
                            embed = Embed(title='Unknown error!', color=0xe52e2e)
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                                await webhook.send(embed=embed)

                        await asyncio.sleep((rng(3,10)))

                    if (i == 29):
                        printc(f'Security timeout! | DMs sent: {i} | Waiting 15 minutes...', purple)
                        embed = Embed(title=f'Security timeout! | DMs sent: {i} | Waiting 15 minutes...', color=0xD237D2)
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
                            await webhook.send(embed=embed)
                        i = 0
                        await asyncio.sleep(900)
            else:
                return
    except:
        printc('Error scraping members!', red)
        return

    # End of the task
    printc(f'\n⮡  Task realized successfully! | DMs sent: {dmsCount}\n', purple)

    # End task embed log
    """ Start to create embeds """
    embed_cmd = Embed(
        title = f'Task realized successfully!',
        color = 0x6e0386
    )
    embed_cmd.set_author(
        name = 'Dev by: Sirius Beck (Gabriel Viana) | >>>  CONTACT ME HERE  <<<',
        icon_url = 'https://cdn.discordapp.com/emojis/958870691074179082.webp?size=128&quality=lossless',
        url = 'https://discord.gg/DyWxxK7NHM'
    )
    embed_cmd.add_field(
        name = '📋 Task ID',
        value = f'```{taskIDup}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '👤 User',
        value = f'```{ctx.author.name}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '🌍 Server',
        value = f'```{ctx.guild.name}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '🗨️ Channel',
        value = f'```{ctx.channel.name}```',
        inline = False
    )
    embed_cmd.add_field(
        name = '✅ DMs sent',
        value = f'```{dmsCount}```',
        inline = False
    )
    embed_cmd.set_footer(
        text = dtFormated
    )
    """ End embeds creation """
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(wurl, adapter=AsyncWebhookAdapter(session))
        webhookLog = Webhook.from_url(logUrl, adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed=embed_cmd)
        await webhookLog.send(embed=embed_cmd)

client.run(TOKEN)