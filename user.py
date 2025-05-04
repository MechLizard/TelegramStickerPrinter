import responses


class User:
    def __init__(self, update, users_cf):
        self.username = update.message.chat.username
        self.user_id = update.message.from_user.id
        self.sticker_max = users_cf['sticker_limit']
        self.sticker_count = 0
        self.quiz_encounter = False
        self.bonus_sticker_encounter = False
        self.end_message_encounter = False
        self.message_id_history = []
        self.sticker_history = set()
        self.accepted_random_warning = False
        self.opt_out_sticker_history = False

    def __eq__(self, other):
        if self.user_id == other.user_id:
            return True
        return False

    def get_limit_response(self):
        if self.sticker_count >= self.sticker_max:
            if not self.end_message_encounter:
                self.end_message_encounter = True
                return responses.END_MESSAGE
            else:
                return responses.OUT_OF_STICKERS
        else:
            return responses.STICKER_COUNT.format(count=str(self.sticker_max - self.sticker_count))

    def log_message(self, message_id):
        self.message_id_history.append(message_id)

    # Check this user has the given message ID In their sticker history
    # This is for if the user has their chat hidden for forwarded messages
    # This is the message ID in the superuser's chat that is forwarded by the sticker monitor
    def check_log(self, message_id):
        for i in self.message_id_history:
            if message_id == i:
                return True
        return False
