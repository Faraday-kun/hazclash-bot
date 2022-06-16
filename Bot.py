from tokenize import Name
from unicodedata import name
import discord
import pandas as pd
from discord.ext import commands
import json
import os
from dotenv import load_dotenv, find_dotenv

# Roster = pd.read_excel('Roster.xlsx')
# Names_List = Roster[Roster.columns[4]].tolist()
# print(Names_List)


client = commands.Bot(command_prefix='$')
LINEUP_CHANNEL = 'Gcc-Lineup'


load_dotenv()
DISCORD_TOKEN_ID = os.environ.get("BOT_TOKEN")


@client.event
async def on_ready():
    print('ready')
    print(client.guilds)




@client.command()
async def makechannels(ctx, category_name):
    global Names_List
    print('hi')
    B = discord.utils.get(ctx.guild.channels, name=category_name)
    for i in Names_List[50:59]:
        await ctx.guild.create_text_channel(i, category=B)


@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def move(ctx, current_cat: discord.CategoryChannel, target_cat: discord.CategoryChannel, *Accounts):
    current_cat_channels = current_cat.channels
    iter = 0
    for i in range(len(current_cat_channels)):
        temp = str(current_cat_channels[i])
        print(temp[1:-3])
        print(Accounts[1])
        if temp[1:-3] == Accounts[iter].lower():
            #move channel
            await current_cat_channels[i].edit(category=target_cat)
            #await ctx.channel.edit(category=target_cat)
            iter = iter+1


@client.command()
async def setlineupchannel(channel_name):
    global LINEUP_CHANNEL
    LINEUP_CHANNEL = channel_name

@client.command()
async def green(ctx):
    previous_name = ctx.channel.name
    await ctx.channel.edit(name = '🟢' + previous_name[1:])

@client.command()
async def red(ctx):
    previous_name = ctx.channel.name
    await ctx.channel.edit(name = '🔴' + previous_name[1:])

@client.command()
async def updatelineup(ctx, *Accounts):

    global LINEUP_CHANNEL
    Lineup_Category = discord.utils.get(ctx.guild.channels, name= LINEUP_CHANNEL)

    for i in range(len(Accounts)):
        if Accounts[i][0] == '#':
            channel_id = int(rosteredAccounts[Accounts[i]])
            channelname = discord.utils.get(ctx.guild.channels, id = channel_id)
            await channelname.edit(category = Lineup_Category)

@client.command()
async def revert(ctx):
    Lineup_Category = discord.utils.get(ctx.guild.channels, name= LINEUP_CHANNEL)
    ROSTER_Category = discord.utils.get(ctx.guild.channels, name= 'gcc')
    R11_Category = discord.utils.get(ctx.guild.channels, name= 'GCC 11s')
    
    channels = Lineup_Category.channels
    for i in range(len(channels)):
        if channels[i].name[-2:] == '11':
            await channels[i].edit(category = R11_Category)
        else:
            await channels[i].edit(category = ROSTER_Category)



@client.command()
async def getchannels(ctx, *, category: discord.CategoryChannel):
    channels = category.channels
    for i in range(len(channels)):
        await ctx.send(channels[i].name + '    ' + str(channels[i].id))
        print(channels[i].id)

with open('Roster_Data.json') as j:
    rosteredAccounts = json.load(j)


client.run(DISCORD_TOKEN_ID)

