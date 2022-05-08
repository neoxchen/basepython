import datetime

import discord
import pytz

import src.utils.log_util as log
from src.data import settings, emojis, colors
from src.data.settings import SEP
from src.utils.command_handler import CommandHandler
from src.utils.intent_handler import IntentHandler
from src.utils.sql_util import ChainedStatement, SQLError


class MineCommandHandler(CommandHandler, IntentHandler):
    def __init__(self, bot):
        # Initialize command handler superclass
        CommandHandler.__init__(self, bot, "mine", ["mining"], "Command to view Genshin mining respawn status",
                                f"{settings.BOT_PREFIX}mine [list/update] [args...]",
                                f"{settings.BOT_PREFIX}mine update Breeze\n"
                                f"> {settings.BOT_PREFIX}mine list")
        # Initialize intent handler superclass
        IntentHandler.__init__(self, bot, "genshin_mine", "Check whose Genshin Impact world is ready to be mined")

    async def on_command(self, author, command, args, message, channel, guild):
        if len(args) < 1:
            await self.bot.reply(message, content=f"Invalid arguments! Check out `{settings.BOT_PREFIX}help mine`")
            return

        operation = args[0]
        if operation == "list" or operation == "l":
            await self.bot.send_typing_packet(channel)
            await self.bot.reply(message, embedded=get_mine_list_embedded(get_worlds()))
        elif operation == "update" or operation == "u":
            if len(args) < 2:
                await self.bot.reply(message,
                                     content=f"Invalid arguments! Usage: `{settings.BOT_PREFIX}mine update <name>`")
                return
            # Update mine
            update(args[1])
            await self.bot.react_check(message)
        elif operation == "delete" or operation == "d":
            if len(args) < 2:
                await self.bot.reply(message,
                                     content=f"Invalid arguments! Usage: `{settings.BOT_PREFIX}mine delete <existing name>`")
                return
            # Delete mine entry
            row_count = delete(args[1])
            await self.bot.reply(message, content=f"Operation successful, {row_count} rows affected")
        else:
            await message.add_reaction(emojis.QUESTION)
            return

    async def on_intent_detected(self, author, confidence, message, channel, guild):
        await self.bot.send_typing_packet(channel)
        return await self.bot.reply(message, embedded=get_mine_list_embedded(get_worlds()))


def get_mine_list_embedded(worlds):
    embedded = discord.Embed(
        title=f"List of Genshin Impact worlds",
        description=f"There are a total of {len(worlds)} worlds in the database",
        color=colors.COLOR_GENSHIN
    )
    ready = []
    not_ready = []
    for player, seconds_left in worlds.items():
        if seconds_left == 0:
            ready.append(player)
        else:
            not_ready.append((player, seconds_left))
    embedded.add_field(name="**Ready:**", value=f"> {SEP.join(ready) if ready else None}", inline=False)
    not_ready_format = "{} ({})"
    not_ready = sorted(not_ready, key=lambda a: a[1])
    not_ready_message = SEP.join(
        not_ready_format.format(a[0], format_time(a[1])) for a in not_ready) if not_ready else None
    embedded.add_field(name="**Respawning:**", value=f"> {not_ready_message}", inline=False)
    return embedded


def get_time_stamp():
    pacific = pytz.timezone("US/Pacific")
    return (datetime.datetime.now(pacific) - datetime.datetime(2021, 1, 1, tzinfo=pacific)).total_seconds()


def format_time(timestamp):
    minute, second = divmod(timestamp, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    message = ""
    if day > 1:
        message += f"{int(day)}d"
    message += f"{int(hour):02d}h{int(minute):02d}m"
    return message


def update(player_name):
    sql = f"INSERT INTO genshin_mine VALUES (\"{player_name}\", {get_time_stamp()}) ON DUPLICATE KEY UPDATE time_stamp={get_time_stamp()};"
    try:
        with ChainedStatement() as statement:
            row_count = statement.execute(sql)
        if row_count != 1:
            raise SQLError("Potentially incorrect SQL operation!")
    except SQLError as e:
        log.error(e.strerror)


def delete(player_name):
    sql = f"DELETE FROM genshin_mine WHERE player=\"{player_name}\";"
    with ChainedStatement() as statement:
        row_count = statement.execute(sql)
    return row_count


def get_worlds():
    sql = f"SELECT * FROM genshin_mine"
    now = get_time_stamp()
    try:
        with ChainedStatement() as statement:
            result = list(statement.query(sql))
        return {a[0]: max(a[1] + 259200 - now, 0) for a in result}
    except SQLError as e:
        log.error(e.strerror)
        return []


###############################################################
def register_all(bot):
    """ Register all commands in this module """
    mine = MineCommandHandler(bot)
    bot.register_command_handler(mine)
    bot.register_intent_handler(mine.intent, mine)


if __name__ == "__main__":
    pass
