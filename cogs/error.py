import discord
from discord.ext import commands
from datetime import timedelta
from discord import app_commands
from bot import MyBot

class ErrorCog(commands.Cog):
    def __init__(self, bot:MyBot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self,interaction:discord.Interaction,error:app_commands.AppCommandError):
        if isinstance(error,app_commands.MissingRole):
            role = interaction.guild.get_role(error.missing_role)
            if not role:
                return
            await interaction.response.send_message(f"Missing Role Error - {role.name}")


    @commands.Cog.listener()
    async def on_command_error(self,ctx:commands.Context,error:commands.CommandError):
        if isinstance(error,commands.MissingRequiredArgument):
           return await ctx.send(f"Missing Required argument - {error.param}")
        elif isinstance(error,commands.MissingPermissions):
            perms = ""
            for p in error.missing_permissions:
                perms += f"{p},"
            return await ctx.send(f"You need {perms} to use this command")    
        elif isinstance(error,commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error,commands.CommandNotFound):
            await ctx.send(error)
        elif isinstance(error,commands.CommandInvokeError):
            await ctx.send(error)
        elif isinstance(error,commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error,commands.CommandNotFound):
            await ctx.send(error)
        elif isinstance(error,commands.CommandInvokeError):
            await ctx.send(error)
        elif isinstance(error,commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error,commands.CommandNotFound):
            await ctx.send(error)
        else:
            raise error

async def setup(bot):
     await bot.add_cog(ErrorCog(bot))            