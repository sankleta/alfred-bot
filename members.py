from member import Member
import json


class Members:
    members = {}

    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path) as json_file:
            members_data = json.load(json_file)

        for member_data in members_data:
            member = Member(member_data)
            self.members[member.slack_id] = member

    def save_channel(self, slack_id, channel):
        if slack_id not in self.members or channel == self.members[slack_id].channel:
            return

        self.members[slack_id].channel = channel
        self.save_all()

    def save_all(self):
        with open(self.file_path, 'w') as json_file:
            json.dump([member.to_entry() for member in self.members.values()], json_file, indent=4, sort_keys=True)
