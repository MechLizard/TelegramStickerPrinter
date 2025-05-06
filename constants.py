# ==== Superuser commands ==== #
# After setting your Telegram chat ID, send these strings to the bot over Telegram to interact with it.

# Lists these commands
COMMANDS = "commands"

# Resets all users to 0 used stickers
RESET_ALL_COUNT = "resetall"

# Wipes all users
WIPE = "wipe"

# Clears sticker history for the /random feature
CLEAR_HISTORY = "clearhistory"

# Set all limits to X
# Command has 3 parts: The command, a space, and a digit. Ex: setlimit 10
SET_ALL_LIMIT = "setlimit"

# Get the current default sticker limit
GET_LIMIT = "limit"

# Turn the bot on or off
BOT_ENABLE = "enable"
BOT_DISABLE = "disable"

# Turn sticker monitoring on or off. (Whether the bot sends you the stickers that are printed)
STICKER_MONITORING_ON = "monitor on"
STICKER_MONITORING_OFF = "monitor off"

# Turn random event on or off
EVENT_ON = "event on"
EVENT_OFF = "event off"

# Turn slap detection on or off
SLAP_ON = "slap on"
SLAP_OFF = "slap off"

# Turn random sticker printing on or off
RANDOM_ON = "random on"
RANDOM_OFF = "random off"

# == Reply-to commands == #
# = Reply to a forwarded sticker with these commands = #

# Add, subtract, or set sticker limit (Ex: +5, -1, or =999)
# Command: [+ or - or =][number]

# Set user's sticker limit to 0
BAN = "ban"

# Sets user's stickers printed to 0
RESET = "reset"

# Removes the sticker from the pool of stickers the /random feature chooses from
REMOVE = "remove"

# Displays current offset and explains how to use the offset commands
PRINT_OFFSET = "print offset"

# Adjust the x (Horizontal) offset of the image
PRINT_OFFSET_X = "print offset x"

# Adjust the y (vertical) offset of the image
PRINT_OFFSET_Y = "print offset y"

# Displays the current queue and checks if it exists
CHECK_QUEUE = "check queue"

# Lists the print queues on the device
LIST_QUEUES = "list queues"

# Sets the print queue to your specification
SET_QUEUE = "set queue"

# Saves configuration
SAVE = "save"
