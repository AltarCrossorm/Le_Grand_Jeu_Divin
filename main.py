from config import *
from token_config import TOKEN

import nextcord
from nextcord.ext import commands

import os
import datetime

INTENTS = nextcord.Intents.all()
 
bot = commands.Bot(command_prefix = COMMAND_PREFIX, intents = INTENTS)
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.members = True

@bot.event
async def on_ready(): # message signifiant que le bot est prêt
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game('Guide de développement de bot pour les nuls'))

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    with open("logs\logs_sessions.log", "a") as fichier:
        fichier.write(f"{datetime.datetime.now()} | INFO | bot started\n")
    print("Prêt à servir mon maître")
    print("------------------------")


@bot.command(help = "essai de définition dans le !help")
async def hello(ctx): # nom de l'input
    await ctx.send("Bonjour maître.")

@bot.command()
async def repeat(ctx, arg): # nom de l'input
    print(arg)
    await ctx.send(f'Venez-vous de dire {arg} ?')

@bot.command()
async def embed(ctx):
    embed = nextcord.Embed(title="Voici un embed", url="https://google.com", description="voici une description", color=0xFF00FF)
    embed.set_author(name= ctx.author.display_name, url="https://youtube.tv", icon_url=ctx.author.avatar)
    embed.set_thumbnail(url=ctx.author.avatar)
    embed.add_field(name="Labrador",value="Cute Pyra", inline=True)
    embed.add_field(name="Pyra",value="Cute girl", inline=True)
    embed.set_footer(text="footer of the embed")
    await ctx.send(embed=embed)

@bot.command()
async def shutdown(ctx):
    if(ctx.author.id == ID_DEV or ctx.author.id == ID_OWNER):
        with open("logs\logs_sessions.log", "a") as fichier:
            fichier.write(f"{datetime.datetime.now()} | INFO | bot shutdown by {ctx.author}\n")
        await bot.close()
    else:
        with open("logs\logs_sessions.log", "a") as fichier:
            fichier.write(f"{datetime.datetime.now()} | WARN | shutdown command tried but not authorised\n")

bot.run(TOKEN) # équivalent à "return", lance le bot