from discord.ext import commands
import discord
from bot import MyBot

class LevelSystem(commands.Cog):
    def __init__(self, bot:MyBot):
        self.bot = bot
        self.xp_per_message = 10

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return


        # Increase the user's level
        await self.increase_user_xp(message.author.id,self.xp_per_message)



    async def get_user_level(self, user_id):
        # Check the user's level
        level = await self.bot.db.fetchval('SELECT level FROM user_levels WHERE user_id = $1', user_id)
        return level
    
    async def get_user_xp(self, user_id):
        # Check the user's level
        xp = await self.bot.db.fetchval('SELECT user_xp FROM user_levels WHERE user_id = $1', user_id)
        return xp

    async def update_user_xp(self, user_id, xp_amount):
        await self.bot.db.execute('''
            INSERT INTO user_levels (user_id, user_xp)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET user_xp = $2;
        ''', user_id, xp_amount)

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
        if current_level is not None:
            new_level = current_level + 1
        else:
            new_level = 1    
        await self.update_user_level(user_id, new_level)

         # Check if the user leveled up
        if current_level is not None and new_level > current_level:
            # The user leveled up, send a congratulatory message in the same channel
            user = self.bot.get_user(user_id)
            if user:
                congrats_message = f"Congratulations {user.mention}! You've reached level {new_level}!"
                channel = self.bot.get_channel(user.last_message.channel.id)
                if channel:
                    await channel.send(congrats_message)

    async def increase_user_xp(self, user_id, xp_amount):
        current_xp = await self.get_user_xp(user_id)

        if current_xp is not None:
            new_xp = current_xp + xp_amount
        else:
            new_xp = xp_amount

        await self.update_user_xp(user_id, new_xp)    
    @staticmethod
    def get_required_xp_for_next_level(current_level):
    # Define the required XP for each level. You can adjust this based on your leveling system.
        xp_per_level = 100  # Change this value as needed.

    # Calculate the required XP for the next level.
        required_xp = (current_level + 1) * xp_per_level
        return required_xp



    @commands.command()
    async def level(self, ctx):
        user_id = ctx.author.id

        # Check the user's level
        level = await self.get_user_level(user_id)
        # Calculate required XP for the next level
        required_xp =  self.get_required_xp_for_next_level(level)
        current_xp = await self.get_user_xp(user_id)
        # await ctx.send(f'Your level is {level}.You need {required_xp} xp to level up. Your current XP is {current_xp}')
        boxes = int((current_xp / (200 * ((1/2) * (level))) * 20))
        embed = discord.Embed(title = "{}'s level stats".format(ctx.author.name), description="", color= 0x397882)
        embed.add_field(name="Name", value=ctx.author.mention, inline=True)
        embed.add_field(name="XP", value=f"{current_xp}/{int(200 *(1/2) *level)}", inline=True)
        embed.add_field(name="Level", value=level, inline=True)
        # embed.add_field(name="Rank", value=f"{rank+1}/{ctx.guild.member_count}", inline=True)
        embed.add_field(name="Progress Bar [lvl]", value=boxes*":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        # Fetch the top N users from the database, sorted by level or XP (you can adjust the query as needed)
        top_users = await self.bot.db.fetch('''
            SELECT user_id, level, user_xp FROM user_levels
            ORDER BY level DESC, user_xp DESC
            LIMIT 10  -- Show top 10 users, adjust the number as needed
        ''')

        # Create an embed to display the rank
        embed = discord.Embed(title="Leaderboard", color=discord.Color.blurple())

        # Iterate through the top_users and add their rank, level, and XP to the embed
        for index, (user_id, level, xp) in enumerate(top_users, start=1):
            # Get the user object from the user_id
            user = self.bot.get_user(user_id)
            if user:
                # Add the user's rank, username, level, and XP to the embed
                embed.add_field(name=f"#{index} - {user.name}", value=f"Level: {level} | XP: {xp}", inline=False)

        # Send the leaderboard as a message
        await ctx.send(embed=embed)


async def setup(bot):
   await bot.add_cog(LevelSystem(bot))
