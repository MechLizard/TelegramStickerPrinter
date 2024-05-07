import os
from typing import Dict, Union

from zebra import Zebra
from telegram import Update
from telegram.ext import ContextTypes

from constants import *
import responses
import ConfigHandler

from user import User


async def super_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, users: Dict[int, User],
                             printer: Zebra, printer_cf, users_cf, state_cf, config: Dict) -> bool:
    """ Takes a command sent by a user, determines if it's a superuser.
        If it is a superuser, check whether the messages match a command. If so, run that command.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user
        :param users: A dict containing the users, found by user ID.
        :param printer: The Zebra printer object.
        :param printer_cf: Dict of configuration settings relating to the printer.
        :param users_cf: Dict of configuration settings relating to users.
        :param state_cf: Dict of configuration settings relating to the state of the script.
        :param config: The Dict containing the rest of the _cf configuration dictionaries.

        :returns: A bool indicating whether the message matches a command.
        """

    # First check set_queue, since it is case-sensitive
    # Sets the print queue to your specification
    if await set_queue(update, context, command, printer, printer_cf):
        return True

    command = command.lower()

    # ==== Reply Commands ==== #
    if update.message.reply_to_message is not None:
        reply_message = update.message.reply_to_message

        # Get the sender ID
        if reply_message.forward_origin != "hidden_user":
            current_user = users.get(reply_message.forward_origin.sender_user.id)
        else:  # if the user has their chat hidden
            for key, value in users.items():
                if value.check_log(reply_message.id):
                    current_user = users.get(value.user_id)
                    break
            else:
                current_user = None

        if current_user is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.CANT_FIND_USER_ERROR)
            return True

        # Check for Adding or subtracting sticker limit command (Ex: +5 or -2 or =999 to change limit)
        if await user_limit_adjust(update, context, command, current_user):
            return True

        # Check for ban or reset command
        await ban_reset(update, context, command, current_user)

        return True

    # ==== General Commands ==== #
    # List commands
    if await list_commands(update, context, command):
        return True

    # Resets all users to the default
    if await reset_all(update, context, command, users):
        return True

    # Wipes all users
    if await wipe(update, context, command, users):
        return True

    # Set all limits to X
    # Command has 3 parts: The command, a space, and a digit
    if await set_limit(update, context, command, users, users_cf):
        return True

    # Get sticker limit
    if await get_limit(update, context, command, users_cf):
        return True

    # Turn bot on or off
    if await toggle_bot(update, context, command, printer, state_cf, printer_cf):
        return True

    if await toggle_monitoring(update, context, command, state_cf):
        return True

    # Display print offset and list commands
    if await get_print_offset(update, context, command, printer_cf):
        return True

    # Set the x (Horizontal) print offset
    if await set_print_offset(update, context, command, printer_cf):
        return True

    # Display the current queue and checks if it exists on the system
    if await check_queue(update, context, command, printer, printer_cf):
        return True

    # Lists the print queues on the device
    if await list_queues(update, context, command, printer):
        return True

    # Enables/disables the random event
    if await toggle_random_event(update, context, command, state_cf):
        return True

    # Saves config
    if await save_config(update, context, command, config):
        return True

    return False


