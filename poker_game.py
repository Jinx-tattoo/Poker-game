# importation library
import random

# Definition basic ressources
class Card:
    valeur_card_invert = {0:"Two", 1:"Three", 2: "Four", 3: "Five", 4: "Six", 5: "Seven", 6: "Eight", 7: "Nine", 8: "Ten", 9: "Jack", 10: "Queen", 11: "King", 12:"As"}
    valeur_card = {"Two": 0, "Three": 1, "Four": 2, "Five": 3, "Six": 4, "Seven": 5, "Eight": 6, "Nine": 7, "Ten": 8, "Jack": 9, "Queen": 10, "King": 11, "As": 12}
    colors = ["heart", "spade", "club", "diamond"]
    def __init__(self, figure, color):
        self.figure = figure
        self.valeur = Card.valeur_card[self.figure]
        self.color = color
        self.name = self.figure + " of " + self.color
    def __repr__(self):
        pass    

positions_need = {1: "Big Blind", 2: "Small Blind", 3: "Button",  4: "Cut-Off", 5: "Hijack", 6: "Under The Gun"}
speak_order_postflop = {2: ["Small Blind", "Big Blind"], 3: ["Small Blind", "Big Blind", "Button"], 4: ["Small Blind", "Big Blind", "Cut-Off","Button"], 5: ["Small Blind", "Big Blind", "Hijack", "Cut-Off","Button"], 6: ["Small Blind", "Big Blind", "Under The Gun", "Hijack", "Cut-Off","Button"]}
speak_order_preflop= ["Under The Gun", "Hijack", "Cut-Off", "Button", "Small Blind", "Big Blind"]
dico_street = {0: "preflop", 1: "flop", 2: "turn", 3: "river"}
list_stack = {"NL2": 200, "NL5": 500, "NL10": 1000, "NL20": 2000, "NL50": 5000}
order_jeu = {0: "high card", 1: "pair", 2: "double pair", 3: "tripps", 4: "quint", 5: "flush", 6: "full", 7: "square", 8: "quinte flush"}
order_jeu_invert = {"high card": 0, "pair": 1, "double pair": 2, "tripps": 3, "quint": 4, "flush": 5, "full": 6, "square": 7, "quinte flush": 8}

# Definition function for the game

def deck_creation():
    deck_card_class = []
    for i in range(13):
        for j in range(4):
            deck_card_class.append(Card(Card.valeur_card_invert[i], Card.colors[j]))
    return deck_card_class

def function_game_type():
    game_type = str(input("wich variant of texas holdem would you like to play ? You can enter NL2, NL5, NL10, NL20 or NL50 : "))
    return game_type

def add_player():
    list_players = []
    player = ""
    while (player != "ok") and (len(list_players) <= 6):
        player = input("enter player\'s name to add a new player or \'ok\' to continue : ")
        if player != "ok":
            list_players.append(player)
        elif (player == "ok") and (len(list_players) < 2):
            print("There is not enough player !")
            player = ""
    return list_players

def activate_player(players_informations, game_type):
    player_out = []
    for player in players_informations:
        motivation = input(f"\n{player}, if you want to play enter \"yes\". Otherwise enter \"no\" : ")
        if motivation == "no":
            decision = input(f"\n{player}, if you want to leave the table enter \"leave\". Otherwise enter \"stay\" : ")
            if decision == "leave":
                player_out.append(player)
            else:
                players_informations[player][2] = False
        elif (motivation == "yes") and (players_informations[player][0] == 0):
            restack = resatck(10/100 * list_stack[game_type], list_stack[game_type])
            players_informations[player][3] += restack
            players_informations[player][0] = restack
        elif (players_informations[player][0] > 0) and (motivation == "yes"): 
            players_informations[player][2] = True
    return players_informations, player_out

