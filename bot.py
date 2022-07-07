import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

client = discord.ext.commands.Bot(command_prefix='!')

load_dotenv()
token = os.getenv('token')

@client.event
async def on_ready():
    print("Bot Started")

@client.command()
async def ping(ctx):
    await ctx.send("pong")


client.run(token)