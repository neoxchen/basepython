##########################
# GENERAL CONFIGURATIONS #
##########################
BOT_PREFIX = "~"
SEP = ", "

VERBOSE_LEVEL = 0
STDERR_LEVEL = 5

############################
# SCHEDULER CONFIGURATIONS #
############################
# Note: All units in this section are in seconds
# How often will the scheduler loop run? (default: 10)
SCHEDULER_LOOP_INTERVAL = 10

# How often will the scheduler ping the database? (default: 60)
# - This will also dictate how many "rows" to retrieve in each ping
SCHEDULER_DATABASE_INTERVAL = 60

##########################
# CHANNEL CONFIGURATIONS #
##########################
# Enabled servers
ENABLED_SERVERS = {
    858926254719107092,  # Libenchurl
    552017106611208194,  # Base emotes
    972901791844958219,  # Void
}

# Enabled channels
ENABLED_CHANNELS = {
    563785796050485259,  # MemeOE >> testing channel
    453918676022722561,  # MOE >> moe-bot
    973242909619019817,  # Void >> bot-spam
}

###########################
# BOTWORLD CONFIGURATIONS #
###########################
# Base URL for BotWorld wiki
URL_BOTWORLD_WIKI = "https://www.botworld.wiki/"
