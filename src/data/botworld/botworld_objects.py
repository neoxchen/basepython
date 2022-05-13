import json
from typing import List, Tuple, Dict

import discord

from src.data import colors, emotes
from src.data.settings import URL_BOTWORLD_WIKI
from src.utils import log_util


class Bot:
    BOT_CLASSES = {"TANK", "SPLASHER", "SNIPER", "CHASER", "EVADER", "BRAWLER", "SUPPORT"}
    BOT_RARITIES = {"COMMON", "SPECIAL", "RARE", "EPIC"}

    def __init__(self, name, description, icon_url, bot_class, rarity, acquisition, abilities, ai, stats):
        """
        Initializes a bot
        Args:
            name (str): bot name
            description (str): bot description
            icon_url (str): URL to bot icon
            bot_class (str): bot class, must be one of BOT_CLASSES
            rarity (str): rarity of bot, must be one of BOT_RARITIES
            acquisition (str): description of how to acquire this bot
            abilities (List[Tuple[Any]]): list of bot abilities formatted as [(ability1, desc1, stats1), ...]
            ai (List[List[Tuple[str]]]): list of bot AI upgrades formatted as [[(A, descA), ...], ...]
            stats (Dict[str, List[str]]): dict of bot stats formatted as { level => [HP, ATK, DPS, SPD] }
        """
        # Basics
        self.name = name
        self.description = description
        self.icon_url = icon_url

        # Type
        assert bot_class in Bot.BOT_CLASSES
        self.bot_class = bot_class
        assert rarity in Bot.BOT_RARITIES
        self.rarity = rarity
        self.acquisition = acquisition

        # Details
        self.abilities = abilities
        self.ai = ai
        self.stats = stats

    def ability_count(self):
        return len(self.abilities)

    def ai_count(self):
        return len(self.ai)

    def get_wiki_url(self):
        return f"{URL_BOTWORLD_WIKI}{self.name.lower()}"

    def get_class_emote(self):
        return emotes.get_class_emote(self.bot_class)

    def get_rarity_emote(self):
        return emotes.get_rarity_emote(self.rarity)

    # Embedded generation methods
    def get_general_embedded(self):
        embedded = discord.Embed(
            title=f"**{self.name} (Link to Wiki)**",
            description=f"{self.description}",
            color=colors.COLORS_BOTWORLD[self.rarity],
            url=self.get_wiki_url()
        )
        embedded.set_thumbnail(url=self.icon_url)

        embedded.add_field(name="**Basics:**", value=f"Class: {self.get_class_emote()} **{self.bot_class}**\n"
                                                     f"Rarity: {self.get_rarity_emote()} **{self.rarity}**\n"
                                                     f"Obtain: **{self.acquisition}**",
                           inline=False)
        return embedded

    def get_abilities_embedded(self):
        embedded = discord.Embed(
            title=f"**{self.name}'s Abilities**",
            color=colors.COLORS_BOTWORLD[self.rarity]
        )
        embedded.set_thumbnail(url=self.icon_url)
        for ability in self.abilities:
            ability_details = ability[2]
            ability_details_string = ""
            for name, attribute in ability_details.items():
                ability_details_string += f"{name}: {attribute}\n"
            embedded.add_field(name=f"**{ability[0]}:**", value=f"{ability[1]}\n```{ability_details_string[:-1]}```", inline=False)
        return embedded

    def get_ai_embedded(self):
        embedded = discord.Embed(
            title=f"**{self.name}'s AI Tree**",
            color=colors.COLORS_BOTWORLD[self.rarity]
        )
        embedded.set_thumbnail(url=self.icon_url)
        for i, ai_level in enumerate(self.ai):
            embedded.add_field(name=f"--", value=f"**AI Level {i + 1}**", inline=False)
            for ai_entry in ai_level:
                embedded.add_field(name=f"**{ai_entry[0]}**", value=ai_entry[1], inline=True)
        return embedded

    def get_stats_embedded(self):
        embedded = discord.Embed(
            title=f"**{self.name}'s Stats**",
            color=colors.COLORS_BOTWORLD[self.rarity]
        )
        embedded.set_thumbnail(url=self.icon_url)
        formatted_stats = f"```{'Level':9s} {'Health':9s} {'Attack':9s} {'DPS':9s} {'Speed':9s}\n"
        for level, stat_list in self.stats.items():
            formatted_stats += f"{level:9s} {stat_list[0]:9s} {stat_list[1]:9s} {stat_list[2]:9s} {stat_list[3]:9s}\n"
        formatted_stats = formatted_stats[:-1] + "```"
        embedded.add_field(name=f"-", value=formatted_stats)
        return embedded

    # Save and load as JSON
    def to_json(self) -> str:
        json_obj = {}

        json_obj["name"] = self.name
        json_obj["description"] = self.description
        json_obj["icon_url"] = self.icon_url

        json_obj["bot_class"] = self.bot_class
        json_obj["rarity"] = self.rarity
        json_obj["acquisition"] = self.acquisition

        # JSON-ify abilities
        abilities = {
            "count": self.ability_count(),
            "list": []
        }
        for ability in self.abilities:
            abilities["list"].append({
                "name": ability[0],
                "description": ability[1],
                "stats": ability[2]
            })
        json_obj["abilities"] = abilities

        # JSON-ify AI tree
        ai_tree = {
            "count": self.ai_count(),
            "list": []
        }
        for ai in self.ai:
            options = {}
            for option in ai:
                options[option[0]] = option[1]
            ai_tree["list"].append(options)
        json_obj["ai"] = ai_tree

        json_obj["stats"] = self.stats
        return json.dumps(json_obj)

    @staticmethod
    def from_json(json_obj: str):
        json_obj = json.loads(json_obj)
        name = json_obj["name"]
        description = json_obj["description"]
        icon_url = json_obj["icon_url"]

        bot_class = json_obj["bot_class"]
        rarity = json_obj["rarity"]
        acquisition = json_obj["acquisition"]

        abilities_json = json_obj["abilities"]
        abilities = []
        for a in range(abilities_json["count"]):
            abilities.append((abilities_json["list"][a]["name"],
                              abilities_json["list"][a]["description"],
                              abilities_json["list"][a]["stats"]))

        ai = []
        ai_json = json_obj["ai"]
        for options in ai_json["list"]:
            ai.append([(a[0], a[1]) for a in options.items()])

        stats = json_obj["stats"]

        return Bot(name, description, icon_url, bot_class, rarity, acquisition,
                   abilities, ai, stats)


