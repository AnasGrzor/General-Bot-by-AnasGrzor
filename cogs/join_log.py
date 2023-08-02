import discord
from discord.ext import commands
from discord.ui import Button,View
import asyncio

class join_log(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.join_log_id = 1135792896717635584

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel_id = 1135795688890966046
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title="User Joined",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green()
        )
        # embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User ID", value=member.id, inline=False)
        await channel.send(embed=embed)

        view = View()
        view.add_item(Button(style=discord.ButtonStyle.red, label="Kick", custom_id=f"kick_{member.id}"))
        view.add_item(Button(style=discord.ButtonStyle.green, label="Ban", custom_id=f"ban_{member.id}"))
        message = await channel.send("Do you want to kick or ban this user?", view=view)

        def check(interaction):
            return interaction.user == member and interaction.message.id == message.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check, timeout=None)
        except asyncio.TimeoutError:
            await message.edit(content="No response received. Test command timed out.", view=None)
            return

        if interaction.custom_id.startswith("kick_"):
            await member.kick(reason="User kicked through button interaction.")
            await interaction.send("User kicked.")
        elif interaction.custom_id.startswith("ban_"):
            await member.ban(reason="User banned through button interaction.")
            await interaction.send("User banned.")

        await message.edit(view=None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testjoin(self, ctx):
        member = ctx.author
        await self.on_member_join(member)

async def setup(bot):
    await bot.add_cog(join_log(bot))

