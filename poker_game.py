import random

deck_of_cards_notfull = ["As", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
colors = ["heart", "spade", "club", "diamond"]
deck_of_cards = []
for color in colors:
    for card in deck_of_cards_notfull:
        deck_of_cards.append(card + " of " + color)
dico_positions = {1: "LowJack", 2: "Hijack", 3: "Cut-Off", 4: "Button", 5: "Small Blind", 6: "Big Blind"}


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
    while (player != "ok") and (len(list_players) <= 6) and (len(list_players) >= 2):
        player = input("enter player\'s name to add a new player or \'ok\' to continue")
        if player != "ok":
            list_players.append(player)
    return list_players

def initialize_players_position(list_players):
    players_position = {}
    count = 1
    for player in list_players:
        players_position[count] = player
        count += 1
    return players_position

def initialize_players_information(list_players):
    players_position = {player:pos for player, pos in zip(list_players, random.sample(range(len(list_players))))} 
    return players_position

def change_players_position(suivi_pos):
    for key in suivi_pos.keys():
        if suivi_pos[key] != len(suivi_pos):
            suivi_pos[key] += 1
        elif suivi_pos[key] == len(suivi_pos):
            suivi_pos[key] = 1
    return suivi_pos


def lauch_game():
    game_type = game_type()
    list_players = add_player()
    LJ_position = random.choice(list_players)
        # while party continue:
        # new_turn()

def new_turn(list_players, game_type):
    distribution = {}
    for player in list_players:
        distribution[player] = random.choices(deck_of_cards, k=2)
    
    


print(len({"a":2, 2:8, "err": "efff"}))