class BotList:
    """ Contains a list of bots and various GET methods """

    def __init__(self):
        with open("src/data/botworld/bots.json") as f:
            data_bots = json.load(f)
        self.data_bots = data_bots

        count = 0
        for bot_class in self.data_bots["bot_classes"]:
            count += len(self.data_bots["bots"][bot_class])
        self.bot_count = count
        log_util.info(f"Loaded BotList with {self.bot_count} bots!")

    def get_bot_count(self):
        return self.bot_count

    def get_embedded_by_class(self, bot_class):
        embedded = discord.Embed(
            title=f"**List of Bots**",
            description=f"There are {self.get_bot_count()} bots currently in BotWorld Adventure",
            color=colors.COLOR_BOTWORLD
        )
        embedded.add_field(name=f"{emotes.get_class_emote(bot_class)} **{bot_class.title()} ({len(self.data_bots['bots'][bot_class])}):**",
                           value="--", inline=False)

        count = 0
        value = "> "
        prev_rarity = None
        for bot in self.data_bots["bots"][bot_class]:
            rarity = self.data_bots['bots'][bot_class][bot]['rarity']
            if rarity != prev_rarity:
                if prev_rarity is not None:
                    embedded.add_field(name=f"{emotes.get_rarity_emote(prev_rarity)} **{prev_rarity} ({count}):**", value=value[:-2], inline=False)
                    count = 0
                    value = "\n> "
                prev_rarity = rarity

            value += f"{bot.title()}, "
            count += 1

        # Add the last one
        embedded.add_field(name=f"{emotes.get_rarity_emote(prev_rarity)} **{prev_rarity} ({count}):**", value=value[:-2], inline=False)
        return embedded


if __name__ == "__main__":
    test_bot = Bot("Flamer", "Hot Hot", "icon_url", "EVADER", "SPECIAL",
                   "acquisition", [("ability1", "desc1", "stat1"), ("ability2", "desc2", "stat2")],
                   [[("1a", "1ad"), ("1b", "1bd")], [("2c", "2cd")]],
                   {"lv1": ["hp", "atk", "dps", "spd"]})
    bot_json = test_bot.to_json()
    print(bot_json)

    b2 = Bot.from_json(bot_json)
    print(b2.to_json())
