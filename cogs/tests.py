import nextcord
from nextcord.ext import commands

class tests(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def auto(self,ctx): # nom de l'input
        print(ctx.message)
        print(ctx.message.content)
        await ctx.send(f'<@{ctx.author.id}>')

    @commands.command()
    async def autoCTX(self,ctx): # nom de l'input
        print(ctx.message)
        await ctx.send(f'<@{ctx.author.id}>')
        await ctx.send(ctx)
        await ctx.send(ctx.message)
        await ctx.send(ctx.author)

async def setup(client):
    client.add_cog(tests(client))