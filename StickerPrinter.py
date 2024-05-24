from __future__ import annotations
import pickle
import logging
from datetime import (datetime, timedelta)
from typing import Dict

import telegram.error
from zebra import Zebra
from telegram import Update
from telegram.ext import (ContextTypes, ApplicationBuilder, Application)

import responses
from user import User
import ConfigHandler
import TextCommands
import StickerCommands

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# ================================= #
# ======= Object Initiation ======= #
# ================================= #
config = ConfigHandler.read_config()
setup_cf = config['SETUP']
printer_cf = config['PRINTER']
users_cf = config['USERS']
state_cf = config['STATE']

# TODO: Properly comment the function of the functions and give type hints

printer = Zebra(printer_cf['printer_queue'])  # z = Zebra( [queue] )
try:
    printer.setup(direct_thermal=True,
                  label_height=[printer_cf['media_size_y'],
                                printer_cf['media_gap']],
                  label_width=printer_cf['media_size_x'])
except:
    # If there is no correct queue. Inform user in command prompt and list printers
    print(responses.MISSING_QUEUE)
    print(printer.getqueues())
    state_cf['bot_enabled'] = False

bot_start_time = datetime.now()


users: Dict[int, User] = {}
# Check if there is a previously saved user list
try:
    with open("limit_tracker.p", "rb") as file:
        users = pickle.load(file)
except FileNotFoundError:
    print("Starting a new list")


# =============================== #
# ========== Functions ========== #
# =============================== #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Greets the user and informs them of how many stickers they have

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return
    text = responses.GREETING.format(amount=str(users_cf['sticker_limit']))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Handles incoming text messages and commands, usually superuser commands to manage the bot

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
    """

    global users

    # ==== Superuser commands ==== #
    if update.message.from_user.id in setup_cf['super_user_id']:
        command = update.message.text

        if await TextCommands.super_user_command(update, context, command, users, printer,
                                                 printer_cf, users_cf, state_cf, config):
            return
        else:
            await TextCommands.command_not_recognized(update, context)
            return

    # If there is no superuser set and someone requests a list of commands. Return
    if await TextCommands.no_super_users(update, context, setup_cf):
        return

    # If the user isn't a superuser
        # text = "This is where a non-superuser command would go"
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def receive_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE, application: Application):
    """ Handles incoming text messages and commands, usually superuser commands to manage the bot

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param application: object containing the general bot interface
    """
    # Triggers when a static sticker is received
    # Downloads and prints the sticker

    global users

    if not state_cf['bot_enabled']:
        return

    # Don't accept stickers if it was before the printer started.
    # Messages that came in before have a datetime of shortly after the bot start time.
    # Wait 1 second before accepting commands.
    if update.message.date.now() < bot_start_time + timedelta(0, 2):
        return

    # Find user in the users list if exists. Otherwise, create a new one.
    current_user = StickerCommands.get_user(update, users, users_cf)

    # Error if user has no stickers left
    if await StickerCommands.limit_exceeded(update, context, current_user):
        return

    # === Print the Sticker === #

    # TODO: get_file() can time out. Add an error message for the user to try again.
    # Error: raise TimedOut from err
    # TODO: Move this section to its own function
    try:
        if update.message.sticker is None:
            # Download photo
            sticker_file = await update.message.photo[-1].get_file(read_timeout=4.0,
                                                                   connect_timeout=4.0,
                                                                   pool_timeout=4.0)
        else:
            # Download sticker
            sticker_file = await update.message.sticker.get_file(read_timeout=4.0,
                                                                 connect_timeout=4.0,
                                                                 pool_timeout=4.0)
    except telegram.error.TimedOut:
        text = responses.MESSAGE_TIMED_OUT + " " + current_user.get_limit_response()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    # Convert sticker to printable format
    print_image = await StickerCommands.convert_sticker(update, sticker_file, printer_cf)

    StickerCommands.print_sticker(print_image, printer, printer_cf)

    # Subtract sticker from the user's amount
    current_user.sticker_count += 1

    # Send confirmation
    text = responses.get_confirm_message() + "\n\n" + current_user.get_limit_response()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                   disable_web_page_preview=True,
                                   parse_mode="HTML")

    # Random event if enabled
    await StickerCommands.random_event(update, context, current_user, application, printer, state_cf, users_cf, printer_cf)

    # Send Sticker to superuser if enabled
    await StickerCommands.forward_to_superuser(update, current_user, setup_cf, state_cf)

    # Save data
    pickle.dump(users, open("limit_tracker.p", "wb"))

