import os

from discord.ext import commands
from dotenv import load_dotenv

from Help.help import HelpCommand
from Commands import Ping, Memes, CSGO
from Events import BotEvents

client = commands.Bot(command_prefix='!', help_command=None)


def main():
    load_dotenv()

    client.add_cog(BotEvents.BotEvents(client))
    client.add_cog(Ping.Ping(client))
    client.add_cog(Memes.Memes(client))
    client.add_cog(CSGO.CSGO(client))

    client.run(os.getenv('token'), help_command=HelpCommand)


if __name__ == "__main__":
    main()
