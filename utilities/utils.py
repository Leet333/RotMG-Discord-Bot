import discord, aiohttp, random
from io import BytesIO
from discord.ext import commands

async def send_help(ctx):
	if isinstance(ctx.command, commands.Command):
		embed = discord.Embed(color=0x2F3136)
		embed.set_author(
			name="rotmg bot help", 
			icon_url="https://cdn.discordapp.com/avatars/547882297710608388/e019b8ebfd437d210b3917e8341706cc.png?size=4096"
		)
		if ctx.command.aliases:
			embed.set_footer(
				text = "Aliases: " + ", ".join(ctx.command.aliases)
			)
		else:
			embed.set_footer(
				text = "Aliases: N/A"
			)
		if ctx.command.description:
			embed.description = f"{ctx.command.description}" + f"\n{ctx.command.usage}" if ctx.command.usage else f"{ctx.command.description}"
		
		return await ctx.reply(embed=embed, mention_author = False)

async def realmeye_help(ctx):
	if isinstance(ctx.command, commands.Command):
		embed = discord.Embed(color=0x2F3136)
		embed.set_author(
			name = "rotmg bot help", 
			icon_url = "https://cdn.discordapp.com/avatars/547882297710608388/e019b8ebfd437d210b3917e8341706cc.png?size=4096"
		)
		if ctx.command.aliases:
			embed.set_footer(
				text = "Aliases: " + ", ".join(ctx.command.aliases)
			)
		else:
			embed.set_footer(
				text = "Aliases: N/A | Powered by andr123's RealmEye API"
			)
		if ctx.command.description:
			embed.description = f"{ctx.command.description}\n{ctx.command.usage}"
		
		embed.add_field(
			name = "Commands",
			value = "> `realmeye item` - Search for an item\n> `realmeye player` - Search for a player\n> `realmeye characters` - View a players characters\n> `realmeye guild` - Get info on a guild (case sensitive)",
			inline = False
		)

		return await ctx.reply(embed = embed, mention_author = False)
	
async def search_player(ign: str):
    """Grabs information about a player from RealmEye"""
    
    async with aiohttp.ClientSession() as sesh:
        async with sesh.get(f"https://realmeye-api.glitch.me/player/{ign}") as resp:
            data = await resp.json()
            if not data.get("ProfileInfo"):
                fail_embed = discord.Embed(
                    description = f"Unable to find that player", 
                    color = 0xE8D46E
                )
                return fail_embed
            
    embeds = []

    ranks = {
        "17" : "<:lightblue:1100456654748790925>",
        "35" : "<:darkblue:1100456714316292198>",
        "53" : "<:redstar:1100456743294746635>",
        "71" : "<:orangestar:1100456782599573585>",
        "89" : "<:yellowstar:1100456827008852061>",
        "90" : "<:whitestar:1100457095595307109>",
    }
    player_rank = data['ProfileInfo']['Rank']
    for rank, star in ranks.items():
        if int(player_rank) <= int(rank):
            player_rank += star
            break

    basic_info = f"> **Stars:** {player_rank}"
    basic_info += f"\n> **First Seen:** `{data['ProfileInfo'].get('FirstSeen', 'hidden')}`"
    basic_info += f"\n> **Last Seen:** `{data['ProfileInfo']['LastSeen']}`\n> **Guild:** [{data['ProfileInfo'].get('Guild', 'N/A')}](https://www.realmeye.com/guild/{data['ProfileInfo'].get('Guild', '').replace(' ', '%20')}) ({data['ProfileInfo'].get('GuildRank', 'N/A')})"

    embed1 = discord.Embed(
        title = f"{data['ProfileInfo']['PlayerName']}'s Realmeye", 
        description = basic_info, 
        url = f'https://www.realmeye.com/player/{ign}', 
        color = 0x2F3136
    )
    embed1.add_field(
        name = "Overview",
        value = f"> **Characters:** {data['ProfileInfo']['Characters']}\n> **Exalts:** {data['ProfileInfo']['Exaltations']}\n> **Fame:** {data['ProfileInfo']['Fame']}",
        inline = True
    )
    embed1.set_thumbnail(
        url = 'https://www.realmeye.com/s/fa/img/eye-big.png'
    )

    if len(data["CharacterInfo"]) != 0:
        embed1.set_footer(
            text = f"character info on the next page"
        )
    embeds.append(embed1)

    for event in data["CharacterInfo"]:
        embed = discord.Embed(
            title = f"{data['ProfileInfo']['PlayerName']}'s Realmeye • {event['character']}",
            url = f"https://www.realmeye.com/player/{ign}", 
            color = 0x2F3136
        )

        class_img = await check_rotmg_class(str(event['character']))

        embed.set_thumbnail(
            url=class_img,
        )
        embed.add_field(
            name = "Overview",
            value = f"> **Level:** {event['level']}\n> **Fame:** {event['fame']}\n> **Position:** {event['pos']}",
            inline = False,
        )
        embed.add_field(
            name = "Items",
            value = f"> **Weapon:** {event['items'][0]['title']}\n> **Ability:** {event['items'][1]['title']}\n> **Armor:** {event['items'][2]['title']}\n> **Ring:** {event['items'][3]['title']}",
            inline = False,
        )
        embed.set_footer(
            text = f"Page {data['CharacterInfo'].index(event)+1}/{len(data['CharacterInfo'])} ({len(data['CharacterInfo'])} {'entries' if len(data['CharacterInfo']) > 1 else 'entry'})"
         )
        embed.timestamp
        embeds.append(embed)

    return embeds

