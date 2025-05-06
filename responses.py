import random
from unittest import case

import constants

GITHUB_LINK = "https://github.com/MechLizard/TelegramStickerPrinter"
OWNER_TELEGRAM = "@MechLizard"

# First message when starting the bot
GREETING = ("Hi! Send me any sticker or picture and I'll print it!\n\n"
            "/random prints a random sticker previously sent to the printer by anyone.\n"
            "/optout to opt out of having your stickers saved for the /random feature.\n\n"
            "You have {amount} stickers left.")

# Response for /help user command
HELP = ("I can print any (non-animated) sticker or picture. You can forward images or stickers from other users to me, too.\n\n"
        "/random to print a random sticker sent by anyone previously (If feature is enabled).\n"
        "/optout to opt out of having your stickers saved for the /random feature. "
        "This also deletes any previous stickers you've previously sent from the list."
        "However your stickers may still be monitored for moderation purposes.\n\n"
        "Note: What you send is monitored. What you send may be saved to be printed again via the \\random command\n\n"
        "<a href=\"" + GITHUB_LINK + "\">Github of this code</a>\n\n"
        "Owner: " + OWNER_TELEGRAM + "\n\n"
        "You have {amount} stickers left.")


OUT_OF_STICKERS = "You are now out of stickers :("
STICKER_COUNT = "You still have {count} stickers left."
STICKER_PRINTED = "Sending to the printer!"

# Unresponsive printer message
PRINTER_OFFLINE = "Oof, printer isn't responding. Maybe try again?"

# Connection timed out
MESSAGE_TIMED_OUT_RETRYING = "Connection timed out. Retrying..."
MESSAGE_TIMED_OUT = "Sorry, but the internet here is pretty bad. please try again!"

# No such printer queue
MISSING_QUEUE = "No such printer queue or missing printer queue in BotConfig.ini.\n" \
                "Here is a list of printer queues on this device:"

BONUS_STICKER_MESSAGE = "Also, since you've been so nice I'm also printing this bonus sticker just for you:"
# "I'm also printing this one for you to remember me!"
# "I'm also printing this one just for you!

RANDOM_WARNING = ("This will print a random sticker sent by anyone previously. "
                  "This may include explicit or surprising images. Continue?")
RANDOM_WARNING_CANCEL = "Okay! Canceled."

ANIMATED_STICKER_ERROR = "This isn't harry potter, I can't print animated stickers."
STICKER_HISTORY_OPT_OUT = ("You've opted out of having your stickers recorded for use in the random print feature. "
                           "Any stickers you sent previously will also be removed from the list. "
                           "Your stickers may still be monitored by an admin for moderation purposes.")
STICKER_HISTORY_ALREADY_OPTED_OUT = ("You've already opted out of having your stickers recorded for use in the random print feature. "
                           "Any stickers you sent previously were also removed from the list. "
                           "Your stickers may still be monitored by an admin for moderation purposes.")
RANDOM_DISABLED_ERROR = "Sorry, random sticker printing is currently disabled :("
RANDOM_QUEUE_EMPTY_ERROR = "Sorry, can't print a random sticker because there are no stickers in the history D:"
RANDOM_CHOSEN_STICKER = "Your random sticker:"
RANDOM_NO_SENDABLE_STICKERS = "Looks like there is no existing saved stickers. Try sending a few first."



END_MESSAGE = r"""
You are now out of stickers :(

NOTE: DO NOT put these on property that isn't yours.

These are paper stickers and they're annoying to remove. Use isopropyl alcohol, WD-40, or Goo-Gone to make it easier.

Too much heat will turn these black. Will start fading in a few years and will fade faster in direct sunlight or with frequent friction.

Have a good con!


""" + "<a href=\"" + GITHUB_LINK + "\">Github of this code</a>."

# ==== Super user responses ==== #
LOGS_CLEARED = "User limits have been reset"
USERS_WIPED = "All users wiped"
STICKER_HISTORY_CLEARED = "Sticker history cleared"
COUNTS_RESET = "All user counts reset"
SET_NEW_LIMIT = "New sticker limit set to {amount}"
GET_LIMIT = "Sticker limit is currently {amount}"
ADD_USER_LIMIT = "Added {amount} stickers to that user. They now have a limit of {total}"
SUBTRACT_USER_LIMIT = "Removed {amount} stickers from that user. " \
    "They now have a limit of {total}"
