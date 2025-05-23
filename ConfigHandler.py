import configparser
import ast


def get_default_config():
    setup = {'telegram_api_token': '',
             'super_user_id': [],
             'echo_chat_id': False}

    printer = {'printer_queue': '',
               'media_in_x': 2,
               'media_in_y': 2,
               'dpi': 200,
               'media_gap_mm': 5,
               'image_offset_x': 15,
               'image_offset_y': 2}

    users = {'sticker_limit': 10,
             'unlimited_stickers': False,
             'ran_event_start': 0.6,
             'ran_event_chance': 60}

    state = {'bot_enabled': True,
             'sticker_monitoring': True,
             'random_sticker_printing': True,
             'event': False,
             'slap_detection': False}

    default_config = {'SETUP': setup,
                      'PRINTER': printer,
                      'USERS': users,
                      'STATE': state}

    return default_config


def save_config(config_info):
    config = configparser.ConfigParser(allow_no_value=True)

    # Copy and convert all the values to strings. ConfigParser requires this
    save_conf = config_info.copy()
    for outer_key, inner_dict in config_info.items():
        save_conf[outer_key] = inner_dict.copy()
        for inner_key, inner_value in inner_dict.items():
            save_conf[outer_key][inner_key] = str(inner_value)

    # SETUP section
    config.add_section('SETUP')
    config.set('SETUP', '# The token you got from Telegram\'s BotFather as a string', None)
    config.set('SETUP', 'TELEGRAM_API_TOKEN', save_conf['SETUP']['telegram_api_token'])

    config.set('SETUP', '# The ID of the user that is allowed to give moderator commands. Can add multiple, each separated by a comma. A list of ints (can be one)', None)
    config.set('SETUP', 'SUPER_USER_ID', save_conf['SETUP']['super_user_id'])

    config.set('SETUP', '# When sending a text message to the bot, will it respond with your chat ID? Used to get your ID to set the SUPER_USER_ID', None)
    config.set('SETUP', 'ECHO_CHAT_ID', save_conf['SETUP']['echo_chat_id'])

    # PRINTER section
    config.add_section('PRINTER')
    config.set('PRINTER', '# The name of the printer queue. Use the "printers" command to get a list of printer queues on the host.', None)
    config.set('PRINTER', 'PRINTER_QUEUE', save_conf['PRINTER']['printer_queue'])

    config.set('PRINTER', '# Real size of the physical sticker in inches - Width', None)
    config.set('PRINTER', 'MEDIA_IN_X', save_conf['PRINTER']['media_in_x'])

    config.set('PRINTER', '# Real size of the physical sticker in inches - Height', None)
    config.set('PRINTER', 'MEDIA_IN_Y', save_conf['PRINTER']['media_in_y'])

    config.set('PRINTER', '# Dots per inch of the printer (DPI). Should be displayed on the printer\'s sal', None)
    config.set('PRINTER', 'DPI', save_conf['PRINTER']['dpi'])

    config.set('PRINTER', '# The gap between stickers measured in millimeters', None)
    config.set('PRINTER', 'MEDIA_GAP_MM', save_conf['PRINTER']['media_gap_mm'])

    config.set('PRINTER', '# Amount of pixels to offset the image if it isn\'t centered correctly - X', None)
    config.set('PRINTER', 'IMAGE_OFFSET_X', save_conf['PRINTER']['image_offset_x'])

    config.set('PRINTER', '# Amount of pixels to offset the image if it isn\'t centered correctly - Y', None)
    config.set('PRINTER', 'IMAGE_OFFSET_Y', save_conf['PRINTER']['image_offset_y'])

    # USERS section
    config.add_section('USERS')
    config.set('USERS', '# The max stickers the users get', None)
    config.set('USERS', 'STICKER_LIMIT', save_conf['USERS']['sticker_limit'])

    config.set('USERS', '# Ignores the above limit. Does not limit stickers', None)
    config.set('USERS', 'UNLIMITED_STICKERS', save_conf['USERS']['unlimited_stickers'])

    config.set('USERS', '# From 0 to 1. Determines which point the random events should start. Percentage of stickers left before events happen.', None)
    config.set('USERS', 'RAN_EVENT_START', save_conf['USERS']['ran_event_start'])

    config.set('USERS', '# From 0 to 100. Percent chance for random events to happen when enabled', None)
    config.set('USERS', 'RAN_EVENT_CHANCE', save_conf['USERS']['ran_event_chance'])

    # STATE section
    config.add_section('STATE')
    config.set('STATE', '# Whether the bot is enabled at the start', None)
    config.set('STATE', 'BOT_ENABLED', save_conf['STATE']['bot_enabled'])

    config.set('STATE', '# Whether sticker monitoring is enabled by default', None)
    config.set('STATE', 'STICKER_MONITORING', save_conf['STATE']['sticker_monitoring'])

    config.set('STATE', '# Whether the random sticker printing user feature is enabled by default', None)
    config.set('STATE', 'RANDOM_STICKER_PRINTING', save_conf['STATE']['random_sticker_printing'])

    config.set('STATE', '# Whether the random event is enabled by default', None)
    config.set('STATE', 'EVENT', save_conf['STATE']['event'])

    config.set('STATE', '# Whether slap detection is enabled by default', None)
    config.set('STATE', 'SLAP_DETECTION', save_conf['STATE']['slap_detection'])

    with open('BotConfig.ini', 'w') as configfile:
        config.write(configfile)