async def search_guild(guild: str):
    """Grabs information about a guild from RealmEye"""

    async with aiohttp.ClientSession() as sesh:
        async with sesh.get(f"https://realmeye-api.glitch.me/guild/{guild}") as resp:
            data = await resp.json()
            if not data.get("Guild"):
                fail_embed = discord.Embed(
                    description = f"> Unable to find that guild", 
                    color = 0xE8D46E
                )
                return fail_embed
    embeds = []

    embed1 = discord.Embed(
        title = f"{data['Guild']} ({data['Members']} {'members' if len(data['Members']) > 1 else 'member'})", 
        url=f"https://www.realmeye.com/guild/{data['Guild']}", 
        color = 0x2F3136
    )
    embed1.add_field(
        name = "Overview",
        value = f"> **Fame:** {data['Fame']}\n> **Total Characters:** {data['Characters']}\n> **Most active on:** {data['MostActiveOn']}",
        inline = True
    )
    embed1.set_footer(
        text = f"members on the next page"
    )

    embeds.append(embed1)

    for member in data["GuildMemberData"]:
        if member['name'] == "Private":
            continue # skip private members
        embed = discord.Embed(
            color = 0x2F3136, url=f"https://www.realmeye.com/player/{member['name']}", 
            title=f"{data['Guild']} • {member['name']}", description = f"> **Guild Rank:** {member['guild_rank']}"
        )
        embed.add_field(
            name = "Overview",
            value = f"> **Stars:** {member['star_rank']}\n> **Fame:** {member['fame']}\n> **Characters:** {member['characters']}"
        )
        embed.set_footer(
            text = f"Page {data['GuildMemberData'].index(member)+1}/{len(data['GuildMemberData'])} ({len(data['GuildMemberData'])} {'members' if len(data['GuildMemberData']) > 1 else 'member'})"
        )
        embeds.append(embed)
    return embeds

