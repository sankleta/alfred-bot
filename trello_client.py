from trello import TrelloApi


class TrelloClient:
    def __init__(self, key, token, list_id):
        self.trello_client = TrelloApi(apikey=key, token=token)
        self.list_id = list_id

    def add_card(self, user_id, text):
        card = self.trello_client.lists.new_card(self.list_id, text)
        self.trello_client.cards.new_member(card['id'], user_id)
