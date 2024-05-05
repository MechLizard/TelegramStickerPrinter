import random
import constants

# First message when starting the bot
GREETING = "Hi! Send me any sticker or picture and I'll print it!\n\n" \
    "You have {amount} stickers left."

OUT_OF_STICKERS = "You are now out of stickers :("
STICKER_COUNT = "You still have {count} stickers left."
STICKER_PRINTED = "Sending to the printer!"

# Unresponsive printer message
PRINTER_OFFLINE = "Oof, printer isn't responding. Maybe try again?"

# No such printer queue
MISSING_QUEUE = "No such printer queue or missing printer queue in BotConfig.ini.\n" \
                "Here is a list of printer queues on this device:"

BONUS_STICKER_MESSAGE = "Also, since you've been so nice I'm also printing this bonus sticker just for you:"
# "I'm also printing this one for you to remember me!"
# "I'm also printing this one just for you!

END_MESSAGE = r"""
You are now out of stickers :(

NOTE: DO NOT put these on property that isn't yours.

These are paper stickers and they're annoying to remove. Use isopropyl alcohol, WD-40, or Goo-Gone to make it easier.

Too much heat will turn these black. Will start fading in a few years and will fade faster in direct sunlight or with frequent friction.

Have a good con!

<a href="https://github.com/MechLizard/TelegramStickerPrinter">Github of this code</a> and <a href="https://about.me/IzzyJones">check me out</a> if you're hiring.
"""

# ==== Super user responses ==== #
LOGS_CLEARED = "User limits have been reset"
USERS_WIPED = "All users wiped"
COUNTS_RESET = "All user counts reset"
SET_NEW_LIMIT = "New sticker limit set to {amount}"
GET_LIMIT = "Sticker limit is currently {amount}"
ADD_USER_LIMIT = "Added {amount} stickers to that user. They now have a limit of {total}"
SUBTRACT_USER_LIMIT = "Removed {amount} stickers from that user. " \
    "They now have a limit of {total}"
SET_USER_LIMIT = "That user now has a limit of {total}"
BOT_DISABLED = "The bot has been disabled"
BOT_ENABLED = "The bot has been enabled"
BOT_ALREADY_DISABLED = "The bot is already disabled"
BOT_ALREADY_ENABLED = "The bot is already enabled"
MONITORING_ENABLED = "Sticker monitoring enabled"
MONITORING_DISABLED = "Sticker monitoring disabled"
MONITORING_ALREADY_ENABLED = "Sticker monitoring already enabled"
MONITORING_ALREADY_DISABLED = "Sticker monitoring already disabled"
EVENT_ENABLED = "Random event enabled"
EVENT_DISABLED = "Random event disabled"
EVENT_ALREADY_ENABLED = "Random event is already enabled"
EVENT_ALREADY_DISABLED = "Random event is already disabled"
CANT_FIND_USER_ERROR = "Can't find the user for that sticker"
USER_BANNED = "That user has been banned. They have 0 sticker limit"
USER_LIMIT_RESET = "That user has had their stickers reset. They now have {amount} stickers."
PRINT_OFFSET = """
The current print offset in pixels:
Print offset x = {offset_x}
Print offset y = {offset_y}  

Change these by typing \"print offset x/y \" and a number.
x is horizontal, y is vertical offset"
Ex: print offset x 5
Ex: print offset y -15"""
SET_PRINT_OFFSET_X = "The x (horizontal) offset is now set to {offset_x}"
SET_PRINT_OFFSET_Y = "The y (vertical) offset is now set to {offset_y}"
SET_QUEUE_INSTRUCTIONS = f"Check connection or set the queue with \"{constants.LIST_QUEUES}\" " \
                            f"and \"{constants.SET_QUEUE}\""
CHECK_QUEUE_NO_QUEUE = "There is no printer queue set.\n\n" + SET_QUEUE_INSTRUCTIONS
CHECK_QUEUE_SUCCESS = "The print queue exists.\n\n" \
    "The current print queue is {print_queue}"
