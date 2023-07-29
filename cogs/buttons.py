import discord
from discord.ui import Button,View,Select
from discord.ext import commands
from bot import MyBot

class MySelect(Select):
        async def callback(self,interaction:discord.Interaction):
            await interaction.response.send_message(f"You chose {self.values}")

class MyView(View):
    def __init__(self,ctx:commands.Context):
        super().__init__(timeout=5)
        self.ctx = ctx

    @discord.ui.button(label="Click Me",style=discord.ButtonStyle.green,emoji="👍")
    async def button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        button = [x for x in self.children if x.custom_id=="danger"][0]
        button.label = "No more danger!!!!"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
        

    @discord.ui.button(label="Danger",style=discord.ButtonStyle.red,custom_id="danger")
    async def danger_button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        await self.ctx.send("Timeout")
        return

class MyButtons(commands.Cog):
    def __init__(self,bot):
        self.bot = bot    

    @commands.command()
    async def hello(self,ctx:commands.Context):
        view = MyView(ctx)
        await ctx.send("hi",view=view)
        await view.wait()

    @commands.command()
    async def weather(self,ctx:commands.Context):
        select = MySelect(
            min_values=1,
            max_values=4,
            placeholder="Choose a Weather",
            options=[
                discord.SelectOption(
                    label="Cloudy",
                    emoji = "🌤",
                    description="Cloudy",
                ),
                discord.SelectOption(
                    label="Rainy",
                    emoji = "🌧",
                    description="Its raining",
                ),
                discord.SelectOption(
                    label="Sunny",
                    emoji = "☀️",
                    description="Sunny",
                ),
                discord.SelectOption(
                    label="Thunder",
                    emoji = "⛈️",
                    description="Thunderstorm BE CAREFUL!!!",
                )            
            ]
        )

        view = View()
        view.add_item(select)
        await ctx.send("Choose a weather",view=view)


async def setup(bot):
    await bot.add_cog(MyButtons(bot))        
