from nextcord.ext import commands
import sqlite3
import datetime
from config import DATABASE_DIR

class database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect(DATABASE_DIR)
        self.cur = self.con.cursor()
        self.res = []
        self.com = []
        print("Classe DataBase prête à l'emploi !")
    
    @commands.Cog.listener()
    async def on_message(self,message):
        query_ck = f"""
        SELECT id, xp 
        FROM levels 
        WHERE id = {message.author.id};
        """
        self.res = self.cur.execute(query_ck)
        print(self.res.fetchall())
        print(self.res.fetchall() is None)
        if(message.author.bot == False):
            if(self.res.fetchall() is not None):
                query = f"""
                UPDATE levels
                SET xp = xp + (10 + 0.01*{len(message.content)})
                WHERE id = {message.author.id};
                """
                self.com = self.cur.execute(query)
                print(f"Niveau augmente ! utilisateur :{message.author}, valeur : {10+ 0.01*len(message.content)}")
                with open("logs\logs_levels_DB.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | INFO | user : @{message.author} | xp gained : {10 + 0.01*len(message.content)} | channel : {message.channel.id} ({message.channel.name})\n")
            else:
                self.com = self.cur.execute(f"INSERT INTO levels(id, xp) VALUES({message.author.id}, 10);")
                with open("logs\logs_levels_DB.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | INFO | new user registered : @{message.author}")

            self.con.commit()
        
    @commands.command()
    async def dataTest(self,ctx):
        self.res = self.cur.execute("SELECT * FROM levels")
        print(self.res.fetchmany(5))
        await ctx.send(self.res)
    

async def setup(bot):
    bot.add_cog(database(bot))