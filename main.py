# Bot name is at @TheStickerPrinterBot (https://t.me/TheStickerPrinterBot)
# This is an interactive bot that prints any Telegram stickers sent to it as a physical sticker

import pickle
import random
import io
import os
import logging
from datetime import datetime
import sys

import zpl
import telegram
from zebra import Zebra
from telegram import Update
from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
)
from PIL import Image

from constants import *
import responses
from user import User
import ConfigHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================================= #
# ======= Object Initiation ======= #
# ================================= #
config = ConfigHandler.read_config()
setup_cf = config['SETUP']
printer_cf = config['PRINTER']
users_cf = config['USERS']
state_cf = config['STATE']


# TODO: Put this as a toggle in the constants file.
# printer.getqueues() to get list of queues
# printer.setqueue( queue ) to set the printer queue

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
    sys.exit()

# Apply token
application = ApplicationBuilder().token(setup_cf['telegram_api_token']).build()

bot_start_time = datetime.now()

# Check if there is a previously saved user list
try:
    with open("limit_tracker.p", "rb") as file:
        users = pickle.load(file)
except FileNotFoundError:
    print("Starting a new list")
    users = []


# ========================= #
# ======= Functions ======= #
# ========================= #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not state_cf['bot_enabled']:
        return

    text = responses.GREETING + "\n\n" + "You have " + str(users_cf['sticker_limit']) + " stickers left."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global users



    # ==== Superuser commands ==== #
    if update.message.from_user.id in setup_cf['super_user_id']:
        command = update.message.text.lower()

        # ==== Reply Commands ==== #
        if update.message.reply_to_message is not None:
            reply_message = update.message.reply_to_message

            # Get the sender ID
            if reply_message.forward_from is not None:
                sender_id = reply_message.forward_from.id
            else:  # if the user has their chat hidden
                for i in users:
                    if i.check_log(reply_message.id):
                        sender_id = i.user_id
                        break
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.CANT_FIND_USER_ERROR)
                    return

            for i in users:
                if i.user_id == sender_id:
                    current_user = i
                    break
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.CANT_FIND_USER_ERROR)
                return

            # Add or subtract sticker limit (Ex: +5 or -2 or =999 to change limit)
            if command[1:].isdigit():
                if command.startswith("+"):
                    current_user.sticker_max += int(command[1:])
                    text = f"Added {int(command[1:])} stickers to that user. They now have a limit of {current_user.sticker_max}"
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    return
                if command.startswith("-"):
                    current_user.sticker_max -= int(command[1:])
                    text = f"Removed {int(command[1:])} stickers from that user. They now have a limit of {current_user.sticker_max}"
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    return
                if command.startswith("="):
                    current_user.sticker_max = int(command[1:])
                    text = f"That user now has a limit of {current_user.sticker_max}"
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    return

            # ban
            if command == BAN:
                current_user.sticker_max = 0
                await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.USER_BANNED)
                return
            # reset
            if command == RESET:
                current_user.sticker_count = 0
                text = responses.USER_LIMIT_RESET + str(current_user.sticker_max) + " stickers"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                return

            return

        # print(update.effective_chat.id)
        # print(await update.message.sticker.set_name)

        # ==== General Commands ==== #
        if command == COMMANDS:
            text = ("General commands:\n"
                    f"\"{RESET_ALL_COUNT}\" - Resets sticker count to 0\n"
                    f"\"{WIPE}\" - Wipes all users\n"
                    f"\"{SET_ALL_LIMIT} X\" - Sets sticker limit to X\n"
                    f"\"{GET_LIMIT}\" - Shows the current sticker limit\n"
                    f"\"{BOT_ENABLE}\" - Enables the bot\n"
                    f"\"{BOT_DISABLE}\" - Disables the bot\n"
                    f"\"{STICKER_MONITORING_ON}\" - Turn on monitoring (sends superusers all printed stickers)\n"
                    f"\"{STICKER_MONITORING_OFF}\" - Turn off monitoring\n"
                    f"\"{COMMANDS}\" - Displays this help message\n\n"
                    "Reply commands (Reply to a monitored sticker):\n"
                    "[+ or - or =][number] - Add, subtract, or set sticker limit (Ex: +5, -1, or =999)\n"
                    f"\"{BAN}\" - Bans the user. Sets their limit to 0\n"
                    f"\"{RESET}\" - Resets the user's used stickers to 0. Lets them print more")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Resets all users to the default
        if command == RESET_ALL_COUNT:
            for i in users:
                i.sticker_count = 0
            await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.COUNTS_RESET)
            return

        # Wipes all users
        if command == WIPE:
            users.clear()
            try:
                os.remove("limit_tracker.p")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.USERS_WIPED)
            except FileNotFoundError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.NO_FILE)
            except OSError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.CANT_DELETE_FILE)

            return

        # Set all limits to X
        # Command has 3 parts: The command, a space, and a digit
        if command.startswith(SET_ALL_LIMIT):  # Command starts with the limit command
            if command[len(SET_ALL_LIMIT) + 1:].isdigit():  # if command ends with a number
                if command[len(SET_ALL_LIMIT)] == " ":  # If there is a space between

                    new_limit = command[len(SET_ALL_LIMIT) + 1:]
                    for i in users:
                        i.sticker_max = new_limit
                    users_cf['sticker_limit'] = new_limit
                    text = responses.SET_NEW_LIMIT + str(new_limit)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Get sticker limit
        if command == GET_LIMIT:
            text = responses.GET_LIMIT + str(users_cf['sticker_limit'])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Turn off bot
        if command == BOT_DISABLE:
            if state_cf['bot_enabled']:
                text = responses.BOT_DISABLED
            else:
                text = responses.BOT_ALREADY_DISABLED
            state_cf['bot_enabled'] = False
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Turn on bot
        if command == BOT_ENABLE:
            if state_cf['bot_enabled']:
                text = responses.BOT_ALREADY_ENABLED
            else:
                text = responses.BOT_ENABLED
            state_cf['bot_enabled'] = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Turn off sticker monitoring
        if command == STICKER_MONITORING_OFF:
            if state_cf['sticker_monitoring']:
                text = responses.MONITORING_DISABLED
            else:
                text = responses.MONITORING_ALREADY_DISABLED
            state_cf['sticker_monitoring'] = False
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        # Turn on sticker monitoring
        if command == STICKER_MONITORING_ON:
            if state_cf['sticker_monitoring']:
                text = responses.MONITORING_ALREADY_ENABLED
            else:
                text = responses.MONITORING_ENABLED
            state_cf['sticker_monitoring'] = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return

        text = f"Command not recognized. Type \"{COMMANDS}\" for a list of commands"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    # If there is no superuser set and someone requests a list of commands
    elif len(setup_cf['super_user_id']) == 0 and update.message.text.lower() == COMMANDS:
        text = responses.SUPERUSER_NOT_SET
        text += "\n\nYour user ID is: " + str(update.message.from_user.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return

    # If the user isn't a superuser
    else:
        # text = "This is where a non-superuser command would go"
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        pass


async def receive_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global users
    # Triggers when a static sticker is received
    # Downloads and prints the sticker

    if not state_cf['bot_enabled']:
        return

    if update.message.from_user.id in setup_cf['super_user_id'] and False:
        return

    if update.message.date.now() < bot_start_time:
        return

    # Find user in the users list
    for i in users:
        if update.message.from_user.id == i.user_id:
            current_user = i
            break
    # If they aren't found in the array, add them to it
    else:
        users.append(User(update, users_cf))
        current_user = users[-1]

    # Error if user has no stickers left
    if current_user.sticker_count >= current_user.sticker_max:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=current_user.get_limit_response()
        )
        return

    # === Print the Sticker === #
    sticker_file = await update.message.sticker.get_file()
    sticker_buffer = io.BytesIO(b"")  # Create a memory buffer for the sticker to be downloaded to
    await sticker_file.download_to_memory(sticker_buffer)  # Download sticker
    incoming_sticker = Image.open(sticker_buffer).convert("RGBA")  # Create Image object
    print_sticker(incoming_sticker)
    sticker_buffer.close()

    # Subtract sticker from the user's amount
    current_user.sticker_count += 1

    # Send confirmation
    text = responses.GetConfirmMessage() + "\n\n" + current_user.get_limit_response()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if current_user.sticker_count / current_user.sticker_max >= users_cf['ran_event_start']:
        if random.randint(1, 100) <= users_cf['ran_event_chance'] and not current_user.bonus_sticker_encounter:
            # === Do random event === #

            current_user.bonus_sticker_encounter = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.BONUS_STICKER_MESSAGE)

            # === Print a bonus sticker=== #
            bonus_pack = await application.bot.get_sticker_set("BonusSticker")
            bonus_pack = bonus_pack.stickers
            chosen_sticker = bonus_pack[random.randint(0, len(bonus_pack) - 1)].file_id
            await context.bot.send_sticker(context._chat_id, chosen_sticker)

            sticker_file = await context.bot.get_file(chosen_sticker)
            sticker_buffer = io.BytesIO(b"")  # Create a memory buffer for the sticker to be downloaded to
            await sticker_file.download_to_memory(sticker_buffer)  # Download sticker
            incoming_sticker = Image.open(sticker_buffer).convert("RGBA")  # Create Image object
            print_sticker(incoming_sticker)
            sticker_buffer.close()

    # If no more stickers available
    if current_user.sticker_count <= 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.END_MESSAGE)  # Goodbye message

    # Send Sticker to superuser
    if state_cf['sticker_monitoring']:
        # TODO: Exclude superusers from this
        for i in setup_cf['super_user_id']:
            forwarded_message = await update.message.forward(i)
            current_user.log_message(forwarded_message.id)

    # Save data
    pickle.dump(users, open("limit_tracker.p", "wb"))


