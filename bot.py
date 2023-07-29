import discord
from discord.ext import commands
from discord.ui import View
import config
import asyncpg

exts = ["cogs.mod","cogs.test","cogs.error","cogs.welcome","cogs.dev","cogs.buttons","cogs.ticket","cogs.levelsystem"]

class MyBot(commands.Bot):
    def __init__(self,command_prefix : str,intents:discord.Intents,**kwargs):
        super().__init__(command_prefix,intents=intents,**kwargs) 
   
    async def setup_hook(self):
        try:
            self.db = await asyncpg.create_pool(config.DB_Token,min_size=4,max_size=5)
            print("Connected to database")
        except Exception as e:
            print("Failed to connect to database. {0}".format(e))
        try:
            with open("schemas.sql") as f:
                await self.db.execute(f.read())
                print("Excuted schema")
        except Exception as e:
            print("Failed to excute schema. {0}".format(e))        

        try:
            for ext in exts:
                await self.load_extension(ext)
            print("Loaded All Cogs!")
        except Exception as e:
            print("Failed to load Cogs. {0}".format(e))    

    async def on_ready(self):
        print("Bot is ready")
        print(f"Logged in as {self.user} ID: {self.user.id}")
        await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type = discord.ActivityType.listening, name = "\help" ))


if __name__ == "__main__":
    bot = MyBot(command_prefix="-",intents=discord.Intents.all())
    bot.run(config.token)