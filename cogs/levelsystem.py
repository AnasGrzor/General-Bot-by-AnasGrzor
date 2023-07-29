from discord.ext import commands
from bot import MyBot

class LevelSystem(commands.Cog):
    def __init__(self, bot:MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Increase the user's level
        await self.increase_user_level(message.author.id)

    async def get_user_level(self, user_id):
        # Check the user's level
        level = await self.bot.db.fetchval('SELECT level FROM user_levels WHERE user_id = $1', user_id)
        return level

    async def update_user_level(self, user_id, new_level):
        # Update the user's level
        await self.bot.db.execute('''
            INSERT INTO user_levels (user_id, level)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET level = $2;
        ''', user_id, new_level)

    async def increase_user_level(self, user_id):
        current_level = await self.get_user_level(user_id)
        new_level = current_level + 1
        await self.update_user_level(user_id, new_level)

    @commands.command()
    async def level(self, ctx):
        user_id = ctx.author.id

        # Check the user's level
        level = await self.get_user_level(user_id)

        await ctx.send(f'Your level is {level}')

async def setup(bot):
   await bot.add_cog(LevelSystem(bot))
