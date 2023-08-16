import random

# First message when starting the bot
GREETING = "Hi! Send me any sticker and I'll print it!"

# Error when sent an animated sticker
ANIMATED_STICKER_ERROR = "Bitch, this ain't Harry Potter, I can't print an animated sticker"

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
    NOTE: DO NOT put these stickers on con/hotel walls. Do not put this on property that isn't yours. Don't be THAT furry.

These are paper stickers and they suck to remove. 
To remove them from something you can use isopropyl alcohol, WD-40, or Goo-Gone

Too much heat and friction will turn these black (It's basically receipt thermal paper). These will start fading in about 6 months and will fade faster in direct sunlight.

Have a good rest of your con!
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
CANT_FIND_USER_ERROR = "Can't find the user for that sticker"
USER_BANNED = "That user has been banned. They have 0 sticker limit"
USER_LIMIT_RESET = "That user has had their stickers reset. They now have "  # Variable and "sticker" at end
NO_FILE = "The user file is not found or no users have been recorded yet. Either way, it's a clean slate."
CANT_DELETE_FILE = "Unable to delete the user file"
SUPERUSER_NOT_SET = "There is no superuser set.\nEnter your Telegram user ID in BotConfig.ini in the \"super_user_id\" field"

# After the user sends a sticker. Picks at random from the list and inserted at "_____! Sending to the printer!"
def GetConfirmMessage():
    responses = [
        "Pog!",
        "As an AI language model that sticker is dope as fuck.",
        "👀👌💯",
        "...really?",
        "Nice!",
        "Wow, great choice!",
        "That's a juicy sticker right there.",
        "Coming right up!",
        "This one will look great on your water bottle you bring to work.",
        """...look, I don't judge. While I'm not in to that I understand that others are.
        
...Not that you're an \"other\" or anything like... look, just take your sticker.""",
        "Cool! That sticker is only 18% cringe!",
        "Thank you for signing up for the furry surveillance program. We are now watching.",
    ]

    return responses[random.randint(0, len(responses)) - 1] + " Sending to the printer!"
