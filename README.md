# TelegramStickerPrinter
A telegram bot that accepts stickers and prints them out on a black and white zebra printer. I use a second hand QL320 Plus thermal printer for ultra cheap prints and the portable battery.   

Currently known to run on Windows computers, but I'm currently working on a headless build ran from a Raspberry Pi.

During setup one or multiple superusers or administrators can be assigned. Superusers/administrators can send commands to the bot to control it through Telegram. The goal is to be able to run this remotely from a phone. The computer running the code shouldn't need to be touched.

# Administrative Functions
A superuser can communicate with the bot through Telegram messages. These commands can:
 - Adjust the sticker limit
 - Get info on sticker limit, status, queue, and settings
 - Enable/disable the bot
 - Enable/disable sticker monitoring (forwards the printed stickers to the superusers)
 - Reply to a monitored sticker to reset/adjust a specific user's sticker limit or ban them
 - Adjust print offset and queue name

