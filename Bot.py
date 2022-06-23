from ast import alias
from tokenize import Name
from unicodedata import name
import discord
#import pandas as pd
from discord.ext import commands
import json
import os
from dotenv import load_dotenv, find_dotenv
import csv

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

@client.command(aliases='ul')
async def updatelineup(ctx, *Accounts):

    global LINEUP_CHANNEL
    Lineup_Category = discord.utils.get(ctx.guild.channels, name= LINEUP_CHANNEL)

    for i in range(len(Accounts)):
        if Accounts[i][0] == '#':
            try:
                channel_id = int(rosteredAccounts[Accounts[i]])
            except Exception:
                pass
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



@client.command(aliases='gc')
async def getchannels(ctx, *, category: discord.CategoryChannel):
    channels = category.channels
    for i in range(len(channels)):
        await ctx.send(channels[i].name + '    ' + str(channels[i].id))
        print(channels[i].id)

@client.command(aliases='hr')
async def hitrate(ctx, MODE, TARGET_CLAN='us'):
    if str(ctx.message.attachments) == "[]": # Checks if there is an attachment on the message
        return
    else: # If there is it gets the filename from message.attachments
        split_v1 = str(ctx.message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        if filename.endswith(".csv"): # Checks if it is a .csv file
            await ctx.message.attachments[0].save(fp="HRsheets\\{}".format(filename)) # saves the file
            ATTACKS, TRIPLES = hrcalculation("HRsheets\\{}".format(filename), TARGET_CLAN, MODE )
            Output = "\n"
            for i in ATTACKS.keys():
                Output = Output + "\n" + i.rjust(20) + "\t" + str(TRIPLES.get(i,0)) + '/' + str(ATTACKS.get(i,0))
            Embed_Output = discord.Embed(title="{0} \n {1}".format(filename, TARGET_CLAN), description="```{0}```".format(Output))
            os.remove("HRsheets\\{}".format(filename)) #cleanup
            await ctx.send(embed=Embed_Output)



def hrcalculation(FilePath, TARGET, MODE):
    # Variables for interface with minion bot csv output, These are actually the corresponding column values in the csv
    # Maybe I should make these in a json outside the script so that they are easier to change if mb updates
    Att_Clan = 0
    Def_Clan = 1
    Att      = 2
    Def      = 3
    Att_Tag  = 18
    Def_Tag  = 19
    Clan_Tag = 14
    Opp_Tag  = 15
    Att_Clan_Tag = 25
    Def_Clan_Tag = 26
    Fresh = 24
    Att_Th = 29
    Def_Th = 30
    Stars = 20
    Stars_Gained = 21

    #initializers dicts for HRs, Occurences records attacks and Triples records triples
    Triples = {}
    Occurences = {}

    with open(FilePath , encoding='utf8') as File:
        readtemp = csv.reader(File)
        read = sorted(readtemp, key=lambda elem: elem[Att_Th], reverse=True)

    if TARGET.lower() == 'us':
        TARGET_CLAN = read[1][Att_Clan_Tag]
    else:
        TARGET_CLAN = read[1][Def_Clan_Tag]

    for row in read:
        if MODE.lower() == 'attack':
            mode = Att_Clan_Tag
            name = Att
        else:
            mode = Def_Clan_Tag
            name = Def

        if row[mode] != TARGET_CLAN:
            continue
   
        if row[Stars_Gained] == '' or row[Att_Th] != row[Def_Th]:
            continue

        Occurences.setdefault(row[name], 0)
        Occurences[row[name]] = Occurences[row[name]] + 1

        if int(row[Stars]) == 3 and int(row[Stars_Gained]) != 0:
            Triples.setdefault(row[name], 0)
            Triples[row[name]] = Triples[row[name]] + 1

    return (Occurences, Triples)


with open('Roster_Data.json') as j:
    rosteredAccounts = json.load(j)


client.run(DISCORD_TOKEN_ID)