def read_config():
    config_dict = {}
    config = configparser.ConfigParser()

    # Read in BotConfig.ini. If it doesn't exist get a default one.
    try:
        with open('BotConfig.ini') as f:
            config.read_file(f)
        for section in config.sections():
            config_dict[section] = dict(config[section])
    except IOError:
        config_dict = get_default_config()
        save_config(config_dict)

    config.read('BotConfig.ini')

    # Convert the strings from the .ini in to their appropriate variable types
    for outer_key, inner_dict in config_dict.items():
        for inner_key, inner_value in inner_dict.items():
            try:
                # Try to convert the string to a number or bool
                inner_dict[inner_key] = ast.literal_eval(inner_value)
            except ValueError:
                # If fails, that means it was already the correct value
                pass
            # This is there because the format of the api token can cause a syntax error
            except SyntaxError:
                pass

    # === Conversions and math stuff === #

    # size of the sticker in pixels
    # Ex: DPI of Zebra QL320 is 200dpi(dots per inch). 2" x 2" = 400x400 image size
    config_dict['PRINTER']['media_size_x'] = config_dict['PRINTER']['media_in_x'] * config_dict['PRINTER']['dpi']
    config_dict['PRINTER']['media_size_y'] = config_dict['PRINTER']['media_in_y'] * config_dict['PRINTER']['dpi']

    # Real size of the physical sticker in mm
    config_dict['PRINTER']['media_mm_x'] = round(config_dict['PRINTER']['media_in_x'] * 25.4)
    config_dict['PRINTER']['media_mm_y'] = round(config_dict['PRINTER']['media_in_y'] * 25.4)

    # Dots per millimeter
    # Ex: if dpi of printer is 200. Note: 25.4 is the amount of millimeters in an inch.
    # 1/25.4 * 200(the dpi) = 7.87. Rounded to whole number
    config_dict['PRINTER']['dpmm'] = round((1 / 25.4) * config_dict['PRINTER']['dpi'])

    # The gap between stickers measured in dots
    # If gap is 5mm and DPI=200dpi.
    # Then dots per mm is ~39 (5(mm) / 25.4(mm per inch) * 200(dpi) = 39.37)
    config_dict['PRINTER']['media_gap'] = round((1 / 25.4) * config_dict['PRINTER']['dpi'] * config_dict['PRINTER']['media_gap_mm'])

    return config_dict
