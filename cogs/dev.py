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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def join(self,ctx:commands.Context):
        # Check if the user is in a voice channel
        if ctx.author.voice is None:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        # Get the voice channel that the user is in
        voice_channel = ctx.author.voice.channel

        # Check if the bot is already in a voice channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(voice_channel)
            await ctx.send(f"Moved to {voice_channel.name}")
        else:
            # Join the voice channel
            voice_client = await voice_channel.connect()
            await ctx.send(f"Joined {voice_channel.name}")
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self,ctx):
        # Check if the bot is in a voice channel
        if ctx.voice_client is None:
            await ctx.send("I am not currently in a voice channel.")
            return    
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")    

async def setup(bot:MyBot):
    await bot.add_cog(Dev(bot))