SET_USER_LIMIT = "That user now has a limit of {total}"
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
SLAP_ENABLED = "Slap detection enabled"
SLAP_DISABLED = "Slap detection disabled"
SLAP_ALREADY_ENABLED = "Slap detection is already enabled"
RANDOM_ENABLED = "Random sticker printing enabled"
RANDOM_DISABLED = "Random sticker printing disabled"
RANDOM_ALREADY_ENABLED = "Random sticker printing is already enabled"
RANDOM_ALREADY_DISABLED = "Random sticker printing is already disabled"
SLAP_ALREADY_DISABLED = "Slap detection is already disabled"
SLAP_HARDWARE_MISSING = "There is no accelerometer. Slap detection is disabled."
CANT_FIND_USER_ERROR = "Can't find the user for that sticker"
USER_BANNED = "That user has been banned. They have 0 sticker limit"
STICKER_REMOVED_FROM_HISTORY = "Sticker removed from history"
CANT_REMOVE = "That isn't something I can remove from the sticker history"
USER_LIMIT_RESET = "That user has had their stickers reset. They now have {amount} stickers."
PRINT_OFFSET = """
The current print offset in pixels:
Print offset x = {offset_x}
Print offset y = {offset_y}  

Change these by typing \"print offset x/y \" and a number.
x is horizontal, y is vertical offset"
Ex: print offset x 5
Ex: print offset y -15"""
SET_PRINT_OFFSET_X = "The x (horizontal) offset is now set to {offset_x}"
SET_PRINT_OFFSET_Y = "The y (vertical) offset is now set to {offset_y}"
SET_QUEUE_INSTRUCTIONS = f"Check connection or set the queue with \"{constants.LIST_QUEUES}\" " \
                            f"and \"{constants.SET_QUEUE}\""
CHECK_QUEUE_NO_QUEUE = "There is no printer queue set.\n\n" + SET_QUEUE_INSTRUCTIONS
CHECK_QUEUE_SUCCESS = "The print queue exists.\n\n" \
    "The current print queue is {print_queue}"
CHECK_QUEUE_FAIL = "The current print queue is not found in the system.\n\n" + SET_QUEUE_INSTRUCTIONS
LIST_QUEUES = "These are the current queues: "
LIST_QUEUES_NO_QUEUES = "There are currently no printer queues on this system. Connect a printer and try again."
SET_QUEUE_SUCCESS = "Print queue has been set"
SET_QUEUE_SYNTAX_ERROR = "Improper syntax. You must have the command, a space, and then the print queue name.\n" \
                         f"Ex: {constants.SET_QUEUE} Zebra_QL320plus"
SET_QUEUE_BAD_QUEUE = f"That print queue does not exist on this device. \n" \
                      f"Use \"{constants.LIST_QUEUES}\" to list the current print queues on this device"
