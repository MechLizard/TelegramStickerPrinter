import io
import os
import random

import zpl
from PIL import Image
from pyrlottie import (LottieFile,
                       convSingleLottieFrames)

from user import User
import responses


def get_user(update, users, users_cf) -> User:
    # Find user in the users list
    current_user = users.get(update.message.from_user.id)
    if current_user is None:
        users[update.message.from_user.id] = User(update, users_cf)
        current_user = users[update.message.from_user.id]

    return current_user


async def limit_exceeded(update, context, current_user) -> bool:
    # Error if user has no stickers left
    if current_user.sticker_count >= current_user.sticker_max:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=current_user.get_limit_response()
        )
        return True

    return False


async def convert_sticker(update, sticker_file) -> Image:
    if update.message.sticker.is_animated:
        # For pyrlottie to convert animated images, it must be saved to disk.
        await sticker_file.download_to_drive(os.getcwd() + r"\animStickerBuff.tgs")
        g_lottie_file = LottieFile(os.getcwd() + r"\animStickerBuff.tgs")

        # Convert and extract frames
        frame_skip = 5000
        background_color = "FFFFFF"
        g_lottie_frames = await convSingleLottieFrames(g_lottie_file, background_color, frame_skip, 1)

        # Get the first item in the g_lottie_frames dict and get the first frame
        incoming_sticker = g_lottie_frames[list(g_lottie_frames)[0]].frames[0]
        incoming_sticker = incoming_sticker.convert("RGBA")
    else:
        # Static sticker
        sticker_buffer = io.BytesIO(b"")  # Create a memory buffer for the sticker to be downloaded to
        await sticker_file.download_to_memory(sticker_buffer)  # Download sticker
        incoming_sticker = Image.open(sticker_buffer).convert("RGBA")  # Create Image object
        sticker_buffer.close()

    return incoming_sticker


async def random_event(update, context, current_user, application, printer, users_cf, printer_cf):
    # Random event
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
            print_sticker(incoming_sticker, printer, printer_cf)
            sticker_buffer.close()


async def forward_to_superuser(update, current_user, setup_cf, state_cf):
    # forward Sticker to superusers if its enabled
    if state_cf['sticker_monitoring']:
        for i in setup_cf['super_user_id']:
            forwarded_message = await update.message.forward(i)
            current_user.log_message(forwarded_message.id)


def print_sticker(incoming_sticker, printer, printer_cf):
    # Takes a sticker object and prints it.
    # Input: A PIL Image object converted to RGBA format
    # Output: A print job sent to the Zebra printer queue in the config

    # TODO Make stickers resize in both directions until one side hits the edge. Use laughing emoji 😂 to test with kekw sticker
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

    del print_command_gen
    del sticker_img
