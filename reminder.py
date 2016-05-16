class Reminder:
    message = "Hi %s. I'm your friendly neighbourhood bot. Did you do anything which should be listed on "\
              + "Trello? Please tell me or Joep will terminate you. Have a nice day!"

    def __init__(self, slack_client, members):
        self.slack_client = slack_client
        self.members = members

    def remind(self):
        # TODO: Added iterate method to Members
        for member in self.members.members.values():
            if member.needs_reminder():
                self.slack_client.rtm_send_message(member.channel, self.message % member.name)
