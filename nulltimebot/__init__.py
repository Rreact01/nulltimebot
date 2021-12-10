import logging
import os
import sys
import time

import deethon
from dotenv import load_dotenv
from telethon import TelegramClient, functions, types
from telethon.events import NewMessage

formatter = logging.Formatter(
    '%(levelname)s %(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler(f'{__name__}.log', 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.WARNING)
telethon_logger.addHandler(ch)
telethon_logger.addHandler(fh)

botStartTime = time.time()

load_dotenv()

try:
    API_ID = int(os.environ["A394063"])
    API_HASH = os.environ["fcaae0325b2bd1132acbb8f6eccf2a19"]
    BOT_TOKEN = os.environ["5008674339:AAGEWlU0Qn5ZKFeu4P1SoEkOSEpUG7YTq4E"]
    DEEZER_TOKEN = os.environ["7220039d5b1c2d846c45c2fb42539c8dc300ead9d0c9be5cb1ef75c084e9697b8922a627d7e4d5dfe642aabd3ab607ec77404f740b1935b5a53c1c8cb5ee628467e64cd15cc4c025a9b46461b65bc980cbe5cd6dc68b429434fe3e080805186f"]
    OWNER_ID = int(os.environ["2102436501"])
except KeyError:
    logger.error("One or more environment variables are missing! Exiting now…")
    sys.exit(1)

deezer = deethon.Session(DEEZER_TOKEN)
logger.debug(f'Using deethon v{deethon.__version__}')

bot = TelegramClient(__name__, API_ID, API_HASH,
                     base_logger=telethon_logger).start(bot_token=BOT_TOKEN)
logger.info("Bot started")

# Saving user preferences locally
users = {}

bot.loop.run_until_complete(
    bot(functions.bots.SetBotCommandsRequest(
        commands=[
            types.BotCommand(
                command='start',
                description='Get the welcome message'),
            types.BotCommand(
                command='help',
                description='How to use the bot'),
            types.BotCommand(
                command='settings',
                description='Change your preferences'),
            types.BotCommand(
                command='info',
                description='Get some useful information about the bot'),
            types.BotCommand(
                command='stats',
                description='Get some statistics about the bot'),
        ]
    ))
)


@bot.on(NewMessage())
async def init_user(event: NewMessage.Event):
    if event.chat_id not in users.keys():
        users[event.chat_id] = {
            "quality": "FLAC"
        }
