import nextcord
from nextcord.ext import commands
from math import exp
import sqlite3
import datetime
from config import DATABASE_DIR

class experience(commands.Cog):

    def __init__(self, bot):
        """
        Initialize experience class
        :param bot: The bot Discord instancy.
        """

        self.bot = bot
        self.con = sqlite3.connect(DATABASE_DIR)
        self.cur = self.con.cursor()

        try: # Checking if the database is opennable
            self.con.cursor()
            return print("Database ready")
        except Exception as ex:
            return print("Database Error")
    
    @commands.Cog.listener()
    async def on_message(self,message):
        """
        Event invoked whenever a message can be seen by the bot
        :param message: The message sent.
        """

        if message.author.bot: # Checks if the sender isn't a bot 
            return

        # Declaring variables who will be used later
        user_id = message.author.id
        message_length = len(message.content)

        # Checks if the used exists in the Database
        query_check = f"""
        SELECT id, xp 
        FROM levels 
        WHERE id = {user_id};
        """
        self.cur.execute(query_check)

        # Checks if user is empty or not
        user = self.cur.fetchone()
        if user:

            # Grants more xp by the size of the text
            query_update = f"""
            UPDATE levels
            SET xp = xp + (5 + 0.02 * {message_length}), xp_total = xp_total + (5 + 0.02 * {message_length})
            WHERE id = {user_id};
            """
            self.cur.execute(query_update)

            # Write the xp gain into the .log file
            with open("./logs/logs_levels_DB.log", "a") as fichier:
                fichier.write(f"{datetime.datetime.now()} | INFO | user : @{message.author} | xp gained : {(10 + 0.01 * message_length):.2f} | channel : {message.channel.id} ({message.channel.name})\n")

        else:
            # Create a new section for the user
            query_insert = f"""
            INSERT INTO levels(id, xp, level, xp_total)
            VALUES({user_id}, 5, 0, 5);
            """
            self.cur.execute(query_insert)

            # Write the user insert into the .log file
            with open("logs\logs_levels_DB.log", "a") as fichier:
                fichier.write(f"{datetime.datetime.now()} | INFO | new user registered : @{message.author}\n")
                

        # Get xp and level infos
        xp_db = self.cur.execute(f"SELECT xp FROM levels WHERE id = {user_id}").fetchone()
        level_db = self.cur.execute(f"SELECT level FROM levels WHERE id = {user_id}").fetchone()

        # Create variables
        xp = xp_db[0]
        level = level_db[0]
        exp_level = 10 * exp(0.2*level)

        # Check if xp is enough for an level up
        if(xp > exp_level):

            # Retrive xp from the user, but not the total xp
            query_levelup = f"""
            UPDATE levels 
            SET xp = xp - {exp_level}, level = level +1 
            WHERE id = {user_id}
            """
            self.cur.execute(query_levelup)

            # Write the user insert into the .log file
            with open("logs\logs_levels_DB.log", "a") as fichier:
                fichier.write(f"{datetime.datetime.now()} | INFO | @{message.author} got to level {level+1}\n")
            await message.channel.send(f"Félicitations {message.author.mention}, vous avez atteint le niveau {level + 1} !")
        
        # Commit all changes
        self.con.commit()



    @commands.command(help = "Display the 5 most experienced users")
    async def topRank(self,ctx):
        """
        Display the top 5 most experienced users
        :param ctx: the context of the message
        """
        xp = [] # Create list for fetching data

        # Fetching the first 5 users into the xp variable
        for row in self.cur.execute("SELECT * FROM levels;").fetchmany(5): 
            user_id = row[0] # Getting user id
            user_lv = row[2] # Getting user level
            user_xp = row[3] # Getting user total xp
            
            xp.append((user_id,user_lv,user_xp)) # Insert data in the list
        
        # make data ready to be displayed
        description = '\n'.join([f'<@{user_id}>: Level {user_lv} ({user_xp:.2f} XP)' for user_id, user_lv, user_xp in xp])

        # Create the embed to display de xp top
        e = nextcord.Embed(
            title="Most 5 experienced users",
            description = description,
            colour=(nextcord.Colour.green())
        )

        await ctx.send(embed=e) # Send th message
    

async def setup(bot):
    """
    function used to setup the class in the bot
    :param bot: the client of the bot
    """
    bot.add_cog(experience(bot))