def resatck(min_val, max_val):
    while True:
        try:
            number = int(input(f"How much do you want to add. The amount must be between {min_val} and {max_val}!"))
            if min_val <= number <= max_val:
                return number
            else:
                print(f"The amount must be between {min_val} and {max_val}!")
        except ValueError:
            print("Please enter a valid integer!")

def get_number_in_range(min_val, max_val):
    while True:
        try:
            number = int(input(f"The raise must be between {min_val}$ and {max_val}$! : "))
            if min_val <= number <= max_val:
                return number
            else:
                print(f"The raise must be between {min_val}$ and {max_val}$! : ")
        except ValueError:
            print("Please enter a valid integer!")

def initialize_players_information(list_players, game_type):
    players_informations = {player:[list_stack[game_type], pos, True, list_stack[game_type]] for player, pos in zip(list_players, random.sample(range(1, len(list_players) + 1), k=len(list_players)))} # {player : stack, position, state, gain}
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
        new_tirage = random.sample(deck, k=3)
        deck.remove(new_tirage[0])
        deck.remove(new_tirage[1])
        deck.remove(new_tirage[2])
        print(f"flop : {new_tirage[0].name}  {new_tirage[1].name}  {new_tirage[2].name}\n")
        return new_tirage
    elif street == "turn":
        new_tirage = random.sample(deck, k=1)
        deck.remove(new_tirage[0])
        print(f"turn : {new_tirage[0].name}")
        return new_tirage
    elif street == "river":
        new_tirage = random.sample(deck, k=1)
        deck.remove(new_tirage[0])
        print(f"river : {new_tirage[0].name}")
        return new_tirage

def update_amount_invest(players_inf_turn):
    for player in players_inf_turn:
        players_inf_turn[player][4] += players_inf_turn[player][5]
        players_inf_turn[player][5] = 0
    return players_inf_turn
    
def state_hand(players_inf_turn, street="preflop"):
    count = 0
    count_all_in = 0
    for player in players_inf_turn:
        if players_inf_turn[player][2] == True:
            count += 1
        if round(players_inf_turn[player][1] - players_inf_turn[player][2]) == 0:
            count_all_in += 1 
    if count - count_all_in == 1:
        street = "river"
        state = False
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
        street = "river"
        state = False
        order_show_card = True
        return street, state, order_show_card

def update_stack(players_inf_turn, pot):
    for player in players_inf_turn:
        if players_inf_turn[player][2] == True:
            players_inf_turn[player][1] += pot - players_inf_turn[player][4]
            print(f"{player} win {pot - players_inf_turn[player][4]}$ ! Stack updated : {players_inf_turn[player][1]}$.")
            players_inf_turn[player][4] = 0
            players_inf_turn[player][5] = 0
        elif players_inf_turn[player][2] == False:
            players_inf_turn[player][1] -= players_inf_turn[player][4]
            print(f"{player} lose {players_inf_turn[player][4]}$. Stack updated : {players_inf_turn[player][1]}$.")
            players_inf_turn[player][4] = 0
            players_inf_turn[player][5] = 0    
    print("\n-----------------------------------------------------------------------------------------------------\n")  
    return

def find_higher_card_pair_tripps_square_except(composition, card):
    compo = ordering(composition)[1]
    for i in range(len(compo)):
        if compo[i].figure != card.figure:
            return compo[i]
    return compo[0]
    

# def ordering(composition):
#     composition_ordered_v = []
#     composition_ordered_v_dico = {}
#     composition_ordered = composition.copy()
#     for card in composition:
#         composition_ordered_v.append(card.valeur)
#         composition_ordered_v_dico[card.valeur] = card
#     composition_ordered_v.sort()
#     for index, i in zip(composition_ordered_v, range(len(composition_ordered_v))):
#         composition_ordered[i] = composition_ordered_v_dico[index]
#     composition_ordered_declining = list(reversed(composition_ordered))
#     return composition_ordered, composition_ordered_declining

