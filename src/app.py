import os
import sys

import discord

# Stabilize imports
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))  # two directories above

from src.bot import BotClient
from src.commands import utility_cmd
from src.commands.botworld import botworld_cmd
from src.commands.genshin import genshin_general_cmd, genshin_mine_cmd
from src.data.environment import DISCORD_TOKEN

print("Hello (happy) world!")
# Create intent
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

# Create and start the client
bot = BotClient(intents=intent)

# Register commands & intents
utility_cmd.register_all(bot)
genshin_general_cmd.register_all(bot)
genshin_mine_cmd.register_all(bot)
botworld_cmd.register_all(bot)

bot.run(DISCORD_TOKEN)
