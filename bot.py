import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os

client = discord.ext.commands.Bot(command_prefix='!', help_command=None)

load_dotenv()
token = os.getenv('token')

@client.event
async def on_ready():
    print("Bot Started")
    await client.change_presence(activity=discord.Game(name="Trying to be helpful ⚡"))

@client.command()
async def help(ctx):
    embed = discord.Embed(title="⬇️ Help ⬇️", description="Avaible commands", color=discord.Colour.from_rgb(234, 200, 115))
    embed.set_image(url="https://cdn.pixabay.com/photo/2015/12/24/15/05/computer-1106900_960_720.jpg")
    embed.add_field(name="cs", value="Paste your ip to generate the connect csgo command", inline=False)
    embed.add_field(name="ping", value="Show bot's latency", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def cs(ctx, arg):
    embed = discord.Embed(title=ctx.author.name + " is on a server ! :{}:".format(emojiPicker()), description="Join him before no more slots left.\n\n**connect {}**".format(arg), color=discord.Colour.from_rgb(234, 200, 115))
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping Command", description=f"🏓 My latency is about **{round(client.latency * 1000)} ms**.\nFortunately, I'm still alive ! :rainbow:", color=discord.Colour.from_rgb(234, 200, 115))
    await ctx.send(embed=embed)


def emojiPicker():
    emoji = ["brain", "chicken", "comet", "crown", "exploding_head", "eyes", "face_in_clouds","fire", "military_helmet", "military_medal", "ninja", "robot", "spy", "woman_astronaut", "woman_factory_worker", "zap"]
    return random.choice(emoji)


client.run(token)