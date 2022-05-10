import discord
from discord.ui import View, Button

from src.commands.botworld.botworld_objects import BotList
from src.commands.botworld.botworld_spider import fetch_bot
from src.data import emotes
from src.data.settings import BOT_PREFIX
from src.utils.command_handler import CommandHandler

# Statically initialized
# - data doesn't change unless restarted
bot_list = BotList()


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
        button_refresh = Button(label=f"Use '{BOT_PREFIX}{self.command} {self.bot.name.lower()}' to refresh")
        button_refresh.disabled = True
        self.add_item(button_refresh)

        # Edit message
        await self.message.edit(view=self)


class BotListView(View):
    """ Contains a view for the bot command """

    def __init__(self, bot_class, command):
        super().__init__()
        self.bot_class = bot_class
        self.command = command
        self.message = None

    @discord.ui.button(label="Tank", emoji=emotes.ICON_TANK, disabled=True)
    async def tank_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "TANK"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Splasher", emoji=emotes.ICON_SPLASHER, disabled=False)
    async def splasher_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "SPLASHER"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Sniper", emoji=emotes.ICON_SNIPER, disabled=False)
    async def sniper_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "SNIPER"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Chaser", emoji=emotes.ICON_CHASER, disabled=False)
    async def chaser_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "CHASER"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Evader", emoji=emotes.ICON_EVADER, disabled=False)
    async def evader_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "EVADER"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Brawler", emoji=emotes.ICON_BRAWLER, disabled=False)
    async def brawler_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "BRAWLER"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

    @discord.ui.button(label="Support", emoji=emotes.ICON_SUPPORT, disabled=False)
    async def support_callback(self, button, interaction: discord.Interaction):
        self.enable_all_items(exclusions=[button])
        button.disabled = True
        self.bot_class = "SUPPORT"
        await interaction.response.edit_message(embed=bot_list.get_embedded_by_class(self.bot_class), view=self)

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
            default_bot_class = "TANK"
            view = BotListView(default_bot_class, self.command)
            view.message = await self.bot.reply(message, embedded=bot_list.get_embedded_by_class(default_bot_class), view=view)
            return

        bot_name = args[0].lower()

        # TODO: Temporary fix for dune bug bot
        if bot_name == "dunebug":
            bot_name = "dune-bug"

        try:
            bot = fetch_bot(bot_name)
        except AttributeError:
            # TODO: perhaps add fuzz search here?
            await self.bot.reply(message, content=f"Bot not found, use `{BOT_PREFIX}{self.command}` to view a list of bots")
            return

        view = BotView(bot, self.command)
        view.message = await self.bot.reply(message, embedded=bot.get_general_embedded(), view=view)


def register_all(bot):
    """ Register all commands in this module """
    bot.register_command_handler(BotCommandHandler(bot))