def ordering(composition):
    # Input validation
    if not composition:
        return [], []
    
    # Create copy to avoid modifying original
    composition_ordered = composition.copy()
    
    # Sort directly using value attribute
    composition_ordered.sort(key=lambda card: card.valeur)
    
    # Create reversed version
    composition_ordered_declining = composition_ordered[::-1]
    
    return composition_ordered, composition_ordered_declining

def flush(composition):
    compo = []
    for card in composition:
        list_color = []
        list_color.append(card.color)
    for color in Card.colors:
        count = list_color.count(color)
        if count > 4:              
            for card in ordering(composition)[1]:
                if card.color == color:
                    compo.append(card)
            return True, compo
    return False, composition
    
def quint(composition):
    compo = ordering(composition)[0]
    for i in range(2, -1, -1):
        count = 0
        for j in compo[i:i+4]:
            if Card.valeur_card[compo[i+1].figure] - Card.valeur_card[compo[i].figure] == 1:           
                count += 1
            else:
                break
        if count == 5:
            return True, compo[i:i+5]
    return False, composition
    

def square(composition):
    compo = ordering(composition)[1]
    compo_2 = [card.figure for card in compo]
    jeu = []
    for card in composition:
        if compo_2.count(card.figure) == 4:
            jeu.append(card)
            if len(jeu) == 3:
                for i in range(2):
                    high_card = find_higher_card_pair_tripps_square_except(compo, card)
                    jeu.append(high_card)
                    compo.remove(high_card)
                return True, jeu
    return False, composition

def tripps(composition):
    compo = ordering(composition)[1]
    compo_2 = [card.figure for card in compo]
    jeu = []
    for card in compo:
        if compo_2.count(card.figure) == 3:
            jeu.append(card)
            if len(jeu) == 3:
                for i in range(2):
                    high_card = find_higher_card_pair_tripps_square_except(compo, card)
                    jeu.append(high_card)
                    compo.remove(high_card)
                return True, jeu
    return False, composition

def double_pair(composition):
    compo = ordering(composition)[1]
    compo_2 = [card.figure for card in compo]
    jeu = []
    for card in compo:
        if compo_2.count(card.figure) == 2:
            jeu.append(card)
            if len(jeu) == 4:
                high_card = find_higher_card_pair_tripps_square_except(composition, card)
                jeu.append(high_card)
                return True, jeu        
    return False, composition
        
def pair(composition):
    compo = ordering(composition)[1]
    compo_2 = [card.figure for card in compo]
    jeu = []
    for card in compo:
        if compo_2.count(card.figure) == 2:
            jeu.append(card)
            if len(jeu) == 2:
                for i in range(3):
                    high_card = find_higher_card_pair_tripps_square_except(compo, card)
                    jeu.append(high_card)
                    compo.remove(high_card)
                return True, jeu
    return False, composition      

def full(composition):
    variable_tripps, tripps_compo = tripps(composition)
    variable_pair, pair_compo = pair(composition)
    if (variable_tripps == True) and (variable_pair == True):
        compo_full = tripps_compo[:3] + pair_compo[:2]
        return True, compo_full
    return False, composition

def quinte_flush(composition):
    variable_quint, quint_compo = quint(composition)
    variable_flush, flush_compo = flush(composition)
    if (variable_quint == True) and (variable_flush == True) and (flush_compo == quint_compo.reverse):
        return True, flush_compo
    return False, composition

def high_card(composition):
        jeu = ordering(composition)[1]
        return True, jeu

def determine_jeu(composition):
    print("\n-----------------------------------------------------------------------------------------------------------------\n")
    print("Composition of card :\n")
    for ele in ordering(composition)[1]:
        print(ele.name)
    if quinte_flush(composition)[0] == True:
        return "quinte flush", quinte_flush(composition)[1]
    elif square(composition)[0] == True:
        return "square", square(composition)[1]
    elif full(composition)[0] == True:
        return "full", full(composition)[1]
    elif flush(composition)[0] == True:
        return "flush", flush(composition)[1]
    elif quint(composition)[0] == True:
        return "quint", quint(composition)[1]
    elif tripps(composition)[0] == True:
        return "tripps", tripps(composition)[1]
    elif double_pair(composition)[0] == True:
        return "double pair", double_pair(composition)[1]
    elif pair(composition)[0] == True:
        return "pair", pair(composition)[1]
    elif high_card(composition)[0] == True:
        return "high card", high_card(composition)[1]
