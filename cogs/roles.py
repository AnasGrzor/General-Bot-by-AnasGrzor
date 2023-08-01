import discord
from discord.ext import commands
import discord.ui
# from bot import MyBot

# class AssignRole(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @discord.ui.button(label="Verify",custom_id="Role 1",style=discord.ButtonStyle.green)    
#     async def verify(self,interaction:discord.Interaction,button:discord.ui.Button):
#         role_id = 1135721201080205493
#         user = interaction.user
#         role = interaction.guild.get_role(role_id)
#         if role is not None:
#             if role in user.roles:
#                 button.disabled = True
#                 await interaction.response.send_message(f"You already have this {role} role ",ephemeral=True)
#             else:
#                 await user.add_roles((role))
#                 await interaction.response.send_message(f"Role {role} added",ephemeral=True)    

#             await interaction.message.delete()          

class AssignRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.role_id = 1135721201080205493
        self.role = None
        self.user_has_role = False
        self.clicked_users = set()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.role is None:
            self.role = interaction.guild.get_role(self.role_id)
            if self.role is not None:
                self.user_has_role = self.role in interaction.user.roles

        return await super().interaction_check(interaction)

    @discord.ui.button(label="Verify", custom_id="Role 1", style=discord.ButtonStyle.green)    
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user_has_role:
            await interaction.response.send_message(f"You already have the role {self.role.mention}", ephemeral=True)
        elif interaction.user.id in self.clicked_users:
            await interaction.response.send_message("You have already clicked the button.", ephemeral=True)
        else:
            # Add the role to the user
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"Role {self.role.mention} added", ephemeral=True)
            self.clicked_users.add(interaction.user.id)

        # Delete the button only for the user
        button.disabled = True



class Roles(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def verify(self,ctx:commands.Context):
        view = AssignRole()
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))        
