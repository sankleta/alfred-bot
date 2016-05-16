class Message:
    message_type = 'message'
    type_key = 'type'
    channel_key = 'channel'
    text_key = 'text'
    user_key = 'user'

    def __init__(self, entry):
        self.entry = entry

    def is_message(self):
        return self.type_key in self.entry and self.entry[self.type_key] == self.message_type

    def channel(self):
        return self.entry[self.channel_key] if self.channel_key in self.entry else ''

    def text(self):
        return self.entry[self.text_key] if self.text_key in self.entry else ''

    def user(self):
        return self.entry[self.user_key] if self.user_key in self.entry else ''

    def is_private(self):
        return self.channel().startswith('D')

    def is_public(self):
        return self.channel().startswith('C')
