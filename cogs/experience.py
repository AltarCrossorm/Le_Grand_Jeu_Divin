import nextcord
from nextcord.ext import commands
import sqlite3
import datetime
from config import DATABASE_DIR

class experience(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect(DATABASE_DIR)
        self.cur = self.con.cursor()
        self.res = []
        self.com = []
        try:
            self.con.cursor()
            return print("Database ready")
        except Exception as ex:
            return print("Database Error")
    
    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.bot:
            return

        user_id = message.author.id
        message_length = len(message.content)
        query_ck = f"""
        SELECT id, xp 
        FROM levels 
        WHERE id = {user_id};
        """
        
        self.cur.execute(query_ck)
        user = self.cur.fetchone()

        if user:
            query_update = f"""
            UPDATE levels
            SET xp = xp + (10 + 0.01 * {message_length})
            WHERE id = {user_id};
            """
            self.cur.execute(query_update)
            if(self.cur.rowcount > 0):
                print(f"Niveau augmente ! utilisateur :{message.author}, valeur : {10 + 0.01 * message_length}")

                with open("./logs/logs_levels_DB.log", "a") as fichier:
                    fichier.write(f"{datetime.datetime.now()} | INFO | user : @{message.author} | xp gained : {10 + 0.01 * message_length} | channel : {message.channel.id} ({message.channel.name})\n")
                    print("Log envoyé")
            else:
                print("Error databaase, please check it up")

        else:
            query_insert = f"""
            INSERT INTO levels(id,xp)
            VALUES({user_id}, 10);
            """
            self.com = self.cur.execute(query_insert)
            with open("logs\logs_levels_DB.log", "a") as fichier:
                fichier.write(f"{datetime.datetime.now()} | INFO | new user registered : @{message.author}\n")
                print("New user added to the database")

        self.con.commit()
        
    @commands.command(help = "draws the 5 most experienced users")
    async def dataTest(self,ctx):

        xp = []

        for row in self.cur.execute("SELECT * FROM levels;").fetchmany(5):
            user_id = row[0]
            user_xp = row[1]
            user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
            xp.append((user,user_xp))
        
        description = '\n'.join([f'{user.name}: {xp} XP' for user, xp in xp])

        mbed = nextcord.Embed(
            title="Most 5 experienced users",
            description = description,
            colour=(nextcord.Colour.green())
        )

        await ctx.send(embed=mbed)
    

async def setup(bot):
    bot.add_cog(experience(bot))