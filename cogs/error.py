import discord
from discord.ext import commands
from datetime import timedelta
from discord import app_commands
from bot import MyBot

channel_id = 1131616288381353984
class ErrorCog(commands.Cog):
    def __init__(self, bot:MyBot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error
        self.error_logs_channel_id = 1135792896717635584

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
            await ctx.send("This command is on cooldown")
        elif isinstance(error,commands.CommandNotFound):
            await ctx.send("This command does not exist")
        elif isinstance(error,commands.CommandInvokeError):
            await ctx.send("Something went wrong")
        elif isinstance(error,commands.CheckFailure):
            channel = self.bot.get_channel(channel_id)
            await ctx.send(f"Please use bot commands in {channel.mention}")
        else:
            await ctx.send("Something went wrong")

        # Send the error message to the error logs channel
        error_logs_channel = self.bot.get_channel(self.error_logs_channel_id)
        if error_logs_channel:
            await error_logs_channel.send(f"An error occurred while running a command:\n```\n{error}\n```")
        else:
            # If the error logs channel is not found, send the error message to the command's channel
            await ctx.send(f"An error occurred while running the command:\n```\n{error}\n```")

async def setup(bot):
     await bot.add_cog(ErrorCog(bot))            