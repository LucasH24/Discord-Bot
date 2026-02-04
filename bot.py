import discord
import config
import json
import requests

from rankCalc import calc_tag
from colorCalc import calc_color
from miwDataObject import get_miw_data
from io import BytesIO
from discord.ext import commands
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

bot = commands.Bot(command_prefix=config.PREFIX, case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')

def in_blacklist(ctx):
  return not str(ctx.message.author.id) in ['374955775656984576', '584565037256146945', '631025362863783946']

def getInfo(call):
    r = requests.get(call)
    return r.json()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"{config.PREFIX}help"))
    print("-----")
    print("Bot is online!")
    print("-----")

# basic commands -----------------------------------------------------------------------------------

@bot.command()
@commands.check(in_blacklist)
async def ping(ctx):
    await ctx.send(f"I have a latency of {round(bot.latency * 1000, 1)}** ms")

@bot.command()
@commands.check(in_blacklist)
async def help(ctx):
    await ctx.send(f"Check the pin in the bots channel of the Mini Walls community server for help")

# stat commands -----------------------------------------------------------------------------------
@bot.command()
@commands.check(in_blacklist)
async def s(ctx, username):

    try:
        errorValue = 1
        mojangUrl = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        dataMojang = getInfo(mojangUrl)
        uuid = dataMojang["id"]
        
        errorValue = 2
        hypixelUrl = f"https://api.hypixel.net/player?key={config.APIKEY}&uuid={uuid}"
        dataHypixel = getInfo(hypixelUrl)
        rankReturn = calc_tag(dataHypixel["player"])
        miwDataObject = get_miw_data(dataHypixel)
        
    except:
        match errorValue:
            case 1:
                await ctx.send(f"Mojang API Return: {dataMojang['errorMessage']}")
            case 2:
                #await ctx.send(f"Hypixel API Return: {dataHypixel}")
                await ctx.send(f"")
    
    img = Image.new('RGB', (700, 350), color = '#181c30')
    font = ImageFont.truetype("arial.ttf", 25)

    d = ImageDraw.Draw(img)
    d.line((3, 3) + (698, 3), width=5, fill=("#5b2573"))
    d.line((3, 3) + (3, 347), width=5, fill=("#5b2573"))
    
    d.line((697, 3) + (697, 347), width=5, fill=("#5b2573"))
    d.line((3, 349) + (697, 347), width=5, fill=("#5b2573"))
    
    d.text((20,10), "Mini Walls Stats", fill=("white"), font=font)


    #draw rank
    if len(rankReturn) == 1:
        if rankReturn[0][1] == "[VIP]":
            d.text((20,50), f"[VIP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((68,50), f"] {miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)

        elif rankReturn[0][1] == "[MVP]":
            d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((82,50), f"] {miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)

        else:
            d.text((20,50), f"{miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)

    else:
        if rankReturn[0][1] == "[VIP":
            d.text((20,50), f"[VIP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((70,50), f"+", fill=(f"#{rankReturn[1][0]}"), font=font)
            d.text((85,50), f"] {miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)
        else:
            if rankReturn[1][1] == "+":
                d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
                d.text((83,50), f"+", fill=(f"#{rankReturn[1][0]}"), font=font)
                d.text((98,50), f"] {miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)

            if rankReturn[1][1] == "++":
                d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
                d.text((83,50), f"++", fill=(f"#{rankReturn[1][0]}"), font=font)
                d.text((114,50), f"] {miwDataObject.name}", fill=(f"#{rankReturn[0][0]}"), font=font)
    #------------------------

    d.text((20,110), f"Wins: {'{:,}'.format(miwDataObject.wins)}", fill=("white"), font=font)
    d.text((20,150), f"Kills: {'{:,}'.format(miwDataObject.kills)}", fill=("white"), font=font)
    d.text((20,190), f"Finals: {'{:,}'.format(miwDataObject.finals)}", fill=("white"), font=font)
    d.text((20,230), f"Wither Damage: {'{:,}'.format(miwDataObject.witherDamage)}", fill=("white"), font=font)
    d.text((20,270), f"Wither Kills: {'{:,}'.format(miwDataObject.witherKills)}", fill=("white"), font=font)
    d.text((20,310), f"Deaths: {'{:,}'.format(miwDataObject.deaths)}", fill=("white"), font=font)

    d.text((400,110), f"TK/D: {miwDataObject.tkd}", fill=("white"), font=font)
    d.text((400,150), f"K/D: {miwDataObject.kd}", fill=("white"), font=font)
    d.text((400,190), f"F/D: {miwDataObject.fd}", fill=("white"), font=font)
    d.text((400,230), f"WD/D: {miwDataObject.wdd}", fill=("white"), font=font)
    d.text((400,270), f"WK/D: {miwDataObject.wkd}", fill=("white"), font=font)
    d.text((400,310), f"AA: {miwDataObject.aa}", fill=("white"), font=font)

    bytes = BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)
    dfile = discord.File(bytes, filename="image.png")

    await ctx.send(file=dfile)


@bot.command()
@commands.check(in_blacklist)
async def advs(ctx, username):

    uuid = ""

    try:
        errorValue = 1
        mojangUrl = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        dataMojang = getInfo(mojangUrl)
        uuid = dataMojang["id"]
        
        errorValue = 2
        hypixelUrl = f"https://api.hypixel.net/player?key={config.APIKEY}&uuid={uuid}"
        dataHypixel = getInfo(hypixelUrl)
        rankReturn = calc_tag(dataHypixel["player"])

        errorValue = 3
        azureUrl = f"https://miw-player-api.azurewebsites.net/api/miwPlayers/uuid/{uuid}"
        dataAzure = getInfo(azureUrl)
        
    except:
        match errorValue:
            case 1:
                await ctx.send(f"Mojang API Return: {dataMojang['errorMessage']}")
            case 2:
                #await ctx.send(f"Hypixel API Return: {dataHypixel}")
                await ctx.send(f"")
            case 3:
                await ctx.send("Player requested is not in the top 250")

    
    img = Image.new('RGB', (900, 430), color = '#181c30')
    font = ImageFont.truetype("arial.ttf", 25)
    fontSmall = ImageFont.truetype("arial.ttf", 20)

    d = ImageDraw.Draw(img)
    d.line((3, 3) + (897, 3), width=5, fill=("#5b2573"))
    d.line((3, 3) + (3, 427), width=5, fill=("#5b2573"))
    
    d.line((897, 3) + (897, 427), width=5, fill=("#5b2573"))
    d.line((3, 427) + (897, 427), width=5, fill=("#5b2573"))
    
    d.text((20,10), "Mini Walls Stats", fill=("white"), font=font)
    
    #draw rank
    if len(rankReturn) == 1:
        if rankReturn[0][1] == "[VIP]":
            d.text((20,50), f"[VIP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((68,50), f"] {dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)

        elif rankReturn[0][1] == "[MVP]":
            d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((82,50), f"] {dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)

        else:
            d.text((20,50), f"{dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)

    else:
        if rankReturn[0][1] == "[VIP":
            d.text((20,50), f"[VIP", fill=(f"#{rankReturn[0][0]}"), font=font)
            d.text((70,50), f"+", fill=(f"#{rankReturn[1][0]}"), font=font)
            d.text((85,50), f"] {dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)
        else:
            if rankReturn[1][1] == "+":
                d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
                d.text((83,50), f"+", fill=(f"#{rankReturn[1][0]}"), font=font)
                d.text((98,50), f"] {dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)

            if rankReturn[1][1] == "++":
                d.text((20,50), f"[MVP", fill=(f"#{rankReturn[0][0]}"), font=font)
                d.text((83,50), f"++", fill=(f"#{rankReturn[1][0]}"), font=font)
                d.text((114,50), f"] {dataAzure[0]['username']}", fill=(f"#{rankReturn[0][0]}"), font=font)
    #------------------------

    d.text((20,110), f"W", fill=("white"), font=fontSmall)
    d.text((20,135), f"{'{:,}'.format(dataAzure[0]['wins'])}", fill=("white"), font=fontSmall)
    d.text((20,160), f"#{(dataAzure[0]['rankWins'])}", fill=(calc_color(dataAzure[0]['rankWins'])), font=fontSmall)

    d.text((130,110), f"K", fill=("white"), font=fontSmall)
    d.text((130,135), f"{'{:,}'.format(dataAzure[0]['kills'])}", fill=("white"), font=fontSmall)
    d.text((130,160), f"#{(dataAzure[0]['rankKills'])}", fill=(calc_color(dataAzure[0]['rankKills'])), font=fontSmall)


    d.text((240,110), f"F", fill=("white"), font=fontSmall)
    d.text((240,135), f"{'{:,}'.format(dataAzure[0]['finals'])}", fill=("white"), font=fontSmall)
    d.text((240,160), f"#{(dataAzure[0]['rankFinals'])}", fill=(calc_color(dataAzure[0]['rankFinals'])), font=fontSmall)

    d.text((350,110), f"WD", fill=("white"), font=fontSmall)
    d.text((350,135), f"{'{:,}'.format(dataAzure[0]['witherDamage'])}", fill=("white"), font=fontSmall)
    d.text((350,160), f"#{(dataAzure[0]['rankWitherDamage'])}", fill=(calc_color(dataAzure[0]['rankWitherDamage'])), font=fontSmall)

    d.text((460,110), f"WK", fill=("white"), font=fontSmall)
    d.text((460,135), f"{'{:,}'.format(dataAzure[0]['witherKills'])}", fill=("white"), font=fontSmall)
    d.text((460,160), f"#{(dataAzure[0]['rankWitherKills'])}", fill=(calc_color(dataAzure[0]['rankWitherKills'])), font=fontSmall)

    d.text((570,110), f"AH", fill=("white"), font=fontSmall)
    d.text((570,135), f"{'{:,}'.format(dataAzure[0]['arrowsHit'])}", fill=("white"), font=fontSmall)
    d.text((570,160), f"#{(dataAzure[0]['rankArrowsHit'])}", fill=(calc_color(dataAzure[0]['rankArrowsHit'])), font=fontSmall)

    d.text((680,110), f"AS", fill=("white"), font=fontSmall)
    d.text((680,135), f"{'{:,}'.format(dataAzure[0]['arrowsShot'])}", fill=("white"), font=fontSmall)
    d.text((680,160), f"#{(dataAzure[0]['rankArrowsShot'])}", fill=(calc_color(dataAzure[0]['rankArrowsShot'])), font=fontSmall)

    d.text((790,110), f"D", fill=("white"), font=fontSmall)
    d.text((790,135), f"{'{:,}'.format(dataAzure[0]['deaths'])}", fill=("white"), font=fontSmall)
    d.text((790,160), f"#{(dataAzure[0]['rankDeaths'])}", fill=("white"), font=fontSmall)

    

    d.text((20,210), f"KD", fill=("white"), font=fontSmall)
    d.text((20,235), f"{'{:,}'.format(dataAzure[0]['kd'])}", fill=("white"), font=fontSmall)
    d.text((20,260), f"#{(dataAzure[0]['rankKD'])}", fill=(calc_color(dataAzure[0]['rankKD'])), font=fontSmall)

    d.text((130,210), f"FKD", fill=("white"), font=fontSmall)
    d.text((130,235), f"{'{:,}'.format(dataAzure[0]['fkd'])}", fill=("white"), font=fontSmall)
    d.text((130,260), f"#{(dataAzure[0]['rankFKD'])}", fill=(calc_color(dataAzure[0]['rankFKD'])), font=fontSmall)

    d.text((240,210), f"TKD", fill=("white"), font=fontSmall)
    d.text((240,235), f"{'{:,}'.format(dataAzure[0]['tkd'])}", fill=("white"), font=fontSmall)
    d.text((240,260), f"#{(dataAzure[0]['rankTKD'])}", fill=(calc_color(dataAzure[0]['rankTKD'])), font=fontSmall)

    d.text((350,210), f"WDD", fill=("white"), font=fontSmall)
    d.text((350,235), f"{'{:,}'.format(dataAzure[0]['wdd'])}", fill=("white"), font=fontSmall)
    d.text((350,260), f"#{(dataAzure[0]['rankWDD'])}", fill=(calc_color(dataAzure[0]['rankWDD'])), font=fontSmall)

    d.text((460,210), f"WKD", fill=("white"), font=fontSmall)
    d.text((460,235), f"{'{:,}'.format(dataAzure[0]['wkd'])}", fill=("white"), font=fontSmall)
    d.text((460,260), f"#{(dataAzure[0]['rankWKD'])}", fill=(calc_color(dataAzure[0]['rankWKD'])), font=fontSmall)

    d.text((570,210), f"AA", fill=("white"), font=fontSmall)
    d.text((570,235), f"{'{:,}'.format(dataAzure[0]['aa'])}", fill=("white"), font=fontSmall)
    d.text((570,260), f"#{(dataAzure[0]['rankAA'])}", fill=(calc_color(dataAzure[0]['rankAA'])), font=fontSmall)

    d.text((680,210), f"RATE", fill=("white"), font=fontSmall)
    d.text((680,235), f"{'{:,}'.format(dataAzure[0]['rate'])}", fill=("white"), font=fontSmall)
    d.text((680,260), f"#{(dataAzure[0]['rankRATE'])}", fill=(calc_color(dataAzure[0]['rankRATE'])), font=fontSmall)



    d.text((20,310), f"KPW", fill=("white"), font=fontSmall)
    d.text((20,335), f"{'{:,}'.format(dataAzure[0]['kpw'])}", fill=("white"), font=fontSmall)
    d.text((20,360), f"#{(dataAzure[0]['rankKPW'])}", fill=("white"), font=fontSmall)

    d.text((130,310), f"FPW", fill=("white"), font=fontSmall)
    d.text((130,335), f"{'{:,}'.format(dataAzure[0]['fpw'])}", fill=("white"), font=fontSmall)
    d.text((130,360), f"#{(dataAzure[0]['rankFPW'])}", fill=("white"), font=fontSmall)

    d.text((240,310), f"TKPW", fill=("white"), font=fontSmall)
    d.text((240,335), f"{'{:,}'.format(dataAzure[0]['tkpw'])}", fill=("white"), font=fontSmall)
    d.text((240,360), f"#{(dataAzure[0]['rankTKPW'])}", fill=("white"), font=fontSmall)

    d.text((350,310), f"WDPW", fill=("white"), font=fontSmall)
    d.text((350,335), f"{'{:,}'.format(dataAzure[0]['wdpw'])}", fill=("white"), font=fontSmall)
    d.text((350,360), f"#{(dataAzure[0]['rankWDPW'])}", fill=("white"), font=fontSmall)

    d.text((460,310), f"WKPW", fill=("white"), font=fontSmall)
    d.text((460,335), f"{'{:,}'.format(dataAzure[0]['wkpw'])}", fill=("white"), font=fontSmall)
    d.text((460,360), f"#{(dataAzure[0]['rankWKPW'])}", fill=("white"), font=fontSmall)

    d.text((570,310), f"DPW", fill=("white"), font=fontSmall)
    d.text((570,335), f"{'{:,}'.format(dataAzure[0]['dpw'])}", fill=("white"), font=fontSmall)
    d.text((570,360), f"#{(dataAzure[0]['rankDPW'])}", fill=("white"), font=fontSmall)

    d.text((680,310), f"SPW", fill=("white"), font=fontSmall)
    d.text((680,335), f"{'{:,}'.format(dataAzure[0]['spw'])}", fill=("white"), font=fontSmall)
    d.text((680,360), f"#{(dataAzure[0]['rankSPW'])}", fill=("white"), font=fontSmall)
    

    bytes = BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)
    dfile = discord.File(bytes, filename="image.png")

    await ctx.send(file=dfile)


@bot.command()
@commands.check(in_blacklist)
async def lb(ctx, type, count):
    sqlType = ""
    javascriptType = ""
    username = "username"
    listOfCommands = ["w", "k", "f", "wd", "wk", "d", "ah", "as", "kd", "fkd", "tkd", "wdd", "wkd", "aa", "rate", "kpw", "fpw", "tkpw", "wdpw", "wkpw", "dpw", "spw"]
    listOfLbsSQL = ["Wins", "Kills", "Finals", "WitherDamage", "WitherKills", "Deaths", "ArrowsHit", "ArrowsShot", "KD", "FKD", "TKD", "WDD", "WKD", "AA", "RATE", "KPW", "FPW", "TKPW", "WDPW", "WKPW", "DPW", "SPW"]
    listOfLbsJavascript = ["wins", "kills", "finals", "witherDamage", "witherKills", "deaths", "arrowsHit", "arrowsShot", "kd", "fkd", "tkd", "wdd", "wkd", "aa", "rate", "kpw", "fpw", "tkpw", "wdpw", "wkpw", "dpw", "spw"]
    counter = 0

    while (22 > counter):
        if listOfCommands[counter] == type or listOfLbsSQL[counter].lower() == type.lower():
            sqlType = listOfLbsSQL[counter]
            javascriptType = listOfLbsJavascript[counter]
        counter = counter + 1 
    
    if sqlType == "":
        await ctx.send("Invalid leaderboard type")
    
    url = f"https://miw-player-api.azurewebsites.net/api/miwPlayers/leaderboard/{sqlType}"
    data = getInfo(url)

    listOfPlayers = []
    for y in data:
        tempObject = [y[username], y[javascriptType]]
        listOfPlayers.append(tempObject)

    embed = discord.Embed(
        colour=discord.Colour.red(),
        title = "Leaderboard",
        description = f"Type: {sqlType}",
    )

    counter = 0
    lbString = ""

    if int(count) > 25:
        await ctx.send("Highest supported lb length is currently 25")

    while (int(count)) > counter:
        lbString = lbString + f"{counter + 1}: " f"{listOfPlayers[counter][0]} - " + f"{'{:,}'.format(listOfPlayers[counter][1])}  \n"
        #embed.add_field(name="", value=f"{counter + 1}: " f"{listOfPlayers[counter][0]} - " + f"{'{:,}'.format(listOfPlayers[counter][1])}", inline=False)
        counter = counter + 1
    embed.add_field(name="", value=lbString, inline=False)
    now = datetime.now()
    embed.set_footer(text = f"Generated at {now}")

    await ctx.send(embed=embed)
   



bot.run(config.TOKEN)


# py bot.py
#py -m pip
#cd OneDrive/Documents/Coding/Side_Projects/Miw Bot