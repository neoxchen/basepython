# Bot class emotes
ICON_TANK = "<:class_tank:973367386671579196>"
ICON_SPLASHER = "<:class_splasher:973367386575085568>"
ICON_SNIPER = "<:class_sniper:973367386533167154>"
ICON_CHASER = "<:class_chaser:973367386411503636>"
ICON_EVADER = "<:class_evader:973367386507989052>"
ICON_BRAWLER = "<:class_brawler:973367385321009207>"
ICON_SUPPORT = "<:class_support:973367386617040966>"

# Bot rarity emotes
RARITY_EPIC = "<:rarity_epic:973349538125475860>"
RARITY_RARE = "<:rarity_rare:973349538209337395>"
RARITY_SPECIAL = "<:rarity_special:973349538251296838>"
RARITY_COMMON = "<:rarity_common:973349537995444274>"


def get_class_emote(bot_class: str):
    if bot_class == "TANK":
        return ICON_TANK
    elif bot_class == "SPLASHER":
        return ICON_SPLASHER
    elif bot_class == "SNIPER":
        return ICON_SNIPER
    elif bot_class == "CHASER":
        return ICON_CHASER
    elif bot_class == "EVADER":
        return ICON_EVADER
    elif bot_class == "BRAWLER":
        return ICON_BRAWLER
    elif bot_class == "SUPPORT":
        return ICON_SUPPORT
    return None


def get_rarity_emote(rarity):
    if rarity == "COMMON":
        return RARITY_COMMON
    elif rarity == "SPECIAL":
        return RARITY_SPECIAL
    elif rarity == "RARE":
        return RARITY_RARE
    elif rarity == "EPIC":
        return RARITY_EPIC
    return None