BOT_ENABLE_ERROR_NO_QUEUE = "Bot enable failed. The print queue is not available.\n\n" + SET_QUEUE_INSTRUCTIONS
NO_FILE = "The user file is not found or no users have been recorded yet. Either way, it's a clean slate."
CANT_DELETE_FILE = "Unable to delete the user file."
CONFIG_SAVED = "Configuration has been saved."
#RANDOM_PRINTED_FOR = "Random printed for @{user_at}"
RANDOM_PRINTED_FOR = "Random printed for <a href=\"tg://user?id={user_id}\">{user_at}</a>"
SUPERUSER_NOT_SET = r"""
There is no superuser set.
Enter your Telegram user ID in the "super_user_id" field in BotConfig.ini

Your user ID is: {id}
"""
COMMAND_NOT_RECOGNIZED = f"Command not recognized. Type \"{constants.COMMANDS}\" for a list of commands"
COMMANDS = f"""
General commands:
\"{constants.RESET_ALL_COUNT}\" - Resets sticker count to 0
\"{constants.WIPE}\" - Wipes all users
\"{constants.CLEAR_HISTORY}\" - Clear sticker history for /random
\"{constants.SET_ALL_LIMIT} X\" - Sets sticker limit to X
\"{constants.GET_LIMIT}\" - Shows the current sticker limit
\"{constants.BOT_ENABLE}\" - Enables the bot
\"{constants.BOT_DISABLE}\" - Disables the bot
\"{constants.STICKER_MONITORING_ON}\"/\"{constants.STICKER_MONITORING_OFF}\" \
- Turn on/off monitoring (sends superusers all printed stickers)
\"{constants.EVENT_ON}\"/\"{constants.EVENT_OFF}\" \
- Turn on/off random events
\"{constants.SLAP_ON}\"/\"{constants.SLAP_OFF}\" - Turn slap detection on/off
\"{constants.RANDOM_ON}\"/\"{constants.RANDOM_OFF}\" - Turn random sticker printing on/off
\"{constants.SAVE}\" - Save current settings to config file

Printer commands:
\"{constants.PRINT_OFFSET}\" - Displays the current print offset and displays commands for adjusting
\"{constants.CHECK_QUEUE}\" - Displays the current queue and checks if it exists
\"{constants.LIST_QUEUES}\" - Lists the print queues on the device
\"{constants.SET_QUEUE}\" - Sets the print queue (Ex: {constants.SET_QUEUE} Zebra_QL230)

"Reply commands (Reply to a monitored sticker):
[+ or - or =][number] - Add, subtract, or set sticker limit (Ex: +5, -1, or =999)
\"{constants.BAN}\" - Bans the user. Sets their limit to 0
\"{constants.RESET}\" - Resets the user's used stickers to 0. Lets them print more
\"{constants.REMOVE}\" - Remove the sticker from /random feature"""


def get_confirm_message(emojis = "") -> str:
    """ Randomized confirmation message for after a sticker is successfully sent to the printer.
        Picks at random from the list and inserted at "_____! Sending to the printer!"

        :param emojis: Optional: One or more emojis associated with the sticker. May be used for a custom response.
        :return: Confirmation message as a string.
    """

    #70% chance of choosing the emoji option, so that it doesn't become predictable.
    if emojis != "" and random.random() < 0.7:
        if (message := get_emoji_confirm_message(emojis)) != "":
            return message + " Sending to the printer!"

    responses = [
        "Pog!",
        "As an AI language model that sticker is dope as fuck.",
        "👀👌💯",
        "😎👌 🤨🕶👌 ...okay.",
        "...really?",
        "Nice!",
        "Wow, great choice!",
        "That's a juicy sticker right there.",
        "Coming right up!",
        "This one will look great on your water bottle you bring to work.",
        "That sticker is only 18% cringe!",
        "Thank you for signing up for the furry surveillance program. We are now watching.",
        "Oh we’re printing this? Okay, choices were made.",
        "I’ve seen worse. Not often, but I have.",
        """͘            🤠
　   🖼🖼🖼
   🖼    🖼   🖼
  👇   🖼🖼  👇
       🖼　 🖼
     🖼　    🖼
　  👢        👢
Howdy! I'm the art sheriff and I say that's a good sticker.""",
    ]

    conclusion = random.choice([" Sending to the printer!", " Straight to the printer!"])
    return responses[random.randint(0, len(responses)) - 1] + conclusion