async def animated_sticker_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.ANIMATED_STICKER_ERROR)


async def main():
    bot = telegram.Bot("6167661077:AAHCLCbzSo5mpTQ_9ysjAC8wdRmk1htSHIA")
    async with bot:
        message = (await bot.get_updates())[-1].message.text
        await bot.send_message(text=message + "\n\n That's what you sound like, you goober", chat_id=92233565)


def print_sticker(incoming_sticker):
    # TODO Don't make stickers resize so much.
    print_command_gen = zpl.Label(printer_cf['media_mm_x'], printer_cf['media_mm_y'], printer_cf['dpmm'])
    # Start with white square as a background
    sticker_img = Image.new("RGBA", (printer_cf['media_size_x'], printer_cf['media_size_y']), "WHITE")
    # Resize the sticker to size of print media
    incoming_sticker = incoming_sticker.resize((printer_cf['media_size_x'], printer_cf['media_size_y']))
    sticker_img.paste(incoming_sticker, mask=incoming_sticker)  # Turn transparent pixels white by pasting sticker over white square
    sticker_img = sticker_img.convert("1")  # Convert image to 1-byte B&W image
    # sticker_img.show()  # Can be used to display the sticker on the host
    print_command_gen.origin(printer_cf['image_offset_x'], printer_cf['image_offset_y'])
    print_command_gen.write_graphic(sticker_img, printer_cf['media_mm_x'])
    print_command_gen.endorigin()

    # print(print_command_gen.dumpZPL())  # Can be used to display the print commands
    printer.output(print_command_gen.dumpZPL())
    # TODO: Test this and see what situations give an error or just hangs in the queue
    # try:
    # print_graphic(x, y, width, length, data, qty)
    # printer.print_graphic(0, 0, MEDIA_SIZE_Y, MEDIA_SIZE_X, sticker_img, 1)
    # except:
    #    text = responses.PRINTER_OFFLINE + "\n\n" + current_user.get_limit_response()
    #    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    #    return

    del print_command_gen
    del sticker_img


# ==================== #
# ======= Main ======= #
# ==================== #
if __name__ == '__main__':
    #asyncio.run(main())

    # ==== Function Declarations ====#
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), receive_text)
    start_handler = CommandHandler('start', start)
    sticker_handler = MessageHandler(filters.Sticker.STATIC, receive_sticker)
    animated_sticker_handler = MessageHandler(filters.Sticker.ALL & (~filters.Sticker.STATIC), animated_sticker_error)

    # ==== Handlers ==== #
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(sticker_handler)
    application.add_handler(animated_sticker_handler)

    application.run_polling()

