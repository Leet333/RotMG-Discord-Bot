import discord, aiohttp, asyncio
from discord.ui import View
from discord.ext import commands
from utilities.context import Context
from utilities import utils, items

class realmeye(commands.Cog):
    """RealmEye integration"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name = "realmeye",
        description = "Interact with RealmEye through the bot",
        usage = "```Syntax: !realmeye <subcommand> <args>\nExample: !realmeye player Leet```"
    )
    async def realmeye(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return await utils.realmeye_help(ctx)
    
    @realmeye.command(
        name = "player",
        description = "Search for a player",
        usage = "```Syntax: !realmeye player <ign>\nExmaple: !realmeye player Leet```"
    )
    async def realmeye_player(self, ctx: Context, ign: str):
        player_info = await utils.search_player(ign)
        await ctx.paginate(player_info)

    @realmeye.command(
        name = "guild",
        description = "Search for a guild (case sensitive!)",
        usage = "```Syntax: !realmeye guild <name>\nExmaple: !realmeye guild Eldia```"
    )
    async def realmeye_guild(self, ctx: Context, *, guild: str):
        guild_info = await utils.search_guild(guild.replace(' ', '+'))
        await ctx.paginate(guild_info)
    
    @realmeye.command(
        name = "item",
        description = "Search for an item",
        usage = "```Syntax: !realmeye item <name>\nExmaple: !realmeye item Divinity```"
    )
    async def realmeye_item(self, ctx: Context, *, item: str):
        input = await items.replace_aliases(item)
        item = input.replace(" ", "-").replace("'", "-")
        item_info = await utils.search_item(item)
        await ctx.reply(embed = item_info, mention_author = False)
    
    @realmeye.command(
        name = "characters",
        description = "View a players characters",
        usage = "```Syntax: !realmeye characters <IGN>\nExmaple: !realmeye characters Leet```",
        aliases = ['chars', 'sets']
    )
    async def realmeye_characters(self, ctx: Context, ign: str):
        async with aiohttp.ClientSession() as sesh:
            async with sesh.get(f"https://realmeye-api.glitch.me/player/{ign}") as resp:
                data = await resp.json()

        characters = [discord.SelectOption(label = f"{char['character']}", value = f"{char['character']}") for char in data["CharacterInfo"]]
        if not characters:
            return await ctx.error(f"{ign} doesn't have any characters")
        
        async def select_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message(
                    embed = discord.Embed(
                        color = 0xED4245,
                        description = "You can't interact with this"
                    ),
                    ephemeral = True
                )
            
            class_set = await utils.file(
                url = f"https://realmeye-api.glitch.me/player/{ign}/{dropdown.values[0]}/set", 
                filename = f"{ign}-{dropdown.values[0]}.png"
            )
            char_items = "\n".join(f"> **{item_type.capitalize()}:** {item['title']}"
                for character in data["CharacterInfo"]
                if character['character'] == dropdown.values[0]
                for item_type, item in zip(["Weapon", "Ability", "Armor", "Ring"], character['items']
                )
            )

            embed = discord.Embed(
                color = 0x2F3136,
                title = f"{ign}'s {dropdown.values[0]}",
                url = f'https://www.realmeye.com/player/{ign}',
                description = char_items
            )
            await msg.edit(embed = embed, view = view)
            await msg.add_files(class_set)
            return await interaction.response.defer()

        async def on_timeout():
            await asyncio.sleep(300)
            dropdown.disabled = True
            return await msg.edit(view = view)
        
        iembed = discord.Embed(
            color = 0x2F3136,
            title = f"Character Viewer • {ign}",
            url = f'https://www.realmeye.com/player/{ign}',
            description = f"> **{ign}** has **{data['ProfileInfo']['Characters']}** characters\n> Use the dropdown menu to view a character"
        )
        dropdown = discord.ui.Select(options = characters, placeholder = "select a character", max_values = 1)
        dropdown.callback = select_callback
        view = View()
        view.add_item(dropdown)
        on_timeout = asyncio.create_task(on_timeout())

        msg = await ctx.reply(embed = iembed, view = view, mention_author = False)

async def setup(bot):
    await bot.add_cog(realmeye(bot))