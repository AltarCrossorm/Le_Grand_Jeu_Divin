import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View

import sqlite3
from config import DATABASE_DIR, MESSAGE_URL, ID_DEV
import datetime



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

        match = None
        for regex in MESSAGE_URL:
            match = regex.match(url)
            if match:
                break

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

            self.content= [lines[1][21:], lines[0][19:], lines[2][33:], lines[3][23:]]
            for attributes in lines[4:]:
                self.attributes.append(attributes)
            
        except nextcord.NotFound:
            return await ctx.send('Message non trouvé.')
        except nextcord.Forbidden:
            return await ctx.send('Permission refusée pour accéder à ce message.')
        except nextcord.HTTPException as e:
            return await ctx.send(f'Erreur HTTP: {e}')

        desc =f"""
**`{self.content[0]}`**
# {self.content[1]}
### {self.content[2]}
*{self.content[3]}*
"""

        e = nextcord.Embed(
            title = f"Ajouter cet objet ?",
            description=desc,
            colour=(nextcord.Colour.orange())
        )

        class AddObjBtn(View):
            def __init__(self, attributes:list, content:list, cursor:sqlite3, ctx):
                super().__init__(timeout=180)
                self.content = []
                self.attributes = []
                self.cur = cursor
                self.ctx = ctx

            @nextcord.ui.button(label="Confirmer", style=nextcord.ButtonStyle.green)
            async def confirm(self, button: Button, interaction: nextcord.Interaction):
                self.cur.execute("INSERT INTO entity_list(type, name, desc, effectDesc) VALUES(?,?,?,?);", self.content)
                self.cur.connection.commit()
                
                id = self.cur.execute("SELECT id FROM entity_list WHERE name = ?;", (self.content[1],)).fetchone()[0]
                

                for rows in self.attributes:
                    if rows[4:7] != "HP ":
                        self.cur.execute(f'INSERT INTO entity_metadata(entityRelated,effectType,valRelated,valquantity) VALUES({id},"{rows[:3]}","{rows[4:7]}","{rows[8:]}");')
                    else:
                        self.cur.execute(f'INSERT INTO entity_metadata(entityRelated,effectType,valRelated,valquantity) VALUES({id},"{rows[:3]}","{rows[4:6]}","{rows[7:]}");')

                self.cur.connection.commit()
                with open("logs\logs_objects.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | INFO | @{ctx.author} added \"{self.content[1]}\" to database\n")
                await interaction.response.send_message("Objet ajouté à la base de données.")
            
            @nextcord.ui.button(label="Annuler", style=nextcord.ButtonStyle.red)
            async def cancel(self, button: Button, interaction: nextcord.Interaction):
                await interaction.response.send_message("Ajout annulé.")
                with open("logs\logs_objects.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | ERROR | @{ctx.author} cancelled to add {self.content[1]} to database\n")
                self.stop()  # Arrête la vue pour désactiver les boutons


        await ctx.send(embed=e, view=AddObjBtn(self.attributes, self.content, self.cur, ctx))

        View.wait()

        self.content = []
        self.attributes = []


    @commands.command()
    async def add_all_objects(self, ctx, channel: nextcord.TextChannel):
        if ctx.author.id != ID_DEV:
            return
        
        i = 0
        async for message in channel.history(limit=2048):
            if (len(message.content) > 30):
                i = i + 1
                print(len(message.content))
                print(i)

        e = nextcord.Embed(
            title = f"Ajouter cet objet ?",
            description=f"En appuyant sur \"Confirmer\" vous ajouterez **{i}** objets, souhaitez-vous confirmer ?",
            colour=(nextcord.Colour.orange())
        )

        class AddAllObjBtn(View):
            def __init__(self, attributes:list, content:list, cursor:sqlite3, ctx, channel:nextcord.TextChannel):
                super().__init__(timeout=180)
                self.content = content
                self.attributes = attributes
                self.cur = cursor
                self.ctx = ctx
                self.channel = channel
                

            @nextcord.ui.button(label="Confirmer", style=nextcord.ButtonStyle.green)
            async def confirm(self, button: Button, interaction: nextcord.Interaction):
                self.cur.execute("DELETE FROM entity_list;")
                self.cur.execute("DELETE FROM entity_metadata;")
                async for message in channel.history(limit=2048):
                    if (len(message.content) > 30):
                        lines = message.content.split('\n')

                        type   = lines[1][21:]
                        name   = lines[0][19:]
                        chara  = lines[2][33:]
                        effect = lines[3][23:]

                        self.content= [type, name, chara, effect]
                        for attributes in lines[4:]:
                            if attributes != '':
                                self.attributes.append(attributes)

                        self.cur.execute("INSERT INTO entity_list(type, name, desc, effectDesc) VALUES(?,?,?,?);", self.content)
                        self.cur.connection.commit()
                        
                        id = self.cur.execute("SELECT id FROM entity_list WHERE name = ?;", (self.content[1],)).fetchone()[0]
                        
                        print(self.attributes)
                        for rows in self.attributes:
                            if rows[4:7] != "HP ":
                                self.cur.execute(f'INSERT INTO entity_metadata(entityRelated,effectType,valRelated,valquantity) VALUES({id},"{rows[:3]}","{rows[4:7]}","{rows[8:]}");')
                            else:
                                self.cur.execute(f'INSERT INTO entity_metadata(entityRelated,effectType,valRelated,valquantity) VALUES({id},"{rows[:3]}","{rows[4:6]}","{rows[7:]}");')

                        self.cur.connection.commit()
                        with open("logs\logs_objects.log", "a") as fichier:
                            fichier.write(f"{datetime.datetime.now()} | INFO | @{ctx.author} added \"{self.content[1]}\" to database\n")

                        await self.ctx.reply(f"Objet \"{self.content[1]}\" ajouté à la base de données.")
                        print(self.content[1])

                        self.attributes.clear()
                        self.content.clear()



            @nextcord.ui.button(label="Annuler", style=nextcord.ButtonStyle.red)
            async def cancel(self, button: Button, interaction: nextcord.Interaction):
                await interaction.response.send_message("Ajout annulé.")
                with open("logs\logs_objects.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | ERROR | @{ctx.author} cancelled to add a package of objects to database\n")
                self.stop()  # Arrête la vue pour désactiver les boutons

        await ctx.send(embed=e, view=AddAllObjBtn(self.attributes, self.content, self.cur, ctx, channel))




async def setup(client):
    """
    function used to setup the class in the bot
    :param client: the client of the bot
    """
    client.add_cog(objects(client))