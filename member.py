from datetime import datetime


class Member:
    name_key = 'name'
    trello_id_key = 'trello_id'
    slack_id_key = 'slack_id'
    channel_key = 'channel'

    def __init__(self, entry):
        self.name = self.read_value(self.name_key, entry)
        self.trello_id = self.read_value(self.trello_id_key, entry)
        self.slack_id = self.read_value(self.slack_id_key, entry)
        self.channel = self.read_value(self.channel_key, entry)

    def needs_reminder(self):
        time_now = datetime.utcnow()
        if len(self.channel) < 1:
            return False
        if time_now.weekday() in range(0, 5) and time_now.hour in range(8, 16):
            return True
        else:
            return False

    def to_entry(self):
        return {self.name_key: self.name,
                self.trello_id_key: self.trello_id,
                self.slack_id_key: self.slack_id,
                self.channel_key: self.channel}

    @staticmethod
    def read_value(key, entry):
        return entry[key] if key in entry else ''
