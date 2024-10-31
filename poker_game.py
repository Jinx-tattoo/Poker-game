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
dico_street = {0: "preflop", 1: "flop", 2: "turn", 3: "river"}

list_stack = {"NL2": 200, "NL5": 500, "NL10": 1000, "NL20": 20000, "NL50": 5000}

order_jeu = {0: "high", 1: "pair", 2: "double pair", 3: "tripp", 4: "suit", 5: "flush", 6: "square", 7: "quinte flush"}

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

def activate_player(players_inf_turn):
    for positon in players_inf_turn:
        if players_inf_turn[positon][1] > 0:
            players_inf_turn[positon][2] = True
    return

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

def new_tirage(street, deck):
    if street == "flop":
        new_tirage = random.choices(deck, k=3)
        deck.remove(new_tirage[0], new_tirage[1], new_tirage[2])
        print(f"flop : {new_tirage[0]}  {new_tirage[1]}  {new_tirage[2]}")
        return new_tirage
    elif street == "turn":
        new_tirage = random.choices(deck, k=1)
        deck.remove(new_tirage[0])
        print(f"turn : {new_tirage[0]}")
        return new_tirage
    elif street == "river":
        new_tirage = random.choices(deck, k=1)
        deck.remove(new_tirage[0])
        print(f"river : {new_tirage[0]}")
        return new_tirage

def update_amount_invest(players_inf_turn):
    for position in players_inf_turn:
        players_inf_turn[position][4] += players_inf_turn[position][5]
        players_inf_turn[position][5] = 0
    return players_inf_turn
    
def state_hand(players_inf_turn, street="preflop"):
    count = 0
    count_all_in = 0
    for position in players_inf_turn:
        if players_inf_turn[position][2] == True:
            count += 1
        if round(players_inf_turn[position][1] - players_inf_turn[position][2]) == 0:
            count_all_in += 1 
    if count - count_all_in == 1:
        street = "river"
        state = True
        order_show_card = True
        return street, state, order_show_card
    if count > 1 and street == "preflop":
        street = "flop"
        state = True
        order_show_card = False
        return street, state, order_show_card
    elif count > 1 and street == "flop":
        street = "turn"
        state = True
        order_show_card = False
        return street, state, order_show_card
    elif count > 1 and street == "turn":
        street = "river"
        state = True
        order_show_card = False
        return street, state, order_show_card
    elif count <= 1 or street == "river":
        street = "turn"
        state = False
        order_show_card = True
        return street, state, order_show_card

def update_stack(players_inf_turn, pot):
    for positon in players_inf_turn:
        if players_inf_turn[positon][2] == True:
            players_inf_turn[positon][1] += pot - players_inf_turn[positon][4]
            players_inf_turn[positon][4] = 0
            players_inf_turn[positon][5] = 0
        elif players_inf_turn[positon][2] == False:
            players_inf_turn[positon][1] -= players_inf_turn[positon][4]
            players_inf_turn[positon][4] = 0
            players_inf_turn[positon][5] = 0
    return

def show_down(deck_of_cards_fictive, displayed_card):
    while len(displayed_card) < 3:
        street_pos = dico_street[len(displayed_card) + 1]
        displayed_card.append(new_tirage(street_pos, deck_of_cards_fictive))
    return displayed_card

def determine_best_game(players_inf_turn, displayed_card):
    player_win = ""
    jeux_players = {}
    for position in players_inf_turn:
        if players_inf_turn[position][2] == True:
            composition = players_inf_turn[3] + displayed_card[0] + [displayed_card[1]] + [displayed_card[2]]
            jeu = determine_jeu(composition)
            jeux_players[players_inf_turn[position][0]] = jeu
    
   
    return

def separate_figure_color(composition):
    return

def determine_jeu(composition):
    # quinte flush
    count_color
    return

def preflop(players_inf_turn_fictive, deck_of_card_fictive, pot):
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
    
