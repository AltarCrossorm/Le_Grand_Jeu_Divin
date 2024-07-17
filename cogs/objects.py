import nextcord
from nextcord.ext import commands

import sqlite3
from config import DATABASE_DIR, MESSAGE_URL
import re

class objects(commands.Cog):

    def __init__(self,bot):
        """initialize the class

        Args:
            bot (Any): the instance of the bot
        """
        self.client = bot
        self.con = sqlite3.connect(DATABASE_DIR)
        self.cur = self.con.cursor()
        self.content = []
        self.attributes = []

        try: # Checking if the database is opennable
            self.con.cursor()
            return print("Objects table ready")
        except Exception as ex:
            return print("Objects table acces error")
        
    @commands.command()
    async def add_object(self, ctx, url: str):

        if(url.startswith("https://discord.com")):
            match = MESSAGE_URL[0].match(url)
        if(url.startswith("https://canary.discord.com")):
            match = MESSAGE_URL[1].match(url)
        if(url.startswith("https://ptb.discord.com")):
            match = MESSAGE_URL[2].match(url)
        if not match:
            await ctx.send('URL de message invalide.')
            return

        guild_id, channel_id, message_id = map(int, match.groups())

        guild = self.client.get_guild(guild_id)
        if not guild:
            await ctx.send('Serveur non trouvé.')
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            await ctx.send('Canal non trouvé.')
            return

        try:
            message = await channel.fetch_message(message_id)
            lines  = message.content.split('\n')
            
            type   = lines[1][21:]
            name   = lines[0][19:]
            chara  = lines[2][33:]
            effect = lines[3][23:]

            self.content.append(type)
            self.content.append(name)
            self.content.append(chara)
            self.content.append(effect)
            for i in range(len(lines)-4):
                self.attributes.append(lines[i+4])
            print(self.attributes)
            print(self.content)

            await ctx.send(f"``{self.content[0]}\n{self.content[1]}\n{self.content[2]}\n{self.content[3]}``")
            
        except nextcord.NotFound:
            await ctx.send('Message non trouvé.')
        except nextcord.Forbidden:
            await ctx.send('Permission refusée pour accéder à ce message.')
        except nextcord.HTTPException as e:
            await ctx.send(f'Erreur HTTP: {e}')

        self.attributes.clear()
        self.content.clear()



async def setup(client):
    """
    function used to setup the class in the bot
    :param client: the client of the bot
    """
    client.add_cog(objects(client))