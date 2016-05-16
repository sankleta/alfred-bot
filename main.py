import ConfigParser
import time

import schedule
from slackclient import SlackClient

from bot import Bot
from members import Members
from reminder import Reminder
from trello_client import TrelloClient

config = ConfigParser.ConfigParser()
config.read('config.ini')

slack_token = config.get("Slack", "slack_token")
trello_key = config.get("Trello", "trello_key")
trello_token = config.get("Trello", "trello_token")
list_id = config.get("Trello", "my_list_id")

members = Members('members.json')
slack = SlackClient(slack_token)
trello = TrelloClient(trello_key, trello_token, list_id)

reminder = Reminder(slack, members)
schedule.every().hour.do(reminder.remind)

if slack.rtm_connect():
    bot = Bot(slack, trello, members)

    while True:
        bot.read_messages()
        schedule.run_pending()
        time.sleep(1)
else:
    print 'Connection Failed, invalid token?'
