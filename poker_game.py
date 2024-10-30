# import random


deck_of_cards_notfull = ["As", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
colors = ["heart", "spade", "club", "diamond"]
deck_of_cards = []
for color in colors:
    for card in deck_of_cards_notfull:
        deck_of_cards.append(card + " of " + color)
print(deck_of_cards)
class Player:
    def __init__(self, name):
        self.name = name

num_player = 0

def game_type():
    game_type = input("wich variant of texas holdem would you like to play ? You can enter NL2, NL5, NL10, NL20 or NL50")
    return game_type

def add_player():
    list_players = []
    player = ""
    while player != "ok":
        player = input("enter player\'s name to add a new player or \'ok\' to continue")
        if player != "ok":
            list_players.append(player)
    return list_players

def lauch_game():
    game_type = game_type()
    list_players = add_player()
    # while party continue:
        # new_turn()

def new_turn(list_players, game_type):
    distribution = {}
    for player in list_players:
        distribution[player] = random.choice(deck_of_cards, k=2)


# print(random.choice(1, 2, 3))




