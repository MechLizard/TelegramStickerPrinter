# This module is to have the printer experience pleasure.
# If an MPU6050, MPU6500, or MPU9250 is connected to the raspberry pi, then this module will be enabled.
# This detects a sudden impact on the module and will print out a processed sticker in the processed_slap_image folder.


import time
import logging
import os
import random
from typing import Dict, Union
from math import sqrt
from collections import deque

import mpu6050
from PIL import Image
from zebra import Zebra

import StickerCommands

# Create a new Mpu6050 object
mpu6050_object = mpu6050.mpu6050(0x68)
# Poke MPU to check if its connected
mpu6050_object.get_accel_data()


class SlapDetection:
    def __init__(self, state: bool, printer: Zebra, printer_cf: Dict[str, Union[str, int]]):
        """ Initialise by loading the images in slap_images folder and convert them to a printable format.
        :param state: A bool that determines whether this module is enabled by default
        :param printer: The Zebra printer object.
        :param printer_cf: Dict of configuration settings relating to the printer.
        """

        self.detection_enabled = state

        self.slap_list = []

        # Go through slap_images and convert them to a quick printing format, and store them in slap_list in memory
        image_file = "./slap_images"
        for file in os.listdir(image_file):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Open the image and convert it to a printable format
                im = StickerCommands.convert_sticker_local(Image.open(image_file + "/" + file))
                # Convert image into printer commands
                commands = StickerCommands.get_print_command(im, printer, printer_cf)
                # If needed, encode commands properly
                if type(commands) is not bytes:
                    commands = str(commands).encode(encoding='cp437')

                self.slap_list.append(commands)

        if len(self.slap_list) == 0:
            raise FileNotFoundError("No .jpg or .png images in slap_images folder.")

    def slap_detection(self, printer: Zebra):
        """ Repeatedly checks if there is an impact on the accelerometer.
        If an impact is detected, print the prepared sticker

        :param printer: The Zebra printer object.
        """

        # Adjustables
        sleep_time = 0.02  # How long should the program sleep between measurements
        tick_amount = 2  # How many measurement readings will be performed to get the change over time
        cot_limit = 10  # Acceleration change over time maximum over tick_amount ticks

        queue = deque()
        for i in range(tick_amount):
            queue.append(9.5)
        cot = (tick_amount - 1) * 9.5
        prev = 9.5  # Usual average value

        logging.info("Slap module ready...")

        while True:
            while self.detection_enabled:
                # Read the sensor data
                accel = mpu6050_object.get_accel_data()

                acceleration = sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)
                change = abs(prev - acceleration)  # amount of acceleration since the last reading
                prev = acceleration

                # Adds up the amount of change over how many readings equal to tick_amount
                cot += change
                queue.append(change)
                cot -= queue.popleft()

                # If the change over time is greater than the cot_limit
                if cot > cot_limit:
                    printer.output(random.choice(self.slap_list))
                    logging.info("Printing slap sticker")
                    time.sleep(2)
                    queue.clear()
                    # Set the tracking variables back to normal acceleration
                    for i in range(tick_amount):
                        queue.append(9.5)
                    cot = (tick_amount - 1) * 9.5
                    prev = 9.5

                time.sleep(sleep_time)

            while not self.detection_enabled:
                time.sleep(3)

    def change_state(self, change: bool):
        """ Changes whether this module is enabled

        :param change: a bool determining if slap detection is enabled
        """
        self.detection_enabled = change
