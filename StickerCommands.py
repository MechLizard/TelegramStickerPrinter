import io
import random
from typing import Dict, Union

import zpl
from zebra import Zebra
from PIL import Image
from telegram import (Update, File)
from telegram.ext import (ContextTypes, Application)

from user import User
import responses


def get_user(update: Update, users: Dict[int, User], users_cf: Dict[str, Union[int, bool]]) -> User:
    """ Finds a user in the users Dict and returns them.
    Adds a new user to the dict if not found and returns that.

        :param update: Update object containing the sent message.
        :param users: A dict containing the users, found by user ID.
        :param users_cf: Dict of configuration settings relating to users.

        :returns: A User object containing the user.
    """

    current_user = users.get(update.message.from_user.id)
    if current_user is None:
        users[update.message.from_user.id] = User(update, users_cf)
        current_user = users[update.message.from_user.id]

    return current_user


async def limit_exceeded(update: Update, context: ContextTypes.DEFAULT_TYPE, current_user: User) -> bool:
    """ Displays an error to the user if their sticker limit is exceeded.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param current_user: A User object containing the user the operation is being performed on.

        :returns: A bool whether the user's limit is exceeded.
        """

    if current_user.sticker_count >= current_user.sticker_max:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=current_user.get_limit_response()
        )
        return True

    return False


async def convert_sticker(update: Update, sticker_file: File, printer_cf: Dict[str, Union[str, int]]) -> Image:
    """ Converts the downloaded sticker or picture to a format the printer can accept

        :param update: Update object containing the sent message.
        :param sticker_file: The unprocessed downloaded image sent to the bot.
        :param printer_cf: Dict of configuration settings relating to the printer.

        :returns: A PIL Image file containing the printable image.
        """

    # Static sticker or Image
    sticker_buffer = io.BytesIO(b"")  # Create a memory buffer for the sticker to be downloaded to
    await sticker_file.download_to_memory(sticker_buffer)  # Download sticker
    incoming_sticker = Image.open(sticker_buffer).convert("RGBA")  # Create Image object
    sticker_buffer.close()

    # Resize the media without changing aspect ratio so that it fills the media without stretching the image.
    ratio_x = printer_cf['media_size_x'] / incoming_sticker.size[0]
    ratio_y = printer_cf['media_size_y'] / incoming_sticker.size[1]
    scale_factor = min(ratio_x, ratio_y)
    new_img_x = int(incoming_sticker.size[0] * scale_factor)
    new_img_y = int(incoming_sticker.size[1] * scale_factor)
    incoming_sticker = incoming_sticker.resize((new_img_x, new_img_y))

    # Create a centered offset to paste the image on to a canvas matching the print media.
    print_offset_x = (printer_cf['media_size_x'] - new_img_x) // 2
    print_offset_y = (printer_cf['media_size_y'] - new_img_y) // 2

    # Create a canvas the size of the print media and paste the sticker on it.
    print_image = Image.new("RGBA",
                            (printer_cf['media_size_x'],
                             printer_cf['media_size_y']),
                            color="white")  # Uses white background so that transparent pixels don't show up as black.
    print_image.paste(incoming_sticker, (print_offset_x, print_offset_y), mask=incoming_sticker)
    print_image = print_image.convert("1")  # Convert image to 1-byte B&W image

    return print_image


async def random_event(update: Update, context: ContextTypes.DEFAULT_TYPE, current_user: User, application: Application,
                       printer: Zebra, state_cf: Dict[str, bool], users_cf: Dict[str, Union[int, bool]],
                       printer_cf: Dict[str, Union[str, int]]):
    """ If the right conditions are met, print a 'bonus' sticker from a pre-prepared sticker pack

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param current_user: A User object containing the user the operation is being performed on.
        :param application: Object containing the general bot interface.
        :param printer: The Zebra printer object.
        :param state_cf: Dict of configuration settings relating to the state of the script.
        :param users_cf: Dict of configuration settings relating to users.
        :param printer_cf: Dict of configuration settings relating to the printer.
        """

    # If random events are disabled, return.
    if not state_cf['event']:
        return

    # Random event
    if current_user.sticker_count / current_user.sticker_max >= users_cf['ran_event_start']:
        if not current_user.bonus_sticker_encounter and random.randint(1, 100) <= users_cf['ran_event_chance']:
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


async def forward_to_superuser(update: Update, current_user: ContextTypes.DEFAULT_TYPE,
                               setup_cf: Dict[str, Union[str, list, bool]], state_cf: Dict[str, bool]):
    """ If enabled, forwards the image to the superusers

        :param update: Update object containing the sent message.
        :param current_user: A User object containing the user the operation is being performed on.
        :param setup_cf: Dict of api token and superuser IDs.
        :param state_cf: Dict of configuration settings relating to the state of the script.
        """
    # forward Sticker to superusers if its enabled
    if state_cf['sticker_monitoring']:
        for i in setup_cf['super_user_id']:
            forwarded_message = await update.message.forward(i)
            current_user.log_message(forwarded_message.id)


def print_sticker(print_image: Image, printer: Zebra, printer_cf: Dict[str, Union[str, int]]):
    """ Takes an image and sends it to the specified print queue in the printer object

        :param print_image: The PIL Image object that is already converted to printable format via convert_sticker
        :param printer: The Zebra printer object
        :param printer_cf: Dict of configuration settings relating to the printer.
        """

    print_command_gen = zpl.Label(printer_cf['media_mm_x'], printer_cf['media_mm_y'], printer_cf['dpmm'])
    # sticker_img.show()  # Can be used to display the sticker on the host

    print_command_gen.origin(printer_cf['image_offset_x'],
                             printer_cf['image_offset_y'])
    print_command_gen.write_graphic(print_image, printer_cf['media_mm_x'])
    print_command_gen.endorigin()

    # print(print_command_gen.dumpZPL())  # Can be used to display the print commands
    printer.output(print_command_gen.dumpZPL())

    del print_command_gen
    del print_image
