import discord
from discord.ext import commands 
from bot import MyBot

class Test(commands.Cog):
    def __init__(self,bot:MyBot):
        self.bot = bot

    @commands.command()
    async def test(self,ctx:commands.Context):
        await self.bot.db.execute("INSERT INTO test_table VALUES ($1,$2)",ctx.guild.id,"Hello My name is Custom bot")    
        return await ctx.send("Done")


    @commands.command()
    async def hi(self,ctx:commands.Context):
        record = await self.bot.db.fetchval("SELECT response FROM test_table WHERE server_id = $1",ctx.guild.id)    
        if not record:
            return await ctx.send("Please set a response using the setHi command")
        else:
            return await ctx.send(record)    

    @commands.command()
    async def setHi(self,ctx:commands.Context,*,text: str):
        record = await self.bot.db.fetchval("SELECT * FROM test_table WHERE server_id = $1",ctx.guild.id)    
        if not record:
            return await ctx.send("No record found")
        await self.bot.db.execute("UPDATE test_table SET response = $1 WHERE server_id = $2",text,ctx.guild.id) 
        return await ctx.send("Done")


async def setup(bot):
   await bot.add_cog(Test(bot))        