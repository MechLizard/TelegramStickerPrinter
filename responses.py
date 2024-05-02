import random
import constants

# First message when starting the bot
GREETING = "Hi! Send me any sticker and I'll print it!"

OUT_OF_STICKERS = "Sorry, but you are out of stickers :("
STICKER_PRINTED = "Sending to the printer!"

# Unresponsive printer message
PRINTER_OFFLINE = "Oof, printer isn't responding. Maybe try again?"

# No such printer queue
MISSING_QUEUE = "No such printer queue or missing printer queue in BotConfig.ini.\n" \
                "Here is a list of printer queues on this device:"

BONUS_STICKER_MESSAGE = "Also, since you've been so nice I'm also printing this bonus sticker just for you:"
# "I'm also printing this one for you to remember me!"
# "I'm also printing this one just for you!

END_MESSAGE = """
You are now out of stickers :(

NOTE: DO NOT put this on property that isn't yours. Don't be THAT furry.

These are paper stickers and they're annoying to remove. Use isopropyl alcohol, WD-40, or Goo-Gone to make it easier.

Too much heat will turn these black. These will start fading in a few years and will fade faster in direct sunlight or with constant gentle friction.

Have a good con!
"""

# ==== Super user responses ==== #
LOGS_CLEARED = "User limits have been reset"
USERS_WIPED = "All users wiped"
COUNTS_RESET = "All user counts reset"
SET_NEW_LIMIT = "New sticker limit set to "  # Variable at end
GET_LIMIT = "Sticker limit is currently "  # Variable at end
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
USER_LIMIT_RESET = "That user has had their stickers reset. They now have "  # Variable and "sticker" at end
PRINT_OFFSET_LIST = "The current print offset in pixels:"
PRINT_OFFSET_INSTRUCTIONS = "Change these by typing \"print offset x/y \" and a number." \
                            "\nx is horizontal, y is vertical offset"
PRINT_OFFSET_X_EXAMPLE = "Ex: print offset x 5"
PRINT_OFFSET_Y_EXAMPLE = "Ex: print offset y -15"
SET_PRINT_OFFSET_X = "The x (horizontal) offset is now set to "
SET_PRINT_OFFSET_Y = "The x (vertical) offset is now set to "
SET_QUEUE_INSTRUCTIONS = f"Check connection or set the queue with \"{constants.LIST_QUEUES}\" " \
                            f"and \"{constants.SET_QUEUE}\""
CHECK_QUEUE_NO_QUEUE = "There is no printer queue set.\n\n" + SET_QUEUE_INSTRUCTIONS
CHECK_QUEUE_SUCCESS = "The print queue exists."
CHECK_QUEUE_FAIL = "The current print queue is not found in the system.\n\n" + SET_QUEUE_INSTRUCTIONS
LIST_QUEUES = "These are the current queues: "
LIST_QUEUES_NO_QUEUES = "There are currently no printer queues on this system. Connect a printer and try again"
SET_QUEUE_SUCCESS = "Print queue has been set"
SET_QUEUE_SYNTAX_ERROR = "Improper syntax. You must have the command, a space, and then the print queue name\n" \
                         f"Ex: {constants.SET_QUEUE} Zebra_QL320plus"
SET_QUEUE_BAD_QUEUE = f"That print queue does not exist on this device. \n" \
                      f"Use \"{constants.LIST_QUEUES}\" to list the current print queues on this device"
BOT_ENABLE_ERROR_NO_QUEUE = "Bot enable failed. The print queue is not available.\n\n" + SET_QUEUE_INSTRUCTIONS
NO_FILE = "The user file is not found or no users have been recorded yet. Either way, it's a clean slate."
CANT_DELETE_FILE = "Unable to delete the user file"
SUPERUSER_NOT_SET = "There is no superuser set.\n" \
                    "Enter your Telegram user ID in BotConfig.ini in the \"super_user_id\" field"

# After the user sends a sticker. Picks at random from the list and inserted at "_____! Sending to the printer!"
def GetConfirmMessage():
    responses = [
        "Pog!",
        "As an AI language model that sticker is dope as fuck.",
        "👀👌💯",
        "😎👌 😕🕶👌 ...okay.",
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
