import re

# Prefix for all text commands
COMMAND_PREFIX = '!'

# ID list
ID_DEV = 585567788400115762
ID_OWNER = 748497983850545163
ID_BOT = 594575361757544452
GUILD_ID = 1039662750563061770
ROLE_ID_TEST = 1079310208062464051

# Database directory
DATABASE_DIR = "./database.db"

# Regular expressions for objects
MESSAGE_URL = [re.compile(r'https://discord.com/channels/(\d+)/(\d+)/(\d+)'),
               re.compile(r'https://canary.discord.com/channels/(\d+)/(\d+)/(\d+)'),
               re.compile(r'https://ptb.discord.com/channels/(\d+)/(\d+)/(\d+)')]