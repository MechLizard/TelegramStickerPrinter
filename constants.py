# TODO: Make these togglable via messages on telegram to make it headless.

# ==== Superuser commands ==== #
# After setting your Telegram chat ID, send these strings to the bot over Telegram to interact with it.

# Lists these commands
COMMANDS = "commands"

# Resets all users to 0 used stickers
RESET_ALL_COUNT = "resetall"

# Wipes all users
WIPE = "wipe"

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

# == Reply-to commands == #
# = Reply to a forwarded sticker with these commands = #

# Add, subtract, or set sticker limit (Ex: +5, -1, or =999)
# Command: [+ or - or =][number]

# Set user's sticker limit to 0
BAN = "ban"

# Sets user's stickers printed to 0
RESET = "reset"

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


"""
# === Conversions and math stuff === #
# Probably don't touch this

# size of the sticker in pixels
# Ex: DPI of Zebra QL320 is 200dpi(dots per inch). 2" x 2" = 400x400 image size
MEDIA_SIZE_X = MEDIA_IN_X * DPI
MEDIA_SIZE_Y = MEDIA_IN_Y * DPI

# Real size of the physical sticker in mm
MEDIA_MM_X = round(MEDIA_IN_X * 25.4)
MEDIA_MM_Y = round(MEDIA_IN_X * 25.4)

# Dots per millimeter
# Ex: if dpi of printer is 200. Note: 25.4 is the amount of millimeters in an inch.
# 1/25.4 * 200(the dpi) = 7.87. Rounded to whole number
DPMM = round((1/25.4) * DPI)

# The gap between stickers measured in dots
# If gap is 5mm and DPI=200dpi.
# Then dots per mm is ~39 (5(mm) / 25.4(mm per inch) * 200(dpi) = 39.37)
MEDIA_GAP = round((1/25.4) * DPI * MEDIA_GAP_MM)"""