import discord
from discord.ext import commands
from utilities.context import Context
from datetime import datetime

# TODO
# Add abort button to panel embed instead of headcount embed
# Add button to convert headcount to an afk check

class headcount(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def disable_button(self, view: discord.ui.View, label: str):
        for item in view.children:
            if isinstance(item, discord.ui.Button) and item.label == label:
                item.disabled = True
                return True
        return False

    @commands.command(
        name="headcount",
        description="Start an Oryx's Sanctuary headcount",
        usage="```Syntax: !headcount\nExample: !headcount```",
        aliases=['hc']
    )
    async def headcount(self, ctx: Context):
        helm, sword, shield, inc = 0, 0, 0, 0
        helm_users, sword_users, shield_users, inc_users = [], [], [], []

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id, channel_name FROM channels WHERE guild_id = ?", (ctx.guild.id,))
            data = await cursor.fetchall()
            if not data:
                return await ctx.error("No raid channel found")

            options = [discord.SelectOption(label = f"{channel[1]}", value = f"{channel[0]}") for channel in data]
            dropdown = discord.ui.Select(placeholder = "select a channel", options = options, max_values = 1)

            async def dropdown_callback(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message(
                        embed = discord.Embed(description = "You can't interact with this", color = 0xED4245),
                        ephemeral=True
                    )
                async def close_callback(interaction: discord.Interaction):
                    if interaction.user.id != ctx.author.id:
                        return await interaction.response.send_message(
                            embed = discord.Embed(description = "You can't interact with this", color = 0xED4245),
                            ephemeral = True
                        )
                    await hc_msg.edit(content = f"Headcount closed by {interaction.user.name}", view = None)
                    headcount_view.stop()
                    embed = discord.Embed(
                        title = "Oryx Sanctuary Headcount Closed",
                        description = "Headcount was closed",
                        color = 0x2F3136
                    )
                    for name, users in [("Helmet Reacts", helm_users), ("Sword Reacts", sword_users), ("Shield Reacts", shield_users), ("Incantation Reacts", inc_users)]:
                        react_list = " | ".join([f'<@{user}>' for user in users]) if users else "N/A"
                        embed.add_field(name = name, value = f"> {react_list}", inline = False)
                    embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar)
                    embed.set_thumbnail(url = "https://i.imgur.com/DSVqdZo.png")
                    return await msg.edit(content = None, embed = embed, view = None)

                async def reaction_callback(interaction: discord.Interaction, confirmed: bool, rune_type: str):
                    users = {
                        "Helmet Rune": helm_users,
                        "Sword Rune": sword_users,
                        "Shield Rune": shield_users,
                        "Incantation": inc_users
                    }.get(rune_type)

                    if confirmed:
                        response_embed = discord.Embed(description = "You already reacted to this", color = 0xE8D46E) if interaction.user.id in users else discord.Embed(description = "Thank you!", color = 0x85ED91)
                        if interaction.user.id not in users:
                            nonlocal helm, sword, shield, inc
                            count = {"Helmet Rune": helm, "Sword Rune": sword, "Shield Rune": shield, "Incantation": inc}.get(rune_type)
                            count += 1
                            if count >= 3:
                                await self.disable_button(headcount_view, rune_type)
                                await hc_msg.edit(embed = headcount_embed, view = headcount_view)

                            users.append(interaction.user.id)
                            helm = count if rune_type == "Helmet Rune" else helm
                            sword = count if rune_type == "Sword Rune" else sword
                            shield = count if rune_type == "Shield Rune" else shield
                            inc = count if rune_type == "Incantation" else inc

                            headcount_embed.set_field_at(
                                index = 0,
                                name = "Reactions",
                                value = f"> <:HelmRune:1103743073818779709> : {helm}\n> <:SwordRune:1103743059260358696> : {sword}\n> <:ShieldRune:1103743046958460978> : {shield}\n> <:Inc:1225238958242529372> : {inc}"
                            )
                            await hc_msg.edit(embed = headcount_embed)
                        await interaction.response.edit_message(embed = response_embed, view = None)
                    else:
                        await interaction.response.edit_message(embed = discord.Embed(description = "Cancelled reaction", color = 0x2F3136), view = None)

                async def create_button_callback(rune_type: str):
                    async def button_callback(interaction: discord.Interaction):
                        Yes = discord.ui.Button(style=discord.ButtonStyle.green, label = "Yes", custom_id = "yes")
                        No = discord.ui.Button(style=discord.ButtonStyle.red, label = "Cancel", custom_id = "no")
                        Yes.callback = lambda i: reaction_callback(i, True, rune_type)
                        No.callback = lambda i: reaction_callback(i, False, rune_type)
                        view = discord.ui.View(timeout=180)
                        view.add_item(Yes)
                        view.add_item(No)

                        return await interaction.response.send_message(embed = discord.Embed(description="Are you sure you want to react?", color = 0x2F3136), view = view, ephemeral = True)
                    return button_callback

                buttons = [
                    ("<:HelmRune:1103743073818779709>", "Helmet Rune"),
                    ("<:SwordRune:1103743059260358696>", "Sword Rune"),
                    ("<:ShieldRune:1103743046958460978>", "Shield Rune"),
                    ("<:Inc:1225238958242529372>", "Incantation")
                ]

                raid_channel = await self.bot.fetch_channel(dropdown.values[0])

                headcount_view = discord.ui.View(timeout = 900)
                for emoji, label in buttons:
                    button = discord.ui.Button(style=discord.ButtonStyle.green, emoji = emoji, label = label)
                    button.callback = await create_button_callback(label)
                    headcount_view.add_item(button)

                closeButton = discord.ui.Button(style = discord.ButtonStyle.red, label = "Close")
                closeButton.callback = close_callback
                headcount_view.add_item(closeButton)

                headcount_embed = discord.Embed(
                    title = "Oryx Sanctuary Headcount",
                    description = "> If you have any runes please react below!",
                    timestamp = datetime.now(),
                    color = 0x2F3136
                )
                headcount_embed.add_field(
                    name = "Reactions",
                    value = f"> <:HelmRune:1103743073818779709> : {helm}\n> <:SwordRune:1103743059260358696> : {sword}\n> <:ShieldRune:1103743046958460978> : {shield}\n> <:Inc:1225238958242529372> : {inc}"
                )
                headcount_embed.set_author(name = f"{interaction.user.name}'s headcount", icon_url = interaction.user.display_avatar)
                headcount_embed.set_thumbnail(url = "https://i.imgur.com/DSVqdZo.png")
                hc_msg = await raid_channel.send("@here", embed = headcount_embed, view = headcount_view)
                dropdown_view.clear_items()
                dropdown_view.stop()
                panel_embed.description = f"> Headcount sent to {raid_channel.mention}"
                await msg.edit(embed = panel_embed, view = None)
                await interaction.response.defer()

            async def close_panel_callback(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message(
                        embed=discord.Embed(description = "You can't interact with this", color = 0xED4245),
                        ephemeral=True
                    )
                panel_embed.description = "Closed the panel"
                await msg.edit(embed = panel_embed, view = None)
                dropdown_view.stop()

            close_button = discord.ui.Button(style = discord.ButtonStyle.red, label = "close panel")
            dropdown.callback = dropdown_callback
            close_button.callback = close_panel_callback
            dropdown_view = discord.ui.View()
            dropdown_view.add_item(dropdown)
            dropdown_view.add_item(close_button)
            panel_embed = discord.Embed(
                title = "Oryx Sanctuary Headcount",
                description = "Use the dropdown menu to send a headcount",
                color = 0x2F3136
            )
            panel_embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar)
            panel_embed.set_thumbnail(url = "https://i.imgur.com/DSVqdZo.png")
            msg = await ctx.reply(embed = panel_embed, view = dropdown_view, mention_author = False)

async def setup(bot):
    await bot.add_cog(headcount(bot))