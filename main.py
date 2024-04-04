import discord, traceback
from discord.ext import commands
from utilities.config import Authorization
from utilities.context import Context

class RotmgBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cogs_loaded = False

    async def get_context(self, message, *, cls = Context):
        return await super().get_context(message, cls = cls)

bot = RotmgBot(
    command_prefix = Authorization.prefix,
    case_insensitive = True,
    activity = discord.Game(name = Authorization.status),
        intents = discord.Intents.all()
    )

cogs = [
    "realmeye",
    "configuration",
    "misc"
]

bot.remove_command("help")

@bot.event
async def on_ready():
    if not bot.cogs_loaded:
        await load_cogs()
    print("Bot Connected")

async def load_cogs():
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
        except Exception as error:
            print(f"Error loading [ {cog} ]")
            traceback.print_exception(type(error), error, error.__traceback__)
    bot.cogs_loaded = True

bot.run(Authorization.token, reconnect = True)
