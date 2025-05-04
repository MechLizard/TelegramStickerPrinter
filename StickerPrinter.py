from __future__ import annotations
import pickle
import logging
from datetime import (datetime, timedelta)
from typing import (Dict, Union)
import random

from Demos.EvtSubscribe_push import query_text

from zebra import Zebra
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, Sticker, PhotoSize)
from telegram.ext import (ContextTypes, ApplicationBuilder, Application)

import responses
from user import User
import ConfigHandler
import TextCommands
import StickerCommands
from threading import Thread

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

# Initialize printer
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

# Slap detection
# Try to import accelerometer module. If failed, disable slap detection.
try:
    import SlapDetection
    state_cf['slap_hardware'] = True
    slap_detector = SlapDetection.SlapDetection(state_cf['slap_detection'], printer, printer_cf)
    thread = Thread(target=slap_detector.slap_detection, args=(printer,))
    thread.start()
    logging.info("Accelerometer detected. Slap detection can be enabled.")
except ModuleNotFoundError:
    state_cf['slap_detection'] = state_cf['slap_hardware'] = False
    slap_detector = None
    logging.info("Slap detection disabled. smbus or mpu6050-raspberrypi module not installed")
except FileNotFoundError:
    state_cf['slap_detection'] = state_cf['slap_hardware'] = False
    slap_detector = None
    logging.error("No .jpg or .png images in slap_images folder. Slap detection disabled.")
except OSError:
    state_cf['slap_detection'] = state_cf['slap_hardware'] = False
    slap_detector = None
    logging.error("Accelerometer not detected. Slap detection disabled.")

bot_start_time = datetime.now()

# User list
users: Dict[int, User] = {}
# Check if there is a previously saved user list
try:
    with open("limit_tracker.p", "rb") as file:
        users = pickle.load(file)
except FileNotFoundError:
    print("Starting a new list")

# Sticker History
sticker_history = set()
try:
    with open("sticker_history.p", "rb") as file:
        sticker_history = pickle.load(file)
except FileNotFoundError:
    print("Starting a new sticker history list")


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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Replies to the user with basic functionality of the bot, github link, and how many stickers they have left.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return
    text = responses.HELP.format(amount=str(users_cf['sticker_limit']))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                   disable_web_page_preview=True,
                                   parse_mode="HTML")

async def random_sticker_start(update: Update, context: ContextTypes.DEFAULT_TYPE, application: Application):
    """ If enabled, gives the random sticker warning and prompt. Forwards to random_sticker if already encountered.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    :param application: Application object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return

    if not state_cf['random_sticker_printing']:
        text = responses.RANDOM_DISABLED_ERROR
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    current_user = StickerCommands.get_user(update, users, users_cf)

    # Warn user if it's the first time attempting to use the random function.
    if not current_user.accepted_random_warning:
        keyboard = [
            [InlineKeyboardButton("I understand", callback_data='random_warning_accept')],
            [InlineKeyboardButton("Nevermind!", callback_data='random_warning_decline')]
        ]
        reply_buttons = InlineKeyboardMarkup(keyboard)
        text = responses.RANDOM_WARNING
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_buttons)
        pickle.dump(users, open("limit_tracker.p", "wb"))
        return

    # Otherwise, print a random sticker
    await random_sticker(update, context, application)

async def random_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE, application: Application):
    """ If enabled, prints a random sticker saved in sticker_history and sticker_history.p.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    :param application: Application object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return

    if not state_cf['random_sticker_printing']:
        text = responses.RANDOM_DISABLED_ERROR
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    current_user = StickerCommands.get_user(update, users, users_cf)
    current_user.accepted_random_warning = True

    if not sticker_history:
        text = responses.RANDOM_QUEUE_EMPTY_ERROR
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    chosen_sticker = random.choice(list(sticker_history))

    text = responses.RANDOM_CHOSEN_STICKER
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    # Try 5 times to get a sticker that sends. Otherwise, there is likely no sendable stickers.
    for i in range(5):
        if type(chosen_sticker) == PhotoSize:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=chosen_sticker)
            break
        elif type(chosen_sticker) == Sticker:
            await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=chosen_sticker.file_id)
            break
        else:
            return
    else:
        text = responses.RANDOM_NO_SENDABLE_STICKERS + "\n\n" + current_user.get_limit_response()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return


    await receive_sticker(update, context, application, object_to_print=chosen_sticker)

