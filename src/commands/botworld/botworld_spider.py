import re

import requests
from bs4 import BeautifulSoup

from src.commands.botworld.botworld_objects import Bot
from src.data.settings import URL_BOTWORLD_WIKI


def fetch_bot(name):
    page = requests.get(f"{URL_BOTWORLD_WIKI}/{name}")
    soup = BeautifulSoup(page.content, "html.parser")
    bot_info = soup.find("div", class_="bot-infos")

    # Bot Basics
    bot_intro = bot_info.find("div", class_="intro")
    bot_name = bot_intro.find("h1").get_text()
    # print(f"NAME: {bot_name}")
    bot_description = bot_intro.find("p").get_text()
    # print(f"DESC: {bot_description}")

    # Bot Icon
    bot_icon = bot_info.find("div", class_="botcard").find("div", class_="pic").find("img")["src"]
    bot_icon = f"{URL_BOTWORLD_WIKI[:-1]}{bot_icon}"
    # print(f"ICON SRC: {bot_icon}")

    # Bot Card
    bot_card = bot_info.find("div", class_="botcard").find("div", class_="cardinfos").find_all("td")
    bot_class = bot_card[0].get_text().upper()
    # print(f"TYPE: {bot_class}")
    bot_rarity = bot_card[1].get_text().upper()
    # print(f"RARITY: {bot_rarity}")
    bot_acquisition = bot_card[2].get_text()
    # print(f"ACQUISITION: {bot_acquisition}")

    # Bot Abilities
    bot_abilities_html = bot_info.find("div", class_="abilities")
    bot_abilities = []
    for i, bot_ability_html in enumerate(bot_abilities_html.find_all("li")):
        bot_ability_name = bot_ability_html.find("h3").get_text()
        bot_ability_description = bot_ability_html.find_all("p")[1].get_text()
        bot_ability_attributes_text = bot_ability_html.find("code").get_text()

        bot_ability_attributes = {}
        pattern = re.compile("( , |, | ,)")
        for ability_entry in pattern.split(bot_ability_attributes_text):
            if pattern.match(ability_entry):
                continue
            try:
                ability_data = ability_entry.strip().split(":")
                bot_ability_attributes[ability_data[0].strip()] = ability_data[1].strip()
            except IndexError:
                bot_ability_attributes[ability_entry] = "N/A"

        bot_abilities.append((bot_ability_name, bot_ability_description, bot_ability_attributes))
        # print(f"ABILITY {i + 1}: {(bot_ability_name, bot_ability_description, bot_ability_attributes)}")

    # Bot AI Tree
    bot_ai_tree_html = bot_info.find("div", class_="bot_bloc_2")
    bot_ai_tree = []
    for bot_ai_html in bot_ai_tree_html.find_all("li"):
        bot_ai_names_html = bot_ai_html.find("thead").find_all("th")
        bot_ai_names = []
        for bot_ai_name_html in bot_ai_names_html:
            if bot_ai_name_html.get_text():
                bot_ai_names.append(bot_ai_name_html.get_text())

        bot_ai_descriptions_html = bot_ai_html.find("tbody").find_all("td")
        bot_ai_descriptions = []
        for bot_ai_description_html in bot_ai_descriptions_html:
            if bot_ai_description_html.get_text():
                bot_ai_descriptions.append(bot_ai_description_html.get_text())

        bot_ai_tree.append(list(zip(bot_ai_names, bot_ai_descriptions)))

    # print(f"AI TREE:")
    # for i, data in enumerate(bot_ai_tree):
    #     print(f"- AI Lv.{i}: {data}")

    bot_stats_html = bot_info.find("div", class_="bot_bloc_3").find("div", class_="stats").find("tbody")
    bot_stats = {}
    for bot_stat_html in bot_stats_html.find_all("tr"):
        bot_stat_level = None
        bot_stat_stats = []
        for i, bot_sub_stat_html in enumerate(bot_stat_html.find_all("td")):
            if i == 0:
                bot_stat_level = bot_sub_stat_html.get_text()
                continue
            bot_stat_stats.append(bot_sub_stat_html.get_text())
        bot_stats[bot_stat_level] = bot_stat_stats

    # print(f"STATS: {bot_stats}")

    bot = Bot(bot_name, bot_description, bot_icon, bot_class, bot_rarity, bot_acquisition, bot_abilities, bot_ai_tree, bot_stats)
    return bot


if __name__ == "__main__":
    response = fetch_bot("nozzle")
    print(response)
