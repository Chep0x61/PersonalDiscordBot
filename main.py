import os

from discord.ext import commands
from dotenv import load_dotenv

from Help.help import EmbeddedHelp
from Commands import Ping, Gmod, Memes, CSGO
from Events import BotEvents


def main():
    load_dotenv()

    client = commands.Bot(command_prefix='!', help_command=EmbeddedHelp())

    client.add_cog(BotEvents.BotEvents(client))
    client.add_cog(Ping.Ping(client))
    client.add_cog(Memes.Memes(client))
    client.add_cog(CSGO.CSGO(client))
    client.add_cog(Gmod.GMOD(client))

    client.run(os.getenv('token'))

if __name__ == "__main__":
    main()