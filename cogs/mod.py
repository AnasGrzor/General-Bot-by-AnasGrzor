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

    @app_commands.command() #Clears Messages
    @app_commands.checks.has_permissions(manage_messages = True)
    async def clear(self,interaction:discord.Interaction,count : int):
        '''Clear Messages'''
        if count <= 100:
                await interaction.channel.purge(limit=count + 1)
                return await interaction.response.send_message(f"{count} messages have been cleared",ephemeral=True)
        if count > 100:
                return await interaction.response.send_message(embed = discord.Embed(color=discord.Color.red(), title=f"My limit is 100 message"),ephemeral=True)    
    @app_commands.command()
    async def eigth(self,interaction:discord.Interaction,*,question: str):
            with open("respones.txt", "r") as f:
                random_respones = f.readlines()
                respone = random.choice(random_respones)
                
            await interaction.response.send_message(respone)

    @commands.command()
    async def rules(self,ctx):
          await ctx.send('''1. Be Respectful and Inclusive:

Treat all members with respect, regardless of their background, beliefs, or opinions.
Avoid discriminatory language, hate speech, or offensive content.
2. No Harassment or Bullying:

Harassment, bullying, or targeted attacks against any member will not be tolerated.
Report any incidents to the server staff.
3. Keep Conversations Civil:

Engage in discussions constructively and avoid disruptive behavior.
No excessive swearing or spamming.
4. No NSFW Content:

Keep all content safe-for-work (SFW) and appropriate for all age groups.
Do not post or share explicit, sexual, or adult content.
5. Respect Privacy:

Do not share personal information, including addresses, phone numbers, or private conversations, without consent.
6. Use the Right Channels:

Post messages, images, and files in appropriate channels.
Use the 'General' or 'Off-topic' channels for casual discussions.
7. No Advertising or Self-Promotion:

Do not promote other Discord servers, websites, or products without permission.
Exceptions may be allowed with approval from the server staff.
8. English Only in Main Channels:

To ensure a shared understanding, please use English in main channels.
Other languages may be used in specific language channels.
9. Follow Discord Terms of Service:

Abide by the Discord Community Guidelines and Terms of Service.
Discord's rules apply to this server as well.
10. No Spoilers without Warning:

If discussing movies, TV shows, books, or games with spoilers, use the spoiler tag.
Provide ample warning before discussing plot details.
11. Obey Staff and Moderators:

Follow instructions given by the server staff and moderators promptly.
Disputes can be discussed respectfully in private messages.
12. No Raiding or Mass Invites:

Do not engage in server raids or mass invite spamming.
Invite links should be shared responsibly.
13. No Bots without Approval:

Bots can be used with approval from server staff only.
Unauthorized bot usage may result in a ban.
14. No Real Money Transactions:

Do not engage in any form of real-money trading or transactions on this server.
15. Report Violations:

If you witness any rule violations or issues, report them to the server staff via direct message.
These rules are a starting point and can be customized to suit the specific focus and nature of your Discord server. Remember to be clear, concise, and consistent when communicating the rules to the community. Additionally, it's essential to enforce the rules consistently and fairly to maintain a positive and welcoming environment for all members.''')


async def setup(bot):
     await bot.add_cog(Mod(bot))            