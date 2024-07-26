import nextcord
from nextcord.ext import commands

class tests(commands.Cog):

    def __init__(self, bot):
        """
        Initialize test class
        :param bot: The bot Discord instancy.
        """
        self.client = bot


    @commands.command(help = "Send message metadata in a terminal")
    async def auto(self,ctx):
        """
        send message characteristics in the terminal
        :param ctx: the context of the message 
        """
        print(ctx.message)
        print(ctx.message.content)
        await ctx.send(f'<@{ctx.author.id}> pong')

    @commands.command(help = "Send message metadata here")
    async def autoCTX(self,ctx):
        """
        send message characteristics in the discord channel
        :param ctx: the context of the message 
        """
        print(ctx.message)
        await ctx.send(f'<@{ctx.author.id}>')
        await ctx.send(ctx)
        await ctx.send(ctx.message)
        await ctx.send(ctx.author)

    @commands.command(help = "Respond, act like a \"ping\"")
    async def hello(self, ctx):
        """
        Print "Bonjour" as a response, like checking if the bot is on
        :param ctx: the context of the message
        """
        await ctx.send("Bonjour")

    @commands.command(help = "replies with what you had sent to the bot")
    async def repeat(self, ctx,*, message):
        """
        # repeat
        ###### bot command
        #### Send exactly the message sent after \"!repeat\"
        - `ctx` : the context of the message
        - `*` : defines `[message]` as all the content
        - `message` : the list of character sent to the bot
        """
        await ctx.reply(f'Venez-vous de dire {message} ?')

    @commands.command(help = "Send a basic embed")
    async def embed(self, ctx):
        """
        # embed
        ###### bot command
        #### Send a sample embed, can be used as a sample for anything
        - `ctx` : the context of the message
        """
        embed = nextcord.Embed(title="Voici un embed", url="https://google.com", description="voici une description", color=0xFF00FF)
        embed.set_author(name= ctx.author.display_name, url="https://youtube.tv", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.add_field(name="Labrador",value="Cute Pyra", inline=True)
        embed.add_field(name="Pyra",value="Cute girl", inline=True)
        embed.set_footer(text="footer of the embed")
        await ctx.send(embed=embed)

async def setup(client):
    """
    function used to setup the class in the bot
    :param client: the client of the bot
    """
    client.add_cog(tests(client))