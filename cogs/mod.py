import discord
from discord.ext import commands
from datetime import timedelta
from discord import app_commands
import random
from bot import MyBot

class Mod(commands.Cog):
    def __init__(self, bot:MyBot):
        self.bot = bot

    @app_commands.command(name="kick")
    @app_commands.checks.has_permissions(ban_members = True)
    @app_commands.checks.bot_has_permissions(kick_members=True)  
    async def kick(self,interaction:discord.Interaction,member:discord.Member,*, reason: str):
            '''Kick a member'''
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member} has been kicked for `{reason}.")
    @app_commands.command(name="ban")
    @app_commands.checks.has_permissions(ban_members = True)
    @app_commands.checks.bot_has_permissions(ban_members=True) 
    async def ban(self,interaction:discord.Interaction,member:discord.Member,*,reason: str):
        '''Ban a member'''
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} has been banned for `{reason}`.")
    @app_commands.command(name="warn")
    @app_commands.checks.has_permissions(ban_members = True)
    async def warn(self,interaction:discord.Interaction,member:discord.Member,*, reason : str):
        '''Warn a member'''
        await interaction.response.send_message(f"{member} has been warned for `{reason}`")
    @app_commands.command(name="dm")
    @app_commands.checks.has_permissions(ban_members = True)
    async def dm(self,interaction:discord.Interaction,member:discord.Member,*,message : str):
            '''DM A Member'''
            await member.send(message)
            await interaction.response.send_message(f"{message} has been sent to `{member}`")    
    @app_commands.command(name="timeout")
    @app_commands.checks.has_permissions(ban_members = True)
    async def timeout(self,interaction:discord.Interaction,member:discord.Member,minutes : int,reason:str):
        '''Timeout a member'''
        delta = timedelta(minutes=minutes)
        await member.timeout(delta , reason=reason)
        await interaction.response.send_message(f"{member} has been timed out for `{reason}`")

    @app_commands.command(name="slash", description="test slash command")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.")

    @commands.command() #Clears Messages
    @commands.has_permissions(manage_messages = True)
    async def clear(self,ctx,count : int):
        if count <= 100:
                await ctx.channel.purge(limit=count + 1)
                return await ctx.send(f"{count} messages have been cleared")
        if count > 100:
                return await ctx.send(embed = discord.Embed(color=discord.Color.red(), title=f"My limit is 100 message"))    

    @app_commands.command()
    async def eigth(self,interaction:discord.Interaction,*,question: str):
            with open("respones.txt", "r") as f:
                random_respones = f.readlines()
                respone = random.choice(random_respones)
                
            await interaction.response.send_message(respone)

async def setup(bot):
     await bot.add_cog(Mod(bot))            