#--------------------------------------------------------------------------------------------
def compare_similar_jeu(meilleur_value_jeu, meilleur_jeu, jeu, compo_jeu):
    if order_jeu_invert[jeu] > order_jeu_invert[meilleur_value_jeu]:
        meilleur_value_jeu, meilleur_jeu = jeu, compo_jeu
        return meilleur_value_jeu, meilleur_jeu
    
    elif order_jeu_invert[jeu] == order_jeu_invert[meilleur_value_jeu]:
        if jeu == "quinte flush": 
            if compo_jeu[4].valeur > meilleur_jeu[4].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            else:
                return meilleur_value_jeu, meilleur_jeu
        
            
        elif jeu == "square":
            if compo_jeu[0].valeur > meilleur_jeu[0].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            elif compo_jeu[0].valeur == meilleur_jeu[0].valeur:
                if compo_jeu[4].valeur > meilleur_jeu[4].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                else:
                    return meilleur_value_jeu, meilleur_jeu
            else:
                return meilleur_value_jeu, meilleur_jeu
                
        elif jeu == "full":
            if compo_jeu[0].valeur > meilleur_jeu[0].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            elif compo_jeu[0].valeur == meilleur_jeu[0].valeur:
                if compo_jeu[3].valeur > meilleur_jeu[3].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                else:
                    return meilleur_value_jeu, meilleur_jeu
            else:
                return meilleur_value_jeu, meilleur_jeu
                
        elif jeu == "flush":
            for i in range(len(compo_jeu)):
                if compo_jeu[i].valeur > meilleur_jeu[i].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                elif compo_jeu[i].valeur < meilleur_jeu[i].valeur:
                    return meilleur_value_jeu, meilleur_jeu
            return meilleur_value_jeu, meilleur_jeu

        elif jeu == "quint":
            if compo_jeu[4].valeur > meilleur_jeu[4].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            else:
                return meilleur_value_jeu, meilleur_jeu
            
        elif jeu == "tripps":
            if compo_jeu[0].valeur > meilleur_jeu[0].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            elif compo_jeu[0].valeur == meilleur_jeu[0].valeur:
                if compo_jeu[3].valeur > meilleur_jeu[3].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                elif compo_jeu[3].valeur == meilleur_jeu[3].valeur:
                    if compo_jeu[4].valeur > meilleur_jeu[4].valeur:
                        jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                        return jeu_copy, compo_jeu_copy
                    else:
                        return meilleur_value_jeu, meilleur_jeu
                else:
                    return meilleur_value_jeu, meilleur_jeu
            else:
                return meilleur_value_jeu, meilleur_jeu
                    
        elif jeu == "double pair":
            if compo_jeu[0].valeur > meilleur_jeu[0].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            elif compo_jeu[0].valeur == meilleur_jeu[0].valeur:
                if compo_jeu[2].valeur > meilleur_jeu[2].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                elif compo_jeu[2].valeur == meilleur_jeu[2].valeur:
                    if compo_jeu[4].valeur > meilleur_jeu[4].valeur:
                        jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                        return jeu_copy, compo_jeu_copy
                    else:
                        return meilleur_value_jeu, meilleur_jeu
                else:
                    return meilleur_value_jeu, meilleur_jeu
            else:
                return meilleur_value_jeu, meilleur_jeu

        elif jeu == "pair":
            if compo_jeu[0].valeur > meilleur_jeu[0].valeur:
                jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                return jeu_copy, compo_jeu_copy
            elif compo_jeu[0].valeur == meilleur_jeu[0].valeur:
                for i in range(1, len(compo_jeu)):
                    if compo_jeu[i].valeur > meilleur_jeu[i].valeur:
                        jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                        return jeu_copy, compo_jeu_copy
                    elif compo_jeu[i].valeur < meilleur_jeu[i].valeur:
                        return meilleur_value_jeu, meilleur_jeu
                return meilleur_value_jeu, meilleur_jeu
            else:
                return meilleur_value_jeu, meilleur_jeu
                    
        elif jeu == "high card":
            for i in range(len(compo_jeu)):
                if compo_jeu[i].valeur > meilleur_jeu[i].valeur:
                    jeu_copy, compo_jeu_copy = jeu, compo_jeu.copy()
                    return jeu_copy, compo_jeu_copy
                elif compo_jeu[i].valeur < meilleur_jeu[i].valeur:
                    return meilleur_value_jeu, meilleur_jeu
            return meilleur_value_jeu, meilleur_jeu
                
    else:
        return meilleur_value_jeu, meilleur_jeu