async def opt_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not state_cf['bot_enabled']:
        return

    current_user = StickerCommands.get_user(update, users, users_cf)
    # If the user opted out.
    if not current_user.opt_out_sticker_history:
        current_user.opt_out_sticker_history = True
        # Delete all of their stickers from the history
        for sticker in current_user.sticker_history:
            if sticker in sticker_history:
                sticker_history.remove(sticker)

        current_user.sticker_history.clear()
        text = responses.STICKER_HISTORY_OPT_OUT
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        pickle.dump(users, open("limit_tracker.p", "wb"))
    else:
        current_user.opt_out_sticker_history = True
        text = responses.STICKER_HISTORY_ALREADY_OPTED_OUT
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def button_press_press(update: Update, context: ContextTypes.DEFAULT_TYPE, application: Application):
    """ Triggers when reply is pressed in the random sticker warning.
    Either triggers a random sticker or cancels the transaction depending on choice.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    :param application: Application object containing the bot interface for the current chat.
    """
    query = update.callback_query
    await query.answer()

    match query.data:
        case "random_warning_decline":
            current_user = StickerCommands.get_user(update, users, users_cf)
            text = responses.RANDOM_WARNING_CANCEL + "\n\n" + current_user.get_limit_response()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return
        case "random_warning_accept":
            await random_sticker(update, context, application)

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
                                                 slap_detector, printer_cf, users_cf, state_cf,
                                                 config, sticker_history):
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


async def receive_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE, application: Application,
                          object_to_print: Union[Sticker, PhotoSize] = None):
    """ Triggers when a static sticker is received. Downloads and prints the sticker.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param application: Object containing the general bot interface
        :param object_to_print: A sticker or PhotoSize object to override current message.
    """

    global users

    if not state_cf['bot_enabled']:
        return

    # Don't accept stickers if it was before the printer started.
    # Messages that came in before have a datetime of shortly after the bot start time.
    # Wait 2 second before accepting commands.
    if update.effective_message.date.now() < bot_start_time + timedelta(0, 2):
        return

    # Find user in the users list if exists. Otherwise, create a new one.
    current_user = StickerCommands.get_user(update, users, users_cf)

    # Error if user has no stickers left
    if await StickerCommands.limit_exceeded(update, context, current_user):
        return

    # === Print the Sticker === #
    # Get the file
    sticker_file, image_object = await StickerCommands.download_image(update, context, current_user,
                                                                      object_to_print=object_to_print)
    if sticker_file is None:
        return

    # Convert sticker to printable format
    print_image = await StickerCommands.convert_sticker(sticker_file, printer_cf)

    StickerCommands.print_sticker(print_image, printer, printer_cf)

    # Subtract sticker from the user's amount
    current_user.sticker_count += 1

    # Send confirmation
    text = responses.get_confirm_message() + "\n\n" + current_user.get_limit_response()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                   disable_web_page_preview=True,
                                   parse_mode="HTML")

    # Random event if enabled
    await StickerCommands.random_event(update, context, current_user, application, printer, state_cf,
                                       users_cf, printer_cf)

    # Send Sticker to superuser if enabled
    await StickerCommands.forward_to_superuser(update, context, current_user, setup_cf, state_cf,
                                               object_to_print=object_to_print)

    # Save data
    if not current_user.opt_out_sticker_history:
        if type(image_object) is Sticker:
            sticker_history.add(image_object)
            current_user.sticker_history.add(image_object)
    pickle.dump(users, open("limit_tracker.p", "wb"))
    pickle.dump(sticker_history, open("sticker_history.p", "wb"))
