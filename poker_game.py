# importation library
import random

# Definition basic ressources
deck_of_cards_notfull = ["As", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
colors = ["heart", "spade", "club", "diamond"]
deck_of_cards = []
for color in colors:
    for card in deck_of_cards_notfull:
        deck_of_cards.append(card + " of " + color)

positions_need = {1: "Button", 2: "Small Blind", 3: "Big Blind",  4: "Cut-Off", 5: "Hijack", 6: "Under The Gun"}
speak_order_postflop = {1: "Small Blind", 2: "Big Blind", 3: "Under The Gun", 4: "Hijack", 5: "Cut-Off", 6: "Button"}
speak_order_preflop = {1: "Under The Gun", 2: "Hijack", 3: "Cut-Off", 4: "Button", 5: "Small Blind", 6: "Big Blind"}

list_stack = {"NL2": 200, "NL5": 500, "NL10": 1000, "NL20": 20000, "NL50": 5000}

# Definition function for the game
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

def get_number_in_range(min_val, max_val):
    while True:
        try:
            number = int(input(f"The raise must be between {min_val} and {max_val}!"))
            if min_val <= number <= max_val:
                return number
            else:
                print(f"The raise must be between {min_val} and {max_val}!")
        except ValueError:
            print("Please enter a valid integer!")

def initialize_players_information(list_players):
    players_informations = {player:[starting_stack, pos] for player, starting_stack, pos in zip(list_players, list_stack, random.sample(1, range(len(list_players) + 1)))} 
    return players_informations

def change_players_position(players_informations):
    for key in players_informations.keys():
        if players_informations[key][1] != len(players_informations):
            players_informations[key][1] += 1
        elif players_informations[key][1] == len(players_informations):
            players_informations[key][1] = 1
    return players_informations


def lauch_game():
    game_type = game_type()
    list_players = add_player()
        # while party continue:
        # new_turn()

def new_turn(players_informations, game_type, deck_of_cards_fictive=deck_of_cards.copy()):
    players_inf_turn = {}
    pot = 1.5/100 * list_stack[game_type]
    for player in players_informations.keys():
        tirage = random.choices(deck_of_cards_fictive, k=2)
        deck_of_cards_fictive.remove(tirage[0], tirage[1])
        players_inf_turn[positions_need[players_informations[player][1]]] = [player, players_informations[player][0], True, tirage, 0] # {position_jeu : [Name_player, starting_stack, active/out, tirage, amount_invest]}
    
    if len(players_informations) < 3:
        players_inf_turn["Button"][-1] = players_inf_turn["Button"][-1] - 1/100 * list_stack
        players_inf_turn["Small Blind"][-1] = players_inf_turn["Small Blind"][-1] - 0.5/100 * list_stack
    else:
        players_inf_turn["Big Blind"][-1] = players_inf_turn["Big Blind"][-1] - 1/100 * list_stack
        players_inf_turn["Small Blind"][-1] = players_inf_turn["Small Blind"][-1] - 0.5/100 * list_stack
    
    new_street(players_inf_turn, deck_of_cards_fictive, pot)
    
def new_street_preflop(players_inf_turn_fictive, deck_of_card_fictive, pot):
    biggest_bet = pot
    for position in players_inf_turn_fictive:
        if (players_inf_turn_fictive[position][2]) and (players_inf_turn_fictive[position][4]) < biggest_bet:
            temporary_decision = input("call, raise or fold")
            if temporary_decision == "call":
                players_inf_turn_fictive[position][3] = biggest_bet
            elif temporary_decision == "raise":
                biggest_bet = get_number_in_range(2*biggest_bet, players_inf_turn_fictive[position][2])

            players_inf_turn_fictive[position].append(input("call or raise"), 0)
    return
    
def new_street(players_inf_turn_fictive, deck_of_card_fictive, pot_fictive):
    biggest_bet = pot_fictive
    count_eliminated_player = 0
    action = True
    while (count_eliminated_player != len(players_inf_turn_fictive)) - 1 and (action == True):
        action = False
        for position in players_inf_turn_fictive:
            players_inf_turn_fictive[position].append(0)                                                            # add a element in the list : amount invest on the street !
            if (players_inf_turn_fictive[position][2]) and (players_inf_turn_fictive[position][5]) == biggest_bet:
                temporary_decision = input("check or raise")
                if temporary_decision == "check":
                    action = False
                elif temporary_decision == "raise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn_fictive[position][1])
                    players_inf_turn_fictive[position][5] = biggest_bet
                    pot_fictive += biggest_bet
            if (players_inf_turn_fictive[position][2]) and (players_inf_turn_fictive[position][5]) < biggest_bet:
                temporary_decision = input("fold, call or reraise")
                if temporary_decision == "fold":
                    count_eliminated_player += 1
                    players_inf_turn_fictive[position][2] = False
                elif temporary_decision == "call":
                    action = False
                    players_inf_turn_fictive[position][5] = biggest_bet
                    pot_fictive += biggest_bet
                elif temporary_decision == "reraise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn_fictive[position][1])
                    players_inf_turn_fictive[position][5] = biggest_bet
                    pot_fictive += biggest_bet

        
    

print(len({"a":2, 2:8, "err": "efff"}))




