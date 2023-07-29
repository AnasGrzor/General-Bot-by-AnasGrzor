import discord
from discord.ui import Button,View
from discord.ext import commands
from bot import MyBot
import asyncio

class CreateTicket(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket",style=discord.ButtonStyle.green,emoji="🎫",custom_id="ticketopen")
    async def ticket(self,interaction:discord.Interaction,button:discord.ui.Button):
        button.disabled = True
        await interaction.response.defer(ephemeral=True)
        category:discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1134236536687317134)
        self.stop()

        r1 : discord.Role = interaction.guild.get_role(736309728652558387)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True,send_messages=True,manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True,send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
        }       
        channel = await category.create_text_channel(
            name = str(interaction.user),
            topic = f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL",
            overwrites = overwrites
        )      
        await channel.send(
            embed = discord.Embed(
            title="Ticket Created!",
            description="Dont ping a staff member, they will be here soon",
            color=discord.Color.green()
            ),view=Close()
        )
        await interaction.followup.send(
            embed = discord.Embed(
                description="Ticket Created! in {0}".format(channel.mention),
                color=discord.Color.red()
            ),
            ephemeral=True
        )

class Close(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket",style=discord.ButtonStyle.danger,emoji="🔒",custom_id="ticketclose")
    async def close(self,interaction:discord.Interaction,button:Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Ticket Closeing in 3s")
        await asyncio.sleep(3)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1134262083995828275)
        r1 : discord.Role = interaction.guild.get_role(736309728652558387)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True,send_messages=True,manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
        }
        await interaction.channel.edit(category=category)
        await interaction.channel.send(
            embed = discord.Embed(
            title="Ticket Closed!",
            color=discord.Color.red()
            ), view = Trash()
        )


class Trash(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete Ticket",style=discord.ButtonStyle.danger,emoji="🗑️",custom_id="trash")
    async def trash(self,interaction:discord.Interaction,button:Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.delete()

class Ticket(commands.Cog):
    def __init__(self,bot:MyBot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket(self,ctx:commands.Context):
        view = CreateTicket()
        await ctx.send(
            embed = discord.Embed(
                description="Press the button to create a new ticket"
            ),view = view   
        )

async def setup(bot):
    await bot.add_cog(Ticket(bot))        