CHECK_QUEUE_FAIL = "The current print queue is not found in the system.\n\n" + SET_QUEUE_INSTRUCTIONS
LIST_QUEUES = "These are the current queues: "
LIST_QUEUES_NO_QUEUES = "There are currently no printer queues on this system. Connect a printer and try again."
SET_QUEUE_SUCCESS = "Print queue has been set"
SET_QUEUE_SYNTAX_ERROR = "Improper syntax. You must have the command, a space, and then the print queue name.\n" \
                         f"Ex: {constants.SET_QUEUE} Zebra_QL320plus"
SET_QUEUE_BAD_QUEUE = f"That print queue does not exist on this device. \n" \
                      f"Use \"{constants.LIST_QUEUES}\" to list the current print queues on this device"
BOT_ENABLE_ERROR_NO_QUEUE = "Bot enable failed. The print queue is not available.\n\n" + SET_QUEUE_INSTRUCTIONS
NO_FILE = "The user file is not found or no users have been recorded yet. Either way, it's a clean slate."
CANT_DELETE_FILE = "Unable to delete the user file."
CONFIG_SAVED = "Configuration has been saved."
SUPERUSER_NOT_SET = r"""
There is no superuser set.
Enter your Telegram user ID in the "super_user_id" field in BotConfig.ini

Your user ID is: {id}
"""
COMMAND_NOT_RECOGNIZED = f"Command not recognized. Type \"{constants.COMMANDS}\" for a list of commands"
COMMANDS = f"""
General commands:
\"{constants.RESET_ALL_COUNT}\" - Resets sticker count to 0
\"{constants.WIPE}\" - Wipes all users
\"{constants.SET_ALL_LIMIT} X\" - Sets sticker limit to X
\"{constants.GET_LIMIT}\" - Shows the current sticker limit
\"{constants.BOT_ENABLE}\" - Enables the bot
\"{constants.BOT_DISABLE}\" - Disables the bot
\"{constants.STICKER_MONITORING_ON}\" - Turn on monitoring (sends superusers all printed stickers)
\"{constants.STICKER_MONITORING_OFF}\" - Turn off monitoring
\"{constants.EVENT_ON}\" - Turn on random events
\"{constants.EVENT_OFF}\" - Turn off random events
\"{constants.COMMANDS}\" - Displays this help message
\"{constants.SAVE}\" - Save current settings to config file

Printer commands:
\"{constants.PRINT_OFFSET}\" - Displays the current print offset and displays commands for adjusting
\"{constants.CHECK_QUEUE}\" - Displays the current queue and checks if it exists
\"{constants.LIST_QUEUES}\" - Lists the print queues on the device
\"{constants.SET_QUEUE}\" - Sets the print queue (Ex: {constants.SET_QUEUE} Zebra_QL230)

"Reply commands (Reply to a monitored sticker):
[+ or - or =][number] - Add, subtract, or set sticker limit (Ex: +5, -1, or =999)
\"{constants.BAN}\" - Bans the user. Sets their limit to 0
\"{constants.RESET}\" - Resets the user's used stickers to 0. Lets them print more"""


def get_confirm_message():
    """ Randomized confirmation message for after a sticker is successfully sent to the printer.
        Picks at random from the list and inserted at "_____! Sending to the printer!"
    """
    responses = [
        "Pog!",
        "As an AI language model that sticker is dope as fuck.",
        "👀👌💯",
        "😎👌 🤨🕶👌 ...okay.",
        "...really?",
        "Nice!",
        "Wow, great choice!",
        "That's a juicy sticker right there.",
        "Coming right up!",
        "This one will look great on your water bottle you bring to work.",
        #"""...look, I don't judge. While I'm not in to that I understand that others are.
        #
#...Not that you're an \"other\" or anything like... look, just take your sticker.""",
        "That sticker is only 18% cringe!",
        "Thank you for signing up for the furry surveillance program. We are now watching.",
    ]

    return responses[random.randint(0, len(responses)) - 1] + " Sending to the printer!"
