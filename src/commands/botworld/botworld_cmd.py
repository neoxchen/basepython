import discord
from discord.ui import View, Button

from src.commands.botworld.botworld_spider import fetch_bot
from src.data.settings import BOT_PREFIX
from src.utils.command_handler import CommandHandler


class BotView(View):
    """ Contains a view for the bot command """

    def __init__(self, bot, command):
        super().__init__()
        self.bot = bot
        self.command = command
        self.message = None

    @discord.ui.button(label="Basics", disabled=True)
    async def basics_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_general_embedded(), view=self)

    @discord.ui.button(label="Abilities")
    async def abilities_callback(self, button, interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_abilities_embedded(), view=self)

    @discord.ui.button(label="AI Tree")
    async def ai_callback(self, button, interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_ai_embedded(), view=self)

    @discord.ui.button(label="Stats")
    async def stats_callback(self, button, interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        await interaction.response.edit_message(embed=self.bot.get_stats_embedded(), view=self)

    async def on_timeout(self):
        # Clear all items
        self.clear_items()

        # Add "interaction expired" button
        button_refresh = Button(label=f"Use {BOT_PREFIX}{self.command} to refresh")
        button_refresh.disabled = True
        self.add_item(button_refresh)

        # Edit message
        await self.message.edit(view=self)


class BotCommandHandler(CommandHandler):
    def __init__(self, bot):
        super().__init__(bot, "bot", ["b"], "Query for a bot", f"{BOT_PREFIX}bot <name>", f"{BOT_PREFIX}bot chainer")

    async def on_command(self, author, command, args, message, channel, guild):
        if not args:
            # TODO: add list of bots
            return
        bot_name = args[0]
        try:
            bot = fetch_bot(bot_name)
        except AttributeError:
            await self.bot.reply(message, content="Bot not found")
            return
        view = BotView(bot, self.command)
        view.message = await self.bot.reply(message, embedded=bot.get_general_embedded(), view=view)


def register_all(bot):
    """ Register all commands in this module """
    bot.register_command_handler(BotCommandHandler(bot))