# -----------------------------------------------------------------------------------------------------------------
def determine_best_game(players_inf_turn, displayed_card):
    jeux_players = {}
    meilleur_jeu = displayed_card[0] + displayed_card[1] + displayed_card[2]
    meilleur_value_jeu = "high card"
    for player in players_inf_turn:
        if players_inf_turn[player][2] == True:
            composition = function_composition(players_inf_turn[player], displayed_card)
            jeu, compo_jeu = determine_jeu(composition)
            # jeux_players[players_inf_turn[player][0]] = [jeu, compo_jeu]
            jeux_players[player] = [jeu, compo_jeu]
            print(f"\nThe best game of {player} is a {jeu} :\n{compo_jeu[0].name} {compo_jeu[1].name} {compo_jeu[2].name} {compo_jeu[3].name} {compo_jeu[4].name}\n")
            meilleur_value_jeu, meilleur_jeu = compare_similar_jeu(meilleur_value_jeu, meilleur_jeu, jeu, compo_jeu)
    for player in players_inf_turn:
        if players_inf_turn[player][2] == True:
            if jeux_players[player][1] != meilleur_jeu:
                players_inf_turn[player][2] = False
            else:
                print("\n-----------------------------------------------------------------------------------------------------\n")
                print(f"{player} win the hand with {jeux_players[player][0]} !\n")
    return

def show_down(deck, displayed_card):
    while len(displayed_card) < 3:
        street_pos = dico_street[len(displayed_card) + 1]
        displayed_card.append(new_tirage(street_pos, deck))
    return displayed_card

def function_composition(info_player, displayed_card):
    return info_player[3] + displayed_card[0] + displayed_card[1] + displayed_card[2]
  
def order_of_play(players_inf_turn, street="preflop"):
    players_inf_turn_2 = {}
    if street == "preflop":
        for position in speak_order_preflop[-len(players_inf_turn):]:
            for player in players_inf_turn:
                if position in players_inf_turn[player][0]:
                    players_inf_turn_2[player] = players_inf_turn[player]
                    break
    else:
        for position in speak_order_postflop[len(players_inf_turn)]:
            for player in players_inf_turn:
                if position in players_inf_turn[player][0]:
                    players_inf_turn_2[player] = players_inf_turn[player]
                    break      
    players_inf_turn = players_inf_turn_2.copy()
    return players_inf_turn

def function_biggest_bet(street, game_type):
    if street == "preflop":
        biggest_bet = 1/100 * list_stack[game_type]
    else: 
        biggest_bet = 0
    return biggest_bet

def function_temporary_decision_1(player, pot, biggest_bet, players_inf_turn):
    while True:
        try:
            decision = str(input(f"\nThis is the turn of {player}. The pot contain {pot}$." + "\n" + f"The biggest bet is {biggest_bet}$. The current mise of {player} is {players_inf_turn[player][5]}$." + "\n\n" + f"Possible action are check or raise : "))
            if (decision == "check") or (decision == "raise"):
                return decision
            else:
                print("Please enter a input!")
        except ValueError:
            print("Please enter a input!")

