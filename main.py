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
async def on_ready(): 
    """
    Startup command for the bot
    """
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game('Guide de développement de bot pour les nuls'))

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    with open("logs/logs_sessions.log", "a") as fichier:
        fichier.write(f"{datetime.datetime.now()} | INFO | bot started\n")
    print("+--------------------------+")
    print("| Prêt à servir mon maître |")
    print("+--------------------------+")


@bot.command()
async def shutdown(ctx):
    if(ctx.author.id == ID_DEV or ctx.author.id == ID_OWNER):
        with open("logs/logs_sessions.log", "a") as fichier:
            fichier.write(f"{datetime.datetime.now()} | INFO | bot shutdown by {ctx.author}\n")
        await bot.close()
    else:
        with open("logs/logs_sessions.log", "a") as fichier:
            fichier.write(f"{datetime.datetime.now()} | WARN | shutdown command tried but not authorised\n")

bot.run(TOKEN) # équivalent à "return", lance le bot