def new_street(players_inf_turn_fictive, pot_fictive):
    biggest_bet = pot_fictive
    count_eliminated_player = 0
    action = True
    while (count_eliminated_player != len(players_inf_turn_fictive) - 1) and (action == True):
        action = False
        for position in players_inf_turn_fictive:
            if (players_inf_turn_fictive[position][2]) and (players_inf_turn_fictive[position][5] == biggest_bet) and (players_inf_turn_fictive[position][1] > players_inf_turn_fictive[position][4]):
                temporary_decision = input("check or raise")
                if temporary_decision == "check":
                    action = False
                elif temporary_decision == "raise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn_fictive[position][1])
                    players_inf_turn_fictive[position][5] = biggest_bet
                    pot_fictive += biggest_bet
            if (players_inf_turn_fictive[position][2]) and (players_inf_turn_fictive[position][5] < biggest_bet) and (players_inf_turn_fictive[position][1] > players_inf_turn_fictive[position][4]):
                temporary_decision = input("fold, call or reraise")
                if temporary_decision == "fold":
                    count_eliminated_player += 1
                    players_inf_turn_fictive[position][2] = False
                elif temporary_decision == "call":
                    action = False
                    if (players_inf_turn_fictive[position][1] - players_inf_turn_fictive[position][4] + players_inf_turn_fictive[position][5]) <= biggest_bet:
                        players_inf_turn_fictive[position][5] = players_inf_turn_fictive[position][1] - players_inf_turn_fictive[position][4] 
                        pot_fictive += players_inf_turn_fictive[position][1] - players_inf_turn_fictive[position][4] 
                    else:
                        players_inf_turn_fictive[position][5] = biggest_bet
                elif temporary_decision == "reraise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn_fictive[position][1])
                    players_inf_turn_fictive[position][5] = biggest_bet
                    pot_fictive += biggest_bet
    return pot_fictive
        
def new_hand(players_informations, game_type, deck_of_cards_fictive=deck_of_cards.copy()):
    players_inf_turn = {}
    pot = 1.5/100 * list_stack[game_type]
    for player in players_informations.keys():
        tirage = random.choices(deck_of_cards_fictive, k=2)
        deck_of_cards_fictive.remove(tirage[0], tirage[1])
        players_inf_turn[positions_need[players_informations[player][1]]] = [player, players_informations[player][0], True, tirage, 0, 0] # {position_jeu : [Name_player, starting_stack, active/out, tirage, amount_invest]}
    
    if len(players_informations) < 3:
        players_inf_turn["Button"][-1] = players_inf_turn["Button"][-1] - 1/100 * list_stack
        players_inf_turn["Small Blind"][-1] = players_inf_turn["Small Blind"][-1] - 0.5/100 * list_stack
    else:
        players_inf_turn["Big Blind"][-1] = players_inf_turn["Big Blind"][-1] - 1/100 * list_stack
        players_inf_turn["Small Blind"][-1] = players_inf_turn["Small Blind"][-1] - 0.5/100 * list_stack
    
    pot += preflop()
    update_amount_invest(players_inf_turn)
    street, state, order_show_card = state_hand(players_inf_turn)
    displayed_card = []
    if order_show_card == True:
        displayed_card = show_down(players_inf_turn, deck_of_cards_fictive, street, displayed_card)
        determine_best_game(players_inf_turn, displayed_card)
    
    while state == True:        
        displayed_card.append(new_tirage(street, deck_of_cards_fictive))
        pot += new_street(players_inf_turn, deck_of_cards_fictive, pot)
        update_amount_invest(players_inf_turn)
        street, state, order_show_card = state_hand(players_inf_turn)
        if order_show_card == True:
            displayed_card = show_down(players_inf_turn, deck_of_cards_fictive, street, displayed_card)
            determine_best_game(players_inf_turn, displayed_card)
    
        update_stack(players_inf_turn, pot)




def lauch_game():
    game_type = game_type()
    list_players = add_player()
    
        # while party continue:
        # new_turn()



