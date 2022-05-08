import discord
from discord.ui import View

from src.commands.botworld.botworld_spider import fetch_bot
from src.data import settings
from src.utils.command_handler import CommandHandler


class BotView(View):
    """ Contains a view for the bot command """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Basics", disabled=True)
    async def basics_callback(self, button, interaction: discord.Interaction):
        for other_button in self.children:
            other_button.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_general_embedded(), view=self)

    @discord.ui.button(label="Abilities")
    async def abilities_callback(self, button, interaction):
        for other_button in self.children:
            other_button.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_abilities_embedded(), view=self)

    @discord.ui.button(label="AI Tree")
    async def ai_callback(self, button, interaction):
        for other_button in self.children:
            other_button.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_ai_embedded(), view=self)

    @discord.ui.button(label="Stats")
    async def stats_callback(self, button, interaction):
        for other_button in self.children:
            other_button.disabled = False
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_stats_embedded(), view=self)


class BotCommandHandler(CommandHandler):
    def __init__(self, bot):
        super().__init__(bot, "bot", ["b"], "Query for a bot", f"{settings.BOT_PREFIX}bot <name>", f"{settings.BOT_PREFIX}bot chainer")

    async def on_command(self, author, command, args, message, channel, guild):
        bot_name = args[0]
        try:
            bot = fetch_bot(bot_name)
        except AttributeError:
            await self.bot.reply(message, content="Bot not found")
            return
        view = BotView(bot)
        await self.bot.reply(message, embedded=bot.get_general_embedded(), view=view)


def register_all(bot):
    """ Register all commands in this module """
    bot.register_command_handler(BotCommandHandler(bot))
