# Made by Maxime Houis https://github.com/MaximeHouis
from typing import List, Mapping, Optional, Union

import discord
from discord.ext import commands
from discord.ext.commands import HelpCommand

import config


class EmbeddedHelp(HelpCommand):
    def __int__(self, **options):
        super().__init__(**options)

    @staticmethod
    def _get_sub_commands(cmd: commands.Command):
        if not isinstance(cmd, commands.GroupMixin):
            return ""

        return " <{}>".format("|".join(list(map(lambda c: c.name, cmd.commands))))

    @staticmethod
    def _cmd_names(cmd: commands.Command):
        if len(cmd.aliases) != 0:
            name = "<{}|{}>".format(cmd.name, "|".join(cmd.aliases))
        else:
            name = cmd.name

        return name

    def _help_base(self) -> discord.Embed:
        embed: discord.Embed = discord.Embed()

        embed.title = ""
        embed.description = ""
        embed.colour = discord.Colour(0xffca00)
        embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
        embed.set_footer(text="Help made with \u2665 by MrYannKee")

        return embed

    async def _send(self, embed: discord.Embed, *, append_perm_text: bool = True):
        if append_perm_text:
            embed.description += f"\nCommands marked with the symbol `{config.perm_char}` " \
                                 f"__cannot__ be used in the current context."
        return await self.context.send(embed=embed)

    def _can_exec(self, cmd: Union[commands.Command, commands.GroupMixin]) -> bool:
        if cmd.parent and not self._can_exec(cmd.parent):
            return False

        try:
            for check in cmd.checks:
                if not check(self.context):
                    return False

            return cmd.cog.cog_check(self.context) if cmd.cog else True
        except commands.CheckFailure:
            return False

    def _exec_status(self, cmd: commands.Command) -> str:
        return '' if self._can_exec(cmd) else config.perm_char

    async def _send_detailed_help(self, obj: Union[commands.Cog, commands.Group]):
        embed: discord.Embed = self._help_base()

        embed.title = obj.description or obj.help or "[unknown]"

        for cmd in obj.walk_commands():
            cmd: commands.Command
            content: str = ""

            if not cmd.parent or isinstance(obj, commands.Group):
                content += f"\n{cmd.help}\n" \
                           f"`{self.get_command_signature(cmd)}{self._get_sub_commands(cmd)}`"

                content += '\n'  # + config.separator
                embed.add_field(name=f"**{cmd.name.title()}{self._exec_status(cmd)}**", value=content, inline=False)
            else:
                # this is a sub-command in a cog, no details needed
                pass

        return await self._send(embed)

    @staticmethod
    def _get_aliases_string(command: commands.Command, parent: str = None) -> str:
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'<{command.name}|{aliases}>'
            if parent:
                fmt = parent + ' ' + fmt
            alias = fmt
        else:
            alias = command.name if not parent else parent + ' ' + command.name

        return alias

    def get_command_signature(self, command: commands.Command):
        parent = command.full_parent_name
        parents = []

        if command.parent:
            current = command.parent
            while current:
                parents.append(self._cmd_names(current))
                current = current.parent
            parents.reverse()
            parent = " ".join(parents)

        return f"{config.command_prefix}{self._get_aliases_string(command, parent)} {command.signature}".strip()

    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
        embed: discord.Embed = self._help_base()

        embed.title = "General Help"
        embed.description = f"Find out more about a command, sub-command or category by using:\n" \
                            f"`{config.command_prefix}help [query]`"

        for cog, _commands in mapping.items():
            name: str = cog.qualified_name if cog else "No Category"
            command_list = list(map(lambda c: f"`{self._cmd_names(c)}{self._exec_status(c)}`", _commands))

            if len(command_list) > 0:
                embed.add_field(name=f"**{name}**", value=", ".join(command_list), inline=False)

        return await self._send(embed)

    async def send_cog_help(self, cog: commands.Cog):
        return await self._send_detailed_help(cog)

    async def send_group_help(self, group: commands.Group):
        if len(group.all_commands) == 0:
            return await self.context.send("error: command group is empty")

        embed: discord.Embed = self._help_base()

        embed.title = f"Help for command group \"{group.name}\""
        embed.description = f"Find out more about a sub-command by using:\n" \
                            f"`{config.command_prefix}help {group.qualified_name} [sub-command]`"

        for cmd in group.commands:
            cmd: commands.Command
            embed.add_field(name=f"**{cmd.name.title()}**",
                            value=f"*{cmd.description or cmd.help or '[unknown]'}*\n"
                                  f"`{self.get_command_signature(cmd)}`",
                            inline=False)

        return await self._send(embed)

    async def send_command_help(self, cmd: commands.Command):
        embed: discord.Embed = self._help_base()
        aliases: str = ", ".join(list(map(lambda a: f"`{a}`", cmd.aliases)))

        if len(aliases) == 0:
            aliases = "None"

        embed.title = f"Help for command '{cmd.qualified_name}'"

        embed.add_field(name="Description", value=f"```\n{cmd.help}```", inline=False)
        embed.add_field(name="Usage",
                        value=f"`{self.get_command_signature(cmd)}{self._get_sub_commands(cmd)}`",
                        inline=False)
        embed.add_field(name="Usable in context?", value="Yes" if self._can_exec(cmd) else "No")
        embed.add_field(name="Category", value=cmd.cog_name or "No Category")
        embed.add_field(name="Aliases", value=aliases)

        return await self._send(embed, append_perm_text=False)

    async def send_error_message(self, error: str):
        return await self.context.send(f"error: {error}")
