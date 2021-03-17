from player import *
from cards import *

class Game(object):
    def __init__(self):
        super().__init__()
        self.num_players = 0
        self.game_over = False
        self.player_list = []
        self.deck = Euchre_Deck()
        self.team_1 = [0]
        self.team_2 = [0]
        self.trump_suit = 0
        self.cards_in_play = []
        self.num_rounds = 0
    def set_up(self):
        name_1 = input("Input player 1 name: \n")
        name_2 = input("Input player 2 name: \n")
        name_3 = input("Input player 3 name: \n")
        name_4 = input("Input player 4 name: \n")
        p1 = Player(name_1)
        p2 = Player(name_2)
        p3 = Player(name_3)
        p4 = Player(name_4)
        self.team_1.append(p1)
        p1.team = 1
        self.team_1.append(p3)
        p3.team = 1
        self.team_2.append(p2)
        p2.team = 2
        self.team_2.append(p4)
        p4.team = 2
        player_list = [p2,p3,p4,p1]
        for player in player_list:
            self.player_list.append(player)
        p1.seat_num = 4
        p1.original_seat_num = 4
        p2.seat_num = 1
        p2.original_seat_num = 1
        p3.seat_num = 2
        p3.original_seat_num = 2
        p4.seat_num = 3
        p4.original_seat_num = 3
    def deal_cards(self):
        self.deck.shuffle()
        for player in self.player_list:
            for i in range(5):
                self.deck.deal(player)
    def set_order_trick(self): # Sets the order of who's turn it is. Orders the player_list into the order of turns based on who won trick.
        for player in self.player_list:
            if player.won_trick == True:
                if player.original_seat_num == 4:
                    player.seat_num = 1
                    for player in self.player_list:
                        if player.original_seat_num == 4:
                            pass
                        elif player.original_seat_num == 1:
                            player.seat_num = 2
                        elif player.original_seat_num == 2:
                            player.seat_num = 3
                        elif player.original_seat_num == 3:
                            player.seat_num = 4
                elif player.original_seat_num == 1:
                    player.seat_num = 1
                    for player in self.player_list:
                        if player.original_seat_num == 1:
                            pass
                        elif player.original_seat_num == 2:
                            player.seat_num = 2
                        elif player.original_seat_num == 3:
                            player.seat_num = 3
                        elif player.original_seat_num == 4:
                            player.seat_num = 4
                elif player.original_seat_num == 2:
                    player.seat_num = 1
                    for player in self.player_list:
                        if player.original_seat_num == 2:
                            pass
                        elif player.original_seat_num == 3:
                            player.seat_num = 2
                        elif player.original_seat_num == 4:
                            player.seat_num = 3
                        elif player.original_seat_num == 1:
                            player.seat_num = 4
                elif player.original_seat_num == 3:
                    player.seat_num = 1
                    for player in self.player_list:
                        if player.original_seat_num == 3:
                            pass
                        elif player.original_seat_num == 4:
                            player.seat_num = 2
                        elif player.original_seat_num == 1:
                            player.seat_num = 3
                        elif player.original_seat_num == 2:
                            player.seat_num = 4      
        # Sets the order of the player list based on the seat number. 
        self.player_list = sorted(self.player_list, key = lambda x: x.seat_num, reverse = False)
    def set_order_deal(self): # Sets the order turns based on who the dealer is.
        for player in self.player_list:
            if player.is_dealer == True:
                if player.original_seat_num == 4:
                    player.seat_num = 4
                    for player in self.player_list:
                        if player.original_seat_num == 4:
                            pass
                        elif player.original_seat_num == 1:
                            player.seat_num = 1
                        elif player.original_seat_num == 2:
                            player.seat_num = 2
                        elif player.original_seat_num == 3:
                            player.seat_num = 3
                elif player.original_seat_num == 1:
                    player.seat_num = 4
                    for player in self.player_list:
                        if player.original_seat_num == 1:
                            pass
                        elif player.original_seat_num == 2:
                            player.seat_num = 1
                        elif player.original_seat_num == 3:
                            player.seat_num = 2
                        elif player.original_seat_num == 4:
                            player.seat_num = 3
                elif player.original_seat_num == 2:
                    player.seat_num = 4
                    for player in self.player_list:
                        if player.original_seat_num == 2:
                            pass
                        elif player.original_seat_num == 3:
                            player.seat_num = 1
                        elif player.original_seat_num == 4:
                            player.seat_num = 2
                        elif player.original_seat_num == 1:
                            player.seat_num = 3
                elif player.original_seat_num == 3:
                    player.seat_num = 4
                    for player in self.player_list:
                        if player.original_seat_num == 3:
                            pass
                        elif player.original_seat_num == 4:
                            player.seat_num = 1
                        elif player.original_seat_num == 1:
                            player.seat_num = 2
                        elif player.original_seat_num == 2:
                            player.seat_num = 3      
        # Sets the order of the player list based on the seat number. 
        self.player_list = sorted(self.player_list, key = lambda x: x.seat_num, reverse = False)

    def decide_trump_top_card(self): # Deciding the trump card. Must be done after cards are dealt.
        self.set_dealer()
        self.set_order_deal()
        top_card = self.deck[0]
        top_suit = -1
        if top_card.suit == 0:
            top_suit = "Spades"
        elif top_card.suit == 1:
            top_suit = "Hearts"
        elif top_card.suit == 2:
            top_suit = "Clubs"
        elif top_card.suit == 3:
            top_suit = "Diamonds"
        for player in self.player_list:
            print("The top card is: ", top_card)
            player.show_hand()
            while True:
                answer = input("Would you like to make the top card trump? (Y/N): \n")
                if answer.lower() not in ("y", "n"):
                    print("Please enter Y or N:")
                    continue
                else:
                    break
            if answer.lower() == "y":
                while True:
                    try:
                        switch_card = int(input("Which card would you like to switch?: (Input Number) \n"))
                    except:
                        print("Please input a number corresponding to the card you'd like to switch.")
                        continue
                    if switch_card in range(1,6):
                        break
                player.hand.append(top_card)
                del player.hand[switch_card - 1]
                self.deck.append(player.hand[switch_card - 1])
                self.trump_suit = top_card.suit
                print("The trump suit is " + top_suit + "!")
                break
            elif answer.lower() == "n" and not player.is_dealer:
                continue
            elif answer.lower() == "n" and player.is_dealer:
                self.decide_trump_no_card()
    def decide_trump_no_card(self): # Decides the trump suit after everyone passes the first round.
        self.set_order_deal()
        top_card = self.deck[0]
        top_suit = ""
        if top_card.suit == 0:
            top_suit = "Spades"
        elif top_card.suit == 1:
            top_suit = "Hearts"
        elif top_card.suit == 2:
            top_suit = "Clubs"
        elif top_card.suit == 3:
            top_suit ="Diamonds"
        print("Turning down the top card. The suit " + top_suit + " is now an invalid trump suit.")
        for player in self.player_list:
            player.show_hand()
            while True:
                response = input("Would you like to call trump suit? (Y/N):\n")
                if response.lower() not in ("y", "n"):
                    print("Please enter Y or N:")
                    continue
                else:
                    break
            if response.lower() == "y":
                while True:
                    print("Suits are:\n 1: Spades \n 2: Hearts \n 3: Clubs \n 4: Diamonds")
                    
                    try:
                        suit_call = int(input("What suit would you like to be trump? \n")) - 1
                    except:
                        print("Please input a number 1 - 4")
                        continue
                    if suit_call  == top_card.suit:
                        print("This is the same as the top card trump suit.")
                        continue
                    elif suit_call not in range(4):
                        print("Please input a number 1 through 4.")
                        continue
                    else:
                        break
                self.trump_suit = suit_call
                suit_set = -1
                if suit_call == 0:
                    suit_set = "Spades"
                elif suit_call == 1:
                    suit_set = "Hearts"
                elif suit_call == 2:
                    suit_set = "Clubs"
                elif suit_call == 3:
                    suit_set ="Diamonds"
                print(f"The trump suit is {suit_set} !")
                break
            if response.lower() == "n" and not player.is_dealer:
                continue
            elif response.lower() == "n" and player.is_dealer:
                print("You just got screwed! The trump suit must be chosen by you.")
                while True:
                    print("Suits are:\n 1: Spades \n 2: Hearts \n 3: Clubs \n 4: Diamonds")
                    try:
                        suit_call = int(input("What suit would you like to be trump? \n")) - 1
                    except:
                        print("Please input a number 1 - 4")
                        continue
                    if suit_call == top_card.suit:
                        print("This is the same as the top card trump suit.")
                        continue
                    elif suit_call not in range(4):
                        print("Please input a number 1 through 4.")
                        continue
                    else:
                        break
                suit_set = -1
                if suit_call == 0:
                    suit_set = "Spades"
                elif suit_call == 1:
                    suit_set = "Hearts"
                elif suit_call == 2:
                    suit_set = "Clubs"
                elif suit_call == 3:
                    suit_set ="Diamonds"
                print(f"The trump suit is {suit_set} !")
                self.trump_suit = suit_call - 1
                break
    def reset_won_trick(self): # Resets every player's won_trick attribute to False.
        for player in self.player_list:
            player.won_trick = False
    def reset_dealer(self): #  Resets every player's is_dealer attribute to False
        for player in self.player_list:
            player.is_dealer = False
    def set_dealer(self):
        if self.num_rounds % 4 != 0:
            num = self.num_rounds % 4 - 1
            original_seat_list = sorted(self.player_list, key = lambda x: x.original_seat_num, reverse = False)
            original_seat_list[num].is_dealer = True
        else:
            original_seat_list = sorted(self.player_list, key = lambda x: x.original_seat_num, reverse = False)
            original_seat_list[3].is_dealer = True
    def play_trick(self): # One full round of Euchre is played. 
        print("Since trump has been chosen, we can start.")
        self.set_order_deal()
        self.set_order_trick()
        for player in self.player_list:
            valid_cards = [] # the indexes of the cards that can be put into play.
            for index, card in enumerate(player.hand):
                if len(self.cards_in_play) > 0:
                    # This makes sure left bower is valid when the leading card is a trump suit card.
                    if card.value == 2 and card.suit % 2 == self.trump_suit % 2 and self.cards_in_play[0].suit == self.trump_suit:
                        valid_cards.append(index)
                    # This checks that left bower is not valid if the leading card matches left bower suit.
                    elif card.suit == self.cards_in_play[0].suit and card.value == 2 and card.suit % 2 == self.trump_suit % 2:
                        continue
                    elif card.suit == self.cards_in_play[0].suit:
                        valid_cards.append(index)
                if len(self.cards_in_play) == 0:
                    valid_cards.append(index)
            for index, card in enumerate(player.hand):
                if len(valid_cards) == 0:
                    for i in range(len(player.hand)):
                        valid_cards.append(i)
            player.show_hand()
            print(valid_cards)
            while True:
                try:
                    card_to_play = int(input("What card would you like to play? \n")) - 1
                except:
                    print("Please input a number corresponding to the card you'd like to play.")
                    continue
                if card_to_play in range(len(player.hand)):
                    if card_to_play not in valid_cards:
                        print("Please choose a card that follows the rules.")
                        continue
                    if card_to_play in valid_cards:
                        break
                else:
                    print("Please choose a card that follows the rules.")
                    continue
            print("Playing: ", player.hand[card_to_play])
            self.cards_in_play.append(player.hand.pop(card_to_play))
            self.num_rounds += 1
    
    def score_round(self): # Gives a score to whoever won the trick.
        lead_suit = self.cards_in_play[0].suit
        winning_card_index = -1
        for index,card in enumerate(self.cards_in_play):
            print(winning_card_index)
            if card.suit == self.cards_in_play[0].suit and card.value == 2 and card.suit % 2 == self.trump_suit % 2:
                continue
            elif card.suit == lead_suit:
                if card.value > winning_card_index:
                    winning_card_index = index
        for index,card in enumerate(self.cards_in_play):
            print(winning_card_index)
            if card.suit == self.trump_suit or card.suit % 2 == self.trump_suit % 2 and card.value == 2:
                if card.value == 2 and card.suit == self.trump_suit:
                    winning_card_index = index
                    break
                elif card.value == 2 and card.suit % 2 == self.trump_suit % 2:
                    winning_card_index = index
                else:
                    if card.value > winning_card_index and self.cards_in_play[winning_card_index].value != 2:
                        winning_card_index = index
        winning_card = self.cards_in_play[winning_card_index]
        print("This is the winning card!" , winning_card)
        winning_player = self.player_list[winning_card_index]
        winning_player.won_trick = True
        winning_team = winning_player.team
        teams = [self.team_1, self.team_2]
        teams[winning_team - 1][0] += 1
        self.cards_in_play = []
    
    