async def search_item(item: str):
    """Grabs information about an item from RealmEye"""

    async with aiohttp.ClientSession() as sesh:
        async with sesh.get(f"https://realmeye-api.glitch.me/wiki/{item}") as resp:
            data = await resp.json()
            if not data.get("Title"):
                fail_embed = discord.Embed(
                    description = "> Unable to find that item",
                    color = 0xE8D46E
                )
                return fail_embed

    tier = f"T{str(data['Tier'])}" if any(x in str(data['Tier']) for x in map(str, range(1, 16))) else data['Tier']
    embed1 = discord.Embed(
        title = f"RealmEye • {data['Title']} ({tier})",
        description = f"{data['Description']}",
        url = f"https://www.realmeye.com/wiki/{item}",
        color = 0x2F3136
    )

    lootbags = {
        "Brown Bag": "<:brownbag:1144734798993170432>", 
        "Pink Bag": "<:pinkbag:1144734826935627876>",
        "Purple Bag": "<:purplebag:1144734829074722826>",
        "Blue Bag": "<:bluebag:1144734796849881149>",
        "Cyan Bag": "<:cyanbag:1144734800243068928>",
        "Red Bag": "<:redbag:1144734830651768832>",
        "Orange Bag": "<:orangebag:1144734807365005353>",
        "White Bag": "<:whitebag:1144734845252141216>"
    }
    lootbag = str(data['LootBag'])
    for bag, emoji in lootbags.items():
        lootbag = lootbag.replace(bag, emoji)

    overview_info = "\n".join([f"> **{key.capitalize()}:** {data[key]}" for key in ['Damage', 'Shots', 'Duration', 'Cooldown', 'MPCost'] if data.get(key)])
    overview = f"> **On Equip:** {data['OnEquip']}\n{overview_info}\n> **Loot Bag:** {lootbag}" if data.get("OnEquip") else f"{overview_info}\n> **Loot Bag:** {lootbag}"
    embed1.add_field(
        name = "Overview",
        value = overview,
        inline = True
    )

    firerate = f"> **Rate of Fire:** {data['RateOfFire']}" if data.get("ProjectileSpeed") and data.get("RateOfFire") else ""
    projectile_info = "\n".join([f"> **{key.capitalize()}:** {data[key]}" for key in ['ProjectileSpeed', 'Lifetime', 'Range'] if data.get(key)])
    embed1.add_field(
        name = "Projectile Info",
        value = f"{projectile_info}\n{firerate}"
    )

    if data.get("ReactiveProcs"):
        embed1.add_field(
            name = "Reactive Procs",
            value = f"`{data['ReactiveProcs']}`",
            inline = False
        )
    if data.get("Effects"):
        embed1.add_field(
            name = "Effects",
            value = f"`{data['Effects']}`",
            inline = False
        )
    
    footer_text = " ".join([f"{key.capitalize()}: {data[key]}" for key in ['FeedPower', 'XPBonus'] if data.get(key)])
    if data.get("Soulbound"):
        footer_text += " | SB: ✓" if data['Soulbound'] else " | SB: ✘"
    embed1.set_footer(text = footer_text)

    return embed1

async def random_class():
    "Returns a random class"

    classes = ['rogue', 'archer', 'wizard', 'priest', 'warrior', 'knight', 'paladin', 'assassin', 'necromancer', 'huntress', 'mystic', 'trickster', 'sorcerer', 'ninja', 'samurai', 'bard', 'kensei']
    chosen_class = random.choice(classes)
    return chosen_class

async def check_rotmg_class(character_class: str):
    """Determines which class image to use"""

    thumbnail_url = {
        "Rogue": "https://i.imgur.com/hgiU2hA.png",
        "Archer": "https://i.imgur.com/OrNGRgy.png",
        "Wizard": "https://i.imgur.com/QAtKJFt.png",
        "Priest": "https://i.imgur.com/MPcn792.png",
        "Warrior": "https://i.imgur.com/It4sclp.png",
        "Knight": "https://i.imgur.com/snm8oKO.png",
        "Paladin": "https://i.imgur.com/caT4rO5.png",
        "Assassin": "https://i.imgur.com/Xy1Lqha.png",
        "Necromancer": "https://i.imgur.com/pmOEcsZ.png",
        "Huntress": "https://i.imgur.com/tylzyyE.png",
        "Mystic": "https://i.imgur.com/bksjGPk.png",
        "Trickster": "https://i.imgur.com/E66uyda.png",
        "Sorcerer": "https://i.imgur.com/dzsmUSA.png",
        "Ninja": "https://i.imgur.com/WS5AQZ7.png",
        "Samurai": "https://i.imgur.com/be8agu7.png",
        "Bard": "https://i.imgur.com/h5Os4xa.png",
        "Summoner": "https://i.imgur.com/4QnFwS9.png",
        "Kensei": "https://i.imgur.com/o1uU6vZ.png"
    }

    return thumbnail_url.get(character_class, "https://www.realmeye.com/s/fa/img/eye-big.png")

async def file(url: str, filename: str = "unknown.png"):
    async with aiohttp.ClientSession() as sesh:
        async with sesh.get(url) as resp:
            data = await resp.read()
    
    return discord.File(BytesIO(data), filename = filename)