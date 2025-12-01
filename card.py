import json

class Card:
    card_id = 0
    card_name = ""
    wins = 0
    avg_trophies = 0
    cost = 0
    tags = ""

    def __init__(self, row):
        self.card_id = row[0]
        self.card_name = row[1]
        self.wins = row[2]
        self.avg_trophies = row[3]
        self.cost = row[4]
        self.tags = row[5]