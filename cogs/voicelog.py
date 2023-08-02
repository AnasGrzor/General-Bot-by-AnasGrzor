import discord
from discord.ext import commands
from bot import MyBot
import datetime
class Voicelog(commands.Cog):
    def __init__(self,bot:MyBot):
        self.bot = bot
        self.channel_id = 1135687031415132271

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        current_time = datetime.datetime.now().strftime('%H:%M')
        if member == self.bot.user:
            return
        if before.channel != after.channel:
            if after.channel and before.channel:
                # User switched voice channels
                await self.send_log_message(f"{member.name} switched from {before.channel.mention} to {after.channel.mention}-{current_time}", discord.Color.blue())
                # User joined a voice channel 
            elif after.channel:
                await self.send_log_message(f"{member.name} joined voice channel {after.channel.mention}-{current_time}",discord.Color.green())
                # User left a voice channel
            elif before.channel:
                await self.send_log_message(f"{member.name} left voice channel {before.channel.mention}-{current_time}",discord.Color.red())


           

    async def send_log_message(self, message,color):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            mbed = discord.Embed(description=message,color=color)
            await channel.send(embed=mbed)    

async def setup(bot):
    await bot.add_cog(Voicelog(bot))            