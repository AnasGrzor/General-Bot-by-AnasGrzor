import discord
from discord.ext import commands
from bot import MyBot

class Dev(commands.Cog):
    def __init__(self,bot:MyBot):
        self.bot = bot
        
    @commands.command(hidden=True)    
    @commands.is_owner()
    async def sync(self,ctx:commands.Context):
        await self.bot.tree.sync()
        await ctx.send("Synced")

async def setup(bot:MyBot):
    await bot.add_cog(Dev(bot))