import random

import discord
from discord.ext import commands

class GMOD(commands.Cog):

    emoji = ["brain", "chicken", "comet", "crown", "exploding_head", "eyes", "face_in_clouds", "fire",
             "military_helmet", "military_medal", "ninja", "robot", "spy", "woman_astronaut", "woman_factory_worker",
             "zap"]

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def gmod(self, ctx: commands.Context):
        """
        Sends the link of our Garry's Mod addons collection
        """
        embed = discord.Embed(title="Garry's Mod Addons Collection ! :{}:".format(self.emoji_picker()),
              description="**Download them faster** :arrow_heading_down:️\n[Our Awesome Addons](https://steamcommunity.com/workshop/filedetails/?id=2883455036)\n",
              color=discord.Colour.from_rgb(37, 150, 190))
        embed.set_image(url="https://files.facepunch.com/lewis/1b1811b1/gmod-hero.png")
        embed.set_footer(text="Now, say my name.", icon_url="https://uploads-ssl.webflow.com/5fa452663d18a6699f11aa07/62b46638bedf9aabc6b3c121_Walter%20white.jpg")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    def emoji_picker(self):
        """
        Picks a random emoji from the list
        """
        return random.choice(self.emoji)