async def no_super_users(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         setup_cf: Dict[str, Union[str, list, bool]]) -> bool:
    """ Checks whether there is a superuser. If not, tells the user what their user_id is.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param setup_cf: Dict of api token and superuser IDs.

        :returns: A bool indicating whether the message triggers this function.
        """
    if len(setup_cf['super_user_id']) == 0 and update.message.text.lower() == COMMANDS:
        text = responses.SUPERUSER_NOT_SET.format(id=update.message.from_user.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


# ========================= #
# ======= Functions ======= #
# ========================= #
def get_command_int(command: str, user_response: str) -> Union[int, None]:
    """ Gets the number part of a command and check if it's in a valid format.
        Used with commands that require a command and a number.
        Ex: 'setlimit 10' returns 10
        Ex: '+5' returns 5
        Ex: 'setlimit 10 asdfs' returns None

        :param command: The text part of the command from the module
        :param user_response: The full message from the user

        :returns: An int representing the amount if it was successful. None if the format was incorrect.
        """

    modifier = False

    if len(command) == len(user_response):
        return None

    # Check if there is a + or - before the number
    if user_response[len(command) + 1] == "+" or user_response[len(command) + 1] == "-":
        modifier = True

    # If there is a space between
    if not user_response[len(command)] == " ":
        return None

    # if command ends with a number
    if not user_response[len(command) + modifier + 1:].isdigit():  # Modifier adds +1 if true
        return None

    # At this point the command is valid

    number = int(user_response[len(command) + modifier + 1:])

    # If there is a negative sign before the number
    if modifier and user_response[len(command) + 1] == "-":
        number *= -1

    return number


async def user_limit_adjust(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            command: str, current_user: User) -> bool:
    """ Reply command. Adjusts a specific user's sticker limit
        Ex: When replying to a monitored sticker use '+5' or '-2' or '=999' to change limit

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param current_user: A User object containing the user the operation is being performed on.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Add or subtract sticker limit (Ex: +5 or -2 or =999 to change limit)
    if not command[1:].isdigit():
        return False

    if command.startswith("+"):
        current_user.sticker_max += int(command[1:])
        text = responses.ADD_USER_LIMIT.format(amount=int(command[1:]),
                                               total=current_user.sticker_max)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True
    if command.startswith("-"):
        current_user.sticker_max -= int(command[1:])
        text = responses.SUBTRACT_USER_LIMIT.format(amount=int(command[1:]),
                                                    total=current_user.sticker_max)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True
    if command.startswith("="):
        current_user.sticker_max = int(command[1:])
        text = responses.SET_USER_LIMIT.format(total=current_user.sticker_max)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def ban_reset(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, current_user: User) -> bool:
    """ Reply command. Ban (set user's sticker limit to 0) and reset (set user's sticker count to 0) commands.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param current_user: A User object containing the user the operation is being performed on.

        :returns: A bool indicating whether the message triggers this function.
        """

    # ban
    if command == BAN:
        current_user.sticker_max = 0
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.USER_BANNED)
        return True
    # reset
    if command == RESET:
        current_user.sticker_count = 0
        text = responses.USER_LIMIT_RESET.format(amount=str(current_user.sticker_max))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
    """ Displays the list of commands

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.

        :returns: A bool indicating whether the message triggers this function.
        """
    if command == COMMANDS:
        text = responses.COMMANDS
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, users: Dict[int, User]) -> bool:
    """ Displays the list of commands

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param users: A dict containing the users, found by user ID.

        :returns: A bool indicating whether the message triggers this function.
        """
    if command == RESET_ALL_COUNT:
        for key, value in users.items():
            value.sticker_count = 0
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.COUNTS_RESET)
        return True
    return False


async def wipe(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, users: Dict[int, User]) -> bool:
    """ Wipes the data on all users, starts over fresh.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param users: A dict containing the users, found by user ID.

        :returns: A bool indicating whether the message triggers this function.
        """

    if command != WIPE:
        return False

    users.clear()
    try:
        os.remove("limit_tracker.p")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.USERS_WIPED)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.NO_FILE)
    except OSError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.CANT_DELETE_FILE)
    return True


async def set_limit(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, users: Dict[int, User],
                    users_cf: Dict[str, Union[int, bool]]) -> bool:
    """ Sets all user's sticker limits to X

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param users: A dict containing the users, found by user ID.
        :param users_cf: Dict of configuration settings relating to users.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Command has 3 parts: The command, a space, and a digit
    if not command.startswith(SET_ALL_LIMIT):  # Command starts with the limit command
        return False

    # Get the number from the command
    command_int = get_command_int(SET_ALL_LIMIT, command)
    if command_int is None:
        return False

    # Change the limit on each user
    for key, value in users.items():
        value.sticker_max = command_int
    users_cf['sticker_limit'] = command_int
    text = responses.SET_NEW_LIMIT.format(amount=str(command_int))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return True


async def get_limit(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                    users_cf: Dict[str, Union[int, bool]]) -> bool:
    """ Gets the current sticker limit

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param users_cf: Dict of configuration settings relating to users.

        :returns: A bool indicating whether the message triggers this function.
        """

    if command != GET_LIMIT:
        return False

    text = responses.GET_LIMIT.format(amount=str(users_cf['sticker_limit']))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return True


async def toggle_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, printer: Zebra,
                     state_cf: Dict[str, bool], printer_cf: Dict[str, Union[str, int]]) -> bool:
    """ Turns the bot on or off. Superuser commands can still be sent, but the bot will not respond anything else.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer: The Zebra printer object.
        :param state_cf: Dict of configuration settings relating to the state of the script.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Turn off bot
    if command == BOT_DISABLE:
        if state_cf['bot_enabled']:
            text = responses.BOT_DISABLED
        else:
            text = responses.BOT_ALREADY_DISABLED
        state_cf['bot_enabled'] = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    # Turn on bot
    if command == BOT_ENABLE:
        if state_cf['bot_enabled']:
            text = responses.BOT_ALREADY_ENABLED
        else:
            # Checks to make sure there is a valid print queue before enabling
            if printer_cf['printer_queue'].lower() in (queue.lower() for queue in printer.getqueues()):
                state_cf['bot_enabled'] = True
                text = responses.BOT_ENABLED
            else:
                text = responses.BOT_ENABLE_ERROR_NO_QUEUE

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def toggle_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                            state_cf: Dict[str, bool]) -> bool:
    """ Turns sticker monitoring on or off. Determines whether stickers that are printed are forwarded to superusers

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param state_cf: Dict of configuration settings relating to the state of the script.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Turn off sticker monitoring
    if command == STICKER_MONITORING_OFF:
        if state_cf['sticker_monitoring']:
            text = responses.MONITORING_DISABLED
        else:
            text = responses.MONITORING_ALREADY_DISABLED
        state_cf['sticker_monitoring'] = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    # Turn on sticker monitoring
    if command == STICKER_MONITORING_ON:
        if state_cf['sticker_monitoring']:
            text = responses.MONITORING_ALREADY_ENABLED
        else:
            text = responses.MONITORING_ENABLED
        state_cf['sticker_monitoring'] = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def get_print_offset(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                           printer_cf: Dict[str, Union[str, int]]) -> bool:
    """ Displays print offset and lists commands

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A bool indicating whether the message triggers this function.
        """

    if command == PRINT_OFFSET:
        text = responses.PRINT_OFFSET.format(offset_x=printer_cf["image_offset_x"],
                                             offset_y=printer_cf["image_offset_y"])

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def set_print_offset(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                           printer_cf: Dict[str, Union[str, int]]) -> bool:
    """ Sets a new x or y print offset

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Set the x (Horizontal) print offset
    if command.startswith(PRINT_OFFSET_X):
        command_int = get_command_int(PRINT_OFFSET_X, command)
        if command_int is not None:
            printer_cf["image_offset_x"] = command_int

            text = responses.SET_PRINT_OFFSET_X.format(offset_x=printer_cf["image_offset_x"])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return True

    # Set the y (vertical) print offset
    if command.startswith(PRINT_OFFSET_Y):
        command_int = get_command_int(PRINT_OFFSET_Y, command)
        if command_int is not None:
            printer_cf["image_offset_y"] = command_int

            text = responses.SET_PRINT_OFFSET_Y.format(offset_y=printer_cf["image_offset_y"])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return True

    return False


async def check_queue(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                      printer: Zebra, printer_cf: Dict[str, Union[str, int]]) -> bool:
    """ Display the current queue and checks if it exists on the system

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer: The Zebra printer object.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A bool indicating whether the message triggers this function.
        """

    if command != CHECK_QUEUE:
        return False

    if printer_cf['printer_queue'] == '':
        text = responses.CHECK_QUEUE_NO_QUEUE
    elif printer_cf['printer_queue'].lower() in (queue.lower() for queue in printer.getqueues()):
        text = responses.CHECK_QUEUE_SUCCESS.format(print_queue=printer_cf['printer_queue'])
    else:
        text = responses.CHECK_QUEUE_FAIL

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return True


async def list_queues(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, printer: Zebra) -> bool:
    """ Lists the print queues on the device

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer: The Zebra printer object.

        :returns: A bool indicating whether the message triggers this function.
        """

    if command != LIST_QUEUES:
        return False

    if len(printer.getqueues()) > 0:
        text = responses.LIST_QUEUES + "\n"
        for i in printer.getqueues():
            text += i + "\n"
    else:
        text = responses.LIST_QUEUES_NO_QUEUES

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return True


async def set_queue(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, printer: Zebra,
                    printer_cf: Dict[str, Union[str, int]]) -> bool:
    """ Changes the printer queue to the one specified

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param printer: The Zebra printer object.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A bool indicating whether the message triggers this function.
        """

    if not command.lower().startswith(SET_QUEUE):
        return False

    # If the space is in the correct position and the name of the printer is longer than 1 character
    if command[len(SET_QUEUE)] == " " and len(command[len(SET_QUEUE) + 1:]) > 1:
        # If the given printer queue name is in the list of the computer's queues
        if command[len(SET_QUEUE) + 1:] in printer.getqueues():
            printer_cf['printer_queue'] = command[len(SET_QUEUE) + 1:]
            text = responses.SET_QUEUE_SUCCESS
        else:
            text = responses.SET_QUEUE_BAD_QUEUE
    else:
        text = responses.SET_QUEUE_SYNTAX_ERROR

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return True


async def toggle_random_event(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,
                              state_cf: Dict[str, bool]) -> bool:
    """ Enables/disables random events

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param state_cf: Dict of configuration settings relating to the state of the script.

        :returns: A bool indicating whether the message triggers this function.
        """

    # Turn on random events
    if command == EVENT_ON:
        if state_cf['event']:
            text = responses.EVENT_ALREADY_ENABLED
        else:
            text = responses.EVENT_ENABLED
            state_cf['event'] = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    # Turn off random events
    if command == EVENT_OFF:
        if state_cf['event']:
            text = responses.EVENT_DISABLED
            state_cf['event'] = False
        else:
            text = responses.EVENT_ALREADY_DISABLED
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False


async def save_config(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, config: Dict) -> bool:
    """ Enables/disables random events

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param config: The Dict containing the rest of the _cf configuration dictionaries.

        :returns: A bool indicating whether the message triggers this function.
        """
    if command != SAVE:
        return False

    ConfigHandler.save_config(config)
    text = responses.CONFIG_SAVED
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return True


async def command_not_recognized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Displays a command not recognized error. Triggers when a user's message doesn't match any other commands.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        """
    text = responses.COMMAND_NOT_RECOGNIZED
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return
