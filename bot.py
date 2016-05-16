from message import Message


class Bot:
    private_response = "I'm going to add a card with the title '%s' into list Develop DO and add you as a member"
    public_response = "Please write me a direct message to add a task on the Trello board"

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
        elif message.is_public() and self.name in message.text():
            self.handle_public(message)

    def handle_private(self, message):
        self.members.save_channel(message.user(), message.channel())
        self.send_message(message.channel(), self.private_response % message.text())
        # TODO: Ask if proceed
        # TODO: Add index method to Members
        self.trello_client.add_card(self.members.members[message.user()].trello_id, message.text())

    def handle_public(self, message):
        self.send_message(message.channel(), self.public_response)

    def send_message(self, channel, message):
        self.slack_client.rtm_send_message(channel, message)
