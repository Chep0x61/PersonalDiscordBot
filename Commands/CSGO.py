import random

import discord
from discord.ext import commands


class CSGO(commands.Cog):
    emoji = ["brain", "chicken", "comet", "crown", "exploding_head", "eyes", "face_in_clouds", "fire",
             "military_helmet", "military_medal", "ninja", "robot", "spy", "woman_astronaut", "woman_factory_worker",
             "zap"]

    def __int__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def cs(self, ctx: commands.Context, ip: str):
        """
        Sends a connect command for a CSGO server
        """

        if ip is None:
            embed = discord.Embed(title=":warning:  Wrong Usage :warning: ", description="An IP is required !",
                                  color=discord.Colour.red())
            embed.add_field(name="Example ⬇️ ", value="`!cs IP:PORT` :white_check_mark:")
            await ctx.message.delete()
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=ctx.author.name + " is on a server ! :{}:".format(self.emoji_picker()),
                              description="Join him before there are no more slots left.\n\n**connect {}**".format(ip),
                              color=discord.Colour.from_rgb(234, 200, 115))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    def emoji_picker(self):
        """
        Picks a random emoji from the list
        """
        return random.choice(self.emoji)
