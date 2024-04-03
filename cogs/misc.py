import discord, copy
from discord.ext import commands
from utilities.context import Context
from utilities import utils

class misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "help",
        description = "View all commands or information on a command",
        usage = "```Syntax: !help <command>\nExample: !help realmeye```"
    )
    async def _help(self, ctx: Context, *, command: str = None):
        if command:
            if not self.bot.get_command(command):
                return await ctx.error("Please provide a valid command")
            
            alt_ctx = copy.copy(ctx)
            alt_ctx.command = self.bot.get_command(command)
            return await utils.send_help(alt_ctx)
        
        embed = discord.Embed(
            title = "Rotmg Bot Help Menu",
            color = 0x2F3136
        )
        embed.add_field(
            name = "Important Info",
            value = "`!help [command]` for more info on a command\n<> = required, [] = optional"
        )
        embed.add_field(
            name = "Commands (6)",
            value = "```realmeye, realmeye player, realmeye guild, realmeye item, realmeye characters, ppe```",
            inline = False
        )

        return await ctx.reply(embed = embed, mention_author = False)
    
    @commands.command(
        name = "ppe",
        description = "Chooses a random class for you",
        usage = "```Syntax: !ppe\nExample: !ppe```"
    )
    async def ppe(self, ctx: Context):
        chosen_class = await utils.random_class()
        class_img = await utils.check_rotmg_class(chosen_class.capitalize())

        embed = discord.Embed(
            color = 0x2F3136,
            title = "Class Selector",
            description = f"> you got **{chosen_class}**"
        )
        embed.set_image(url = class_img)
        embed.set_footer(text = "good luck!")

        return await ctx.reply(embed = embed, mention_author = False)

async def setup(bot):
    await bot.add_cog(misc(bot))