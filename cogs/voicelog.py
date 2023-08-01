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
        if before.channel != after.channel:
            # User joined or left a voice channel
            if after.channel:
                await self.send_log_message(f"{member.name} joined voice channel {after.channel.name}-{current_time}",discord.Color.green())

            if before.channel:
                await self.send_log_message(f"{member.name} left voice channel {before.channel.name}-{current_time}",discord.Color.red())

           

    async def send_log_message(self, message,color):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            mbed = discord.Embed(description=message,color=color)
            await channel.send(embed=mbed)    

async def setup(bot):
    await bot.add_cog(Voicelog(bot))            