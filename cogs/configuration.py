import discord, copy, aiosqlite
from discord.ext import commands
from utilities.context import Context
from utilities import utils

class configuration(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name = "raidchannel",
        description = "Configure the raid channel",
        usage = "```Syntax: !raidchannel <subcommand> [args]\nExample: !raidchannel add #o3-runs```",
        aliases = ['rc']
    )
    async def raidchannel(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return await utils.send_help(ctx)
    
    @raidchannel.command(
        name = "add",
        description = "Adds a channel to the raid channels",
        usage = "```Syntax: !raidchannel add <channel>\nExample: !raidchannel add #o3-runs```"
    )
    async def raidchannel_add(self, ctx: Context, *, channel: discord.TextChannel):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id FROM channels WHERE guild_id = ?", (ctx.guild.id,))
            data = await cursor.fetchall()

            for row in data:
                if row[0] == channel.id:
                    return await ctx.error(f"{channel.mention} is already a raid channel")

            await cursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (ctx.guild.id, channel.id, channel.name))
            await ctx.success(f"Added {channel.mention} as a raid channel")
        return await self.bot.db.commit()

    @raidchannel.command(
        name = "remove",
        description = "Removes a channel from the raid channels",
        usage = "```Syntax: !raidchannel remove <channel>\nExample: !raidchannel remove #o3-runs```"
    )
    async def raidchannel_remove(self, ctx: Context, *, channel: discord.TextChannel):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id FROM channels WHERE guild_id = ?", (ctx.guild.id,))
            data = await cursor.fetchall()

            for row in data:
                if row[0] == channel.id:
                    await cursor.execute("DELETE FROM channels WHERE channel_id = ? AND channel_name = ? AND guild_id = ?", (channel.id, channel.name, ctx.guild.id))
                    await self.bot.db.commit()
                    return await ctx.success(f"{channel.mention} is no longer a raid channel")

            await ctx.success(f"{channel.mention} isn't a raid channel")
        return await self.bot.db.commit()

async def setup(bot):
    await bot.add_cog(configuration(bot))