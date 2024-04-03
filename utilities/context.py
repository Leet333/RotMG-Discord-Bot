import discord
from discord.ext import commands
from discord import Embed
from utilities.config import Color
from typing import Union, Iterable, Optional, Iterator, Any
from .paginator import Paginator

def as_chunks(iterator: Iterable[Any], max_size: int) -> Iterator[Any]:
    ret = list()
    n = 0
    for item in iterator:
        ret.append(item)
        n += 1
        if n == max_size:
            yield ret
            ret = list()
            n = 0
    if ret:
        yield ret
    
class Context(commands.Context):
    """Custom Context for sending messages"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    async def neutral(self, message: str) -> discord.Message:
        embed = Embed(description = f"{message}", color = Color.neutral)
        try:
            await self.reply(embed = embed, mention_author = False)
        except:
            await self.send(embed = embed)

    async def success(self, message: str) -> discord.Message:
        embed = Embed(description = f"{message}", color = Color.success)
        try:
            await self.reply(embed = embed, mention_author = False)
        except:
            await self.send(embed = embed)
        
    async def error(self, message: str) -> discord.Message:
        embed = Embed(description = f"{message}", color = Color.error)
        try:
            await self.reply(embed = embed, mention_author = False)
        except:
            await self.send(embed = embed)

    async def deny(self, message: str) -> discord.Message:
        embed = Embed(description = f"{message}", color = Color.deny)
        try:
            await self.reply(embed = embed, mention_author = False)
        except:
            await self.send(embed = embed)

    def should_paginate(self, _list: list) -> bool:
        return len(_list) > 1

    async def paginate(self, to_paginate: Union[discord.Embed, list]) -> Optional[discord.Message]:
        if isinstance(to_paginate, discord.Embed):
            embed = to_paginate
            if not embed.description:
                return

            if not isinstance(embed.description, list):
                return

            if len(embed.description) == 0:
                return await self.warn("No entries found")
                
            embeds = list()
            num = 0
            rows = [
                f'`{index}` {row}'
                for index, row in enumerate(embed.description, start = 1)
            ]

            for page in as_chunks(rows, 10):
                num += 1
                embeds.append(
                    discord.Embed(
                        color = Color.neutral,
                        title = embed.title,
                        description = '\n'.join(page),
                        timestamp = embed.timestamp
                    )
                    .set_footer(text = f"Page {num}/{len(list(as_chunks(rows, 10)))}  ({len(rows)} {'entries' if len(rows) > 1 else 'entry'})")
                    .set_author(name = self.author.display_name, icon_url = self.author.display_avatar)
                )

            if self.should_paginate(embeds) is False:
                return await self.reply(embed = embeds[0], mention_author = False)

            interface = Paginator(self.bot, embeds, self, invoker = self.author.id, timeout = 180)
            interface.default_pagination()
            return await interface.start()

        elif isinstance(to_paginate, list):
            embeds = to_paginate
            
            if len(embeds) == 0:
                return await self.warn("No entries found")
            if self.should_paginate(embeds) is False:
                return await self.reply(embed = embeds[0], mention_author = False)

            interface = Paginator(self.bot, embeds, self, invoker = self.author.id, timeout = 180)
            interface.default_pagination()
            return await interface.start()