def function_temporary_decision_2(player, pot, biggest_bet, players_inf_turn):
    while True:
        try:
            decision = str(input(f"\nThis is the turn of {player}. The pot contain {pot}$." + "\n" + f"The biggest bet is {biggest_bet}$. The current mise of {player} is {players_inf_turn[player][5]}$." + "\n\n" + f"Possible action are fold, call or reraise : "))
            if (decision == "fold") or (decision == "call") or (decision == "reraise"):
                return decision
            else:
                print("Please enter a input!")
        except ValueError:
            print("Please enter a input!")

def function_action_player(player, count_player_action, temporary_decision):
    if temporary_decision == "raise" or temporary_decision == "reraise":
        for element in count_player_action:
            count_player_action[element] = 0
        count_player_action[player] = 1
        return count_player_action
    elif temporary_decision == "call" or temporary_decision == "check":
        count_player_action[player] = 1
        return count_player_action

def new_street(players_inf_turn, pot, game_type, street="preflop"):
    biggest_bet = function_biggest_bet(street, game_type)
    count_eliminated_player = 0
    for ele in players_inf_turn:
        if ele[2] == False:
            count_eliminated_player += 1
    action = True
    count_player_action = {player: 0 for player in players_inf_turn}
    while (count_eliminated_player != len(players_inf_turn) - 1) and (action == True):
        action = False
        for player in order_of_play(players_inf_turn):
            if (players_inf_turn[player][2]) and (players_inf_turn[player][5] == biggest_bet) and (players_inf_turn[player][1] > players_inf_turn[player][4]) and (count_eliminated_player != len(players_inf_turn) - 1) and (count_player_action[player] == 0):
                temporary_decision = function_temporary_decision_1(player, pot, biggest_bet, players_inf_turn)
                if temporary_decision == "check":
                    print(f"{player} check")
                    action = False
                    count_player_action = function_action_player(player, count_player_action, temporary_decision)
                elif temporary_decision == "raise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn[player][1])
                    pot += biggest_bet 
                    players_inf_turn[player][5] += biggest_bet
                    print(f"{player} raise {biggest_bet}$")
                    count_player_action = function_action_player(player, count_player_action, temporary_decision)
            elif (players_inf_turn[player][2]) and (players_inf_turn[player][5] < biggest_bet) and (players_inf_turn[player][1] > players_inf_turn[player][4]) and (count_eliminated_player != len(players_inf_turn) - 1) and (count_player_action[player] == 0):
                temporary_decision = function_temporary_decision_2(player, pot, biggest_bet, players_inf_turn)
                if temporary_decision == "fold":
                    print(f"{player} fold")
                    count_eliminated_player += 1
                    players_inf_turn[player][2] = False
                elif temporary_decision == "call":
                    if (players_inf_turn[player][1] - players_inf_turn[player][4] + players_inf_turn[player][5]) <= biggest_bet: 
                        pot += players_inf_turn[player][1] - players_inf_turn[player][4] - players_inf_turn[player][5]
                        print(f"{player} call for {players_inf_turn[player][5]}$." + "\n" + f"the pot is now {pot}$.\n")
                        players_inf_turn[player][5] = players_inf_turn[player][1] - players_inf_turn[player][4]
                        count_player_action = function_action_player(player, count_player_action, temporary_decision)
                    else:
                        pot += biggest_bet - players_inf_turn[player][5]
                        print(f"{player} call for {biggest_bet - players_inf_turn[player][5]}$." + "\n" + f"the pot is now {pot}$.\n")
                        players_inf_turn[player][5] = biggest_bet
                        count_player_action = function_action_player(player, count_player_action, temporary_decision)
                elif temporary_decision == "reraise":
                    action = True
                    biggest_bet = get_number_in_range(1.5*biggest_bet, players_inf_turn[player][1])
                    pot += biggest_bet - players_inf_turn[player][5]
                    players_inf_turn[player][5] = biggest_bet
                    print(f"{player} reraise {biggest_bet}$")
                    count_player_action = function_action_player(player, count_player_action, temporary_decision)
    return pot
        