def get_emoji_confirm_message(emojis: str) -> str:
    """ Stickers in telegram are associated with one or more emojis.
    This gives a custom response based on the emoji of the sticker.

        :param emojis: One or more emojis associated with the sticker. May be used for a custom response.
    """

    for emoji in emojis:
        match emoji:
            case "📷": # used for photos
                return random.choice(["Art? Photo? Vibe? Doesn’t matter — it’s beautiful.",
                                    "Looks like culture to me.",
                                    "Ah yes, modern expressionism with a dash of 'what am I looking at? 🖼️\n",
                                    "This one belongs in a museum 🖼️.",
                                    "Truly something to hang on the fridge... or bury in a drawer.",
                                    "High art. Or cursed content. Depends on who you ask.",
                                    "Straight from your photo reel to a sticker.",
                                    "Capturing emotion, color, and some of the creator's unmedicated ADHD.",
                                    "I’ve seen worse. Not often, but I have 🖼️.",
                                    "Bold lines. Questionable choices. Iconic 🖼️\n",
                                    "Picasso is shaking. And crying. 🖼️\n",
                                    "Look at you, making \"content\" 🖼️\n",
                                    "This? Oh this is art... in the same way glitter in your cereal is art. Bold choice, darling.",
                                    "We got big vibes of abstract chaos, unexpected angles, emotional damage in crayon — I LIVE 🖼️\n",
                                    "It’s giving... budget surrealism with a dash of 'what am I looking at?' 🖼️. Werk."])
            case "❤️" | "🤗" | "🫂" | "🥰" | "😍" | "💘" | "💝" | "💖" | "💗" | "💓" | "💞" | "💟" | "❣️" | "😊":
                return "That's so cute ❤️."
            case "😘" | "😚" | "😗" | "😙" | "💋" | "😉":
                return "😘"
            case "🥚":
                return "👁️👄👁️ Egg."
            case "🪨" | "🗿":
                return "🗿\n\n"
            case "🐳" | "🐋":
                return "🐋\n\n"
            case "🔥" | "🌶️" | "🥵":
                return "😳 spicy."
            case "🍆" | "🍑" | "😳" | "⛓️" | "🔒" | "🔐" | "💄" | "🍈" | "🌭":
                return random.choice(["😳 spicy.",
                                      "Oh... we’re sending that kind of energy today? Noted 😳.",
                                      "This sticker is giving... unholy vibes. Good 😘.",
                                      "That’s not a vibe, that’s a lifestyle.",
                                      "Ma’am. Sir. Creature. I am an innocent python script. But I'll accept it 😏.",
                                      "Ma’am. Sir. Creature. The printer is blushing. But I'll make it print it anyway~."])
            case "👮" | "👮‍♂️" | "👮‍♀️" | "🚓" | "🚔":
                return "ACAB. Yes, this situation too."
            case "😭" | "😢":
                return "Crying? I'm crying. 😭"
            case "😎" | "🆒":
                return "Cool 😎."
            case "😬" | "😡" | "🤬" | "😠" | "👎":
                return "Chill, your sticker will be right out."
            case "😈":
                return "You up to no good again 😈."
            case "😇":
                return "Don't act so innocent."
            case "🤔" | "💭":
                return "What you thinkin' about? Nothing? Same 😐."
            case "😆" | "🤣" | "😂":
                return "Crying. Screaming. Throwing up (from laughter) 😂."
            case "😀" | "😃" | "😄" | "😁" | "😊" | "👍":
                return "Downloading those good vibes now 😁."
            case "🦵" | "🦿":
                return "How you do expect me to put that much leg energy onto one sticker. But I'll try."
            case "🧠" | "🤓":
                return ("I'm smart too. My teacher said to me I'm a failure, that I'll never amount to anything. "
                        "I scoffed at him. Shocked, my teacher asked what's so funny, my future is on the line. "
                        "\"Well...you see professor\" I say as the teacher prepares to laugh at my answer, "
                        "rebuttal at hand. \"I watch Rick and Morty.\" The class is shocked, they merely watch "
                        "pleb shows like the big bang theory to feign intelligence, not grasping the humor. \"...how? "
                        "I can't even understand it's sheer nuance and subtlety.\" \"Well you see...WUBBA "
                        "LUBBA DUB DUB!\" One line student laughs in the back, I turn to see a who this fellow "
                        "genius is. It's none other than Albert Einstein.\n\n...")
            case "🙃":
                return "Well this is fine. Everything’s fine 🙃."
            case "🔫":
                return "Threatening me won't get you more stickers 😐."
            case "😶‍🌫️":
                return "Brain? Gone. Thoughts? Vapor."
            case "🤑" | "💵" | "💶" | "💸" | "💲" | "💷" | "💰" | "💴":
                return "Makin' that dosh. That bread. That cheddar. That moolah. Those cold hard grease-flecked jingle biscuits."
            case "🍺" | "🍻" | "🥂" | "🍾" | "🥳" | "🎆" | "🎉" | "🎊":
                return "Cheers 🍻!"
            case "🕷️":
                return "️͘         👁️👁️👄👁️👁️ - spider\n🦵🦵🦵🦵   🦵🦵🦵🦵\n"
            case "🔮":
                return "I forsee... a print job 🔮."
            case "🧙" | "🧙‍♂️":
                return "Real wizard posting hours right now 🧙."
            case "🌈" | "🏳️‍🌈":
                return "Gaaaay. Just how I like it 🏳️‍🌈."
            case "🏳️‍⚧️":
                return "Trans rights 🏳️‍⚧️🏳️‍⚧️🏳️‍⚧️!!"
            case "🐦" | "🕊" | "🦜":
                return "That's a nice government drone there 🔭🕵️."
            case "🐊" | "🦎":
                return "Cold-blooded and unbothered 🐊🦎."
            case "🐍":
                return "Ssslitheringly sssensssational 🐍."
            case "😺" | "😸" | "🐱" | "🤠" | "🐅" | "🐯" | "🐈" | "🦁" | "😻":
                return "Meowdy partner 🐱."
            case "👋":
                return "Howdy 👋."
            case "🐶" | "🐕" | "🐕‍🦺":
                return "That's a good puppy 🐶."
            case "😪" | "😴" | "💤" | "🛌" | "🛏️":
                return "Time to WAKE UP ⏰ because you've got a sticker coming."
            case "🐄" | "🐮" | "🐂" | "🦬" | "🐃":
                return "This sticker is moooooving 🐮 right to ya."
            case "🐒" | "🐵" | "🦍" | "🦧":
                return "Monkey see, monkey print 🐒."
            case "🦦":
                return "Otterly adorable 🦦."
            case "🐴" | "🏇" | "🐎" | "🎠":
                return "Giddy-up, we’re galloping to the printer 🐴!"
            case "🐼":
                return "Too cute to function 🐼."
            case "🐢":
                return "Slow and steady, just like my motivation 🐢."
            case "🐔":
                return "IS THAT THE CHICKEN FROM CHICKEN JOCKY STEVE MINECRAFT 😲?!"  # TODO Remove this when it's a dead meme
            case "🐻":
                return "Soft, cuddly, and might maul you 🐻."
            case "🐀":
                return "Rat detected. Grabbing and shipping."
            case "🐁" | "🐭":
                return "Small, soft, but probably plotting 🐭."
            case "🦖" | "🦕":
                return "We stan the big and small dinos here 🦖."
            case "🐉" | "🐲":
                return "Big dragon energy 😏🔥."
            case "🙈":
                return "They might be hiding 🙈, but you should look out for this sticker."
            case "⌚" | "⏲️" | "⏰" | "⏱️" \
                 "🕐" | "🕑" | "🕒" | "🕓" | "🕔" | "🕕" | "🕖" | "🕗" | "🕘" | "🕙" | "🕚" | "🕛" | \
                 "🕜" | "🕝" | "🕞" | "🕟" | "🕠" | "🕡" | "🕢" | "🕣" | "🕤" | "🕥" | "🕦" | "🕧":
                return "You're right. It's TIME 🕐 for your sticker to be printed."
            case "🎩":
                return "What a fancy fella 🎩."
            case "🤡" | "🎪" | "🤹":
                return "Yeah, we do a little clownin' around here too 🤡."
            case "📈" | "📊" | "📉" | "💎":
                return "Stonks 📊."
            case "👅" | "😛" | "😜" | "😝":
                return "Mlem 😛"
            case "💦" | "💧":
                return "Don't drip too much. I don't have that water-proof sticker paper."
            case "🥺":
                return "You don't have to beg anymore."
            case "👀" | "👁️":
                return "I see you too 👀. Watch this."
            case "🧼" | "🫧":
                return "Time to wash up, stinky."
            case "📦" | "🎁":
                return "Packaging up that sticker."
            case "🐝":
                return ("According to all known laws of aviation, there is no way a bee should be able to fly."
                        "Its wings are too small to get its fat little body off the ground."
                        "The bee, of course, flies anyway because bees don't care what humans think is impossible."
                        "Yellow, black. Yellow, black. Yellow, black. Yellow, black."
                        "Ooh, black and yellow!"
                        "Let's shake it up a little...")
            case "❓" | "⁉️":
                return "Wonder no more. I'm sending it to the printer."

    return ""