import asyncio
import datetime

from src.utils import log_util
from src.utils.command_handler import CommandHandler


def next_weekday(weekday, time):
    now = datetime.datetime.utcnow()
    days_ahead = weekday - now.weekday()

    # Target day already happened this week
    if days_ahead < 0:
        days_ahead += 7
    # Target day is today
    elif days_ahead == 0:
        # If time passed, days += 7
        if now.time() > time:
            days_ahead += 7
        # Otherwise, days += 0

    return datetime.datetime.combine(now.date() + datetime.timedelta(days_ahead), time)


def get_next_monday():
    return next_weekday(0, datetime.time(7, 10, 0))


class RemindCommandHandler(CommandHandler):

    def __init__(self, bot):
        super().__init__(bot, "remind", [], "Remind me to do something", "", "")
        # TODO: Pull reminded users from database on init
        self.bot.loop.create_task(self.background_task())

    async def on_command(self, author, command, args, message, channel, guild):
        log_util.info(f"Echoing message: {message.content}")
        await self.bot.reply(message, content=f"Echoing: {message.content}")

    async def background_task(self):
        next_monday = get_next_monday()

        while True:
            now = datetime.datetime.utcnow()
            seconds = (next_monday - now).total_seconds()
            if seconds < 0:
                await self.send_message()
                next_monday = get_next_monday()
                continue

            await asyncio.sleep(60)

    async def send_message(self):
        await self.bot.send_message_to_channel(858931337549578240, content="<@233735408737976320> Parametric transformer time!")


def register_all(bot):
    """ Register all commands in this module """
    bot.register_command_handler(RemindCommandHandler(bot))