def blindes(players_inf_turn, game_type):
    for player in players_inf_turn:
        if players_inf_turn[player][0] == "Small Blind":
            players_inf_turn[player][5] += 0.5/100 * list_stack[game_type]
        elif players_inf_turn[player][0] == "Big Blind":
            players_inf_turn[player][5] += 1/100 * list_stack[game_type]

def function_fold(players_inf_turn):
    count = 0
    for player in players_inf_turn:
        if players_inf_turn[player][2] == False:
            count += 1
    if (count == len(players_inf_turn) - 1):
        return True
    return False

def new_hand(players_informations, game_type):
    print("------------------------------------------------------------------------------------------------------------------------------------------------------\nA new hand is starting ! Here are player's card :")
    deck = deck_creation()
    players_inf_turn = {}
    pot = 1.5/100 * list_stack[game_type]
    for player in players_informations.keys():
        tirage = random.sample(deck, k=2)
        print(f"\n{player} receive {tirage[0].name} and {tirage[1].name}.")
        deck.remove(tirage[0])
        deck.remove(tirage[1])
        players_inf_turn[player] = [positions_need[players_informations[player][1]], players_informations[player][0], True, tirage, 0, 0] # {Name_player : [position_jeu, stack, active/out, tirage, amount_invest, invest_street, count_action]}    
    blindes(players_inf_turn, game_type)
    pot = new_street(players_inf_turn, pot, game_type)
    update_amount_invest(players_inf_turn)
    fold_test = function_fold(players_inf_turn)
    if fold_test == True:
        update_stack(players_inf_turn, pot)
        for player in players_informations.keys():
            players_informations[player][1] = players_inf_turn[player][1]
        return players_informations
    street, state, order_show_card = state_hand(players_inf_turn)
    displayed_card = []
    if order_show_card == True:
        displayed_card = show_down(deck, displayed_card)
        determine_best_game(players_inf_turn, displayed_card)
    while state == True:  
        print("\n-----------------------------------------------------------------\n")      
        displayed_card.append(new_tirage(street, deck))
        pot = new_street(players_inf_turn, pot, game_type, street)
        update_amount_invest(players_inf_turn)
        if fold_test == True:
            update_stack(players_inf_turn, pot)
            for player in players_informations.keys():
                players_informations[player][1] = players_inf_turn[player][1]
            return players_informations
        street, state, order_show_card = state_hand(players_inf_turn, street)
        if order_show_card == True:
            displayed_card = show_down(deck, displayed_card)
            determine_best_game(players_inf_turn, displayed_card)
    update_stack(players_inf_turn, pot)
    for player in players_informations.keys():
        players_informations[player][0] = players_inf_turn[player][1]
    return players_informations

def function_state_players(players_informations):
    state_players = []
    for player in players_informations:
        state_players.append(players_informations[player][2])
    return state_players

def lauch_game():
    print("\n------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print("Welcome in cash game poker party !\n")
    game_type = function_game_type()
    list_players = add_player()
    players_informations = initialize_players_information(list_players, game_type)
    state_players = function_state_players(players_informations)
    while state_players.count(True) > 1:
        players_informations = new_hand(players_informations, game_type) 
        players_informations, player_out = activate_player(players_informations, game_type)
        if player_out != []:
            for player in player_out:
                gain = players_informations[player][0] - players_informations[player][3]
                print(f"{player} leave the table. {player} gain are {gain}.")
                players_informations.pop(player)
        state_players = function_state_players(players_informations)
        players_informations = change_players_position(players_informations)
    print("the game ended !")

lauch_game()  



     


