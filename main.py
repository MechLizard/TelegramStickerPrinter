# This is an interactive bot that prints any Telegram stickers sent to it as a physical sticker

from __future__ import annotations
from telegram import Update
from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
)

import ConfigHandler
import StickerPrinter
import responses

config = ConfigHandler.read_config()
setup_cf = config['SETUP']

# Apply token
application = ApplicationBuilder().token(setup_cf['telegram_api_token']).build()


# =============================== #
# ======= Async Functions ======= #
# =============================== #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await StickerPrinter.start(update, context)


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await StickerPrinter.receive_text(update, context)


async def receive_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await StickerPrinter.receive_sticker(update, context, application)


async def animated_sticker_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=responses.ANIMATED_STICKER_ERROR)


# ==================== #
# ======= Main ======= #
# ==================== #
if __name__ == '__main__':

    # ==== Function Declarations ====#
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), receive_text)
    start_handler = CommandHandler('start', start)
    sticker_handler = MessageHandler(filters.Sticker.STATIC, receive_sticker)
    animated_sticker_handler = MessageHandler(filters.Sticker.ALL & (~filters.Sticker.STATIC), animated_sticker_error)
    photo_handler = MessageHandler(filters.PHOTO, receive_sticker)

    # ==== Handlers ==== #
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(sticker_handler)
    application.add_handler(photo_handler)
    application.add_handler(animated_sticker_handler)

    application.run_polling()
