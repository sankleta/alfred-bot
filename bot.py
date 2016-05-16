from message import Message


class Bot:
    private_response = "I'm adding a card with the title '%s' into list Develop DO and add you as a member."
    public_response = "Please write me a direct message to add a task on the Trello board."
    no_access_response = "Sorry, I'm not allowed to help you. Please write to @tanya to get the access."
    first_response = "Hello! I'm Albert. I'm here to help you with time tracking. I will post each message" \
                     + "you write me as a card to Trello and remind you to keep tracking."

    def __init__(self, slack_client, trello_client, members):
        self.slack_client = slack_client
        self.trello_client = trello_client
        self.members = members
        self.id = slack_client.server.login_data['self']['id']
        self.name = '<@' + self.id + '>'

    def read_messages(self):
        for entry in self.slack_client.rtm_read():
            self.read_message(Message(entry))

    def read_message(self, message):
        if not message.is_message():
            return

        # TODO: Add 'in' method to Members
        if message.is_private() and message.user() != self.id and message.user() in self.members.members:
            self.handle_private(message)
        elif message.is_private() and message.user() != self.id and message.user() not in self.members.members:
            self.send_message(message.channel(), self.no_access_response)
        elif message.is_public() and self.name in message.text():
            self.handle_public(message)

    def handle_private(self, message):
        if not self.members.has_channel(message.user(), message.channel()):
            self.members.save_channel(message.user(), message.channel())
            self.send_message(message.channel(), self.first_response)
            return

        self.send_message(message.channel(), self.private_response % message.text())
        # TODO: Ask if proceed
        # TODO: Add index method to Members
        self.trello_client.add_card(self.members.members[message.user()].trello_id, message.text())

    def handle_public(self, message):
        self.send_message(message.channel(), self.public_response)

    def send_message(self, channel, message):
        self.slack_client.rtm_send_message(channel, message)
