from player import *
from cards import *
import socket
import threading


class Game(object):
    def __init__(self):
        super().__init__()
        self.num_players = 0
        self.game_over = False
        self.player_list = []
        self.deck = Euchre_Deck()
        self.team_1 = [0]
        self.team_2 = [0]
        self.teams = [self.team_1, self.team_2]
        self.trump_suit = 0
        self.cards_in_play = []
        self.num_rounds = 0
        self.team_1_points = 0
        self.team_2_points = 0
        self.max_points = 0

    def set_up_test(self, player_name_list):
        p1 = Player("Alex")
        p2 = Player(player_name_list[0])
        p3 = Player(player_name_list[1])
        p4 = Player("Joe")
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
    def set_up(self, player_name_list):
        p1 = Player(player_name_list[3])
        p2 = Player(player_name_list[0])
        p3 = Player(player_name_list[1])
        p4 = Player(player_name_list[2])
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
                        if player.original_seat_num != 4:
                            player.seat_num = player.original_seat_num + 1 
        # Sets the order of the player list based on the seat number. 
        self.player_list.sort(key = lambda x: x.seat_num, reverse = False)
    def set_order_deal(self): # Sets the order turns based on who the dealer is.
        for player in self.player_list:
            if player.is_dealer == True:
                for i in range(1, 5):
                    if player.original_seat_num == i:
                        player.seat_num = 4
                        for other in self.player_list:
                            if other.original_seat_num != i:
                                other.seat_num = other.original_seat_num
                                if i != 4: 
                                    other.seat_num -= i
                                    other.seat_num %= 4 #loop back to remain 1-4 and not get a negative number
        # Sets the order of the player list based on the seat number. 
        self.player_list.sort(key = lambda x: x.seat_num, reverse = False)

    def get_top_card(self):
        top_card = self.deck[0]
        return top_card
    
    def ask_player_message(self, message):
        answer = input(message)
        return answer
    
    
        
    def decide_trump_top_card(self): # Deciding the trump card. Must be done after cards are dealt.
        self.reset_dealer()
        self.reset_called_trump()
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
                for player in self.player_list:
                    if player.is_dealer == True:
                        player.show_hand()                                
                        while True:
                            try:
                                switch_card = int(input("Which card would you like to switch?: (Input Number) \n"))
                            except:
                                print("Please input a number corresponding to the card you'd like to switch.")
                                continue
                            if switch_card in range(1,6):
                                break
                        player.hand.append(top_card)
                        player.called_trump = True
                        del player.hand[switch_card - 1]
                        self.deck.append(player.hand[switch_card - 1])
                        self.trump_suit = top_card.suit
                        print("The trump suit is " + top_suit + "!")
                        print("Since trump has been chosen, we can start.")
                        break
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
                player.called_trump = True
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
                print("Since trump has been chosen, we can start.")
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
                print("Since trump has been chosen, we can start.")
                player.called_trump = True
                self.trump_suit = suit_call
                break
    def trump_suit_getter(self, trump):
        if trump == 0:
            return "Spades"
        elif trump == 1:
            return "Hearts"
        elif trump == 2:
            return "Clubs"
        elif trump == 3:
            return "Diamonds"
    def reset_won_trick(self): # Resets every player's won_trick attribute to False.
        for player in self.player_list:
            player.won_trick = False
    def reset_dealer(self): #  Resets every player's is_dealer attribute to False
        for player in self.player_list:
            player.is_dealer = False
    def reset_called_trump(self): # Resets every player's called_trump to False
        for player in self.player_list:
            player.called_trump = False
    def set_dealer(self):
        if self.num_rounds % 4 != 0:
            num = self.num_rounds % 4 - 1
            original_seat_list = sorted(self.player_list, key = lambda x: x.original_seat_num, reverse = False)
            original_seat_list[num].is_dealer = True
        else:
            original_seat_list = sorted(self.player_list, key = lambda x: x.original_seat_num, reverse = False)
            original_seat_list[3].is_dealer = True
    def play_trick(self): # One full round of Euchre is played. 
        self.set_order_deal()
        self.set_order_trick()
        self.reset_won_trick()
        for player in self.player_list:
            valid_cards = [] # the indexes of the cards that can be put into play.
            for index, card in enumerate(player.hand):
                if len(self.cards_in_play) > 0: 
                    # This makes sure that if the leading card is the left bower, then only trumps are valid. 
                    if self.cards_in_play[0].value == 2 and self.cards_in_play[0].suit % 2 == self.trump_suit % 2 and self.cards_in_play[0].suit != self.trump_suit:
                        for index, card in enumerate(player.hand):
                            if card.suit == self.trump_suit:
                                valid_cards.append(index)
                        break
                    # This makes sure left bower is valid when the leading card is a trump suit card.
                    elif card.value == 2 and card.suit % 2 == self.trump_suit % 2 and self.cards_in_play[0].suit == self.trump_suit:
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
    
    def score_round(self): # Gives a score to whoever won the trick.
        lead_suit = self.cards_in_play[0].suit
        winning_card_index = -1
        for index,card in enumerate(self.cards_in_play):
            print(winning_card_index)
            if winning_card_index < 0:
                winning_card_index = 0
            elif card.suit == self.cards_in_play[0].suit and card.value == 2 and card.suit % 2 == self.trump_suit % 2:
                continue
            elif card.suit == lead_suit:
                if card.value > self.cards_in_play[winning_card_index].value:
                    winning_card_index = index
        for index,card in enumerate(self.cards_in_play):
            if card.suit == self.trump_suit or (card.suit % 2 == self.trump_suit % 2 and card.value == 2):
                print(winning_card_index)
                if self.cards_in_play[winning_card_index].suit != self.trump_suit and not (self.cards_in_play[winning_card_index].value == 2 and self.cards_in_play[winning_card_index].suit % 2 == self.trump_suit):
                    winning_card_index = index
                elif card.value == 2 and card.suit == self.trump_suit:
                    winning_card_index = index
                    break
                elif card.value == 2 and card.suit % 2 == self.trump_suit % 2:
                    winning_card_index = index
                else:
                    if card.value > self.cards_in_play[winning_card_index].value and self.cards_in_play[winning_card_index].value != 2:
                        winning_card_index = index
        winning_card = self.cards_in_play[winning_card_index]
        print(winning_card_index)
        print("This is the winning card!" , winning_card)
        winning_player = self.player_list[winning_card_index]
        winning_player.won_trick = True
        winning_team = winning_player.team
        self.teams[winning_team - 1][0] += 1
        self.cards_in_play = []
    def play_full_round(self): # Plays the full 5 rounds of Euchre and gives the score to whoever won the most tricks. 
        self.decide_trump_top_card()
        for i in range(5):
            self.play_trick()
            self.score_round()
            print("Remember: Trump is: ", self.trump_suit_getter(self.trump_suit))
        self.num_rounds += 1
        self.score_full_round()
    def score_full_round(self):
        for player in self.player_list:
            if player.called_trump == True:
                trump_caller_team = self.teams[player.team - 1]
                score_of_trump_caller = trump_caller_team[0]
                print(score_of_trump_caller)
                if score_of_trump_caller < 3:
                    if trump_caller_team == self.team_1:
                        self.team_2_points += 2
                    elif trump_caller_team == self.team_2:
                        self.team_1.points += 2
                    print("Euchred!")
                elif 3 <= score_of_trump_caller < 5:
                    if trump_caller_team == self.team_1:
                        self.team_1_points += 1
                    elif trump_caller_team == self.team_2:
                        self.team_2_points += 1
                elif score_of_trump_caller == 5:
                    if trump_caller_team == self.team_1:
                        self.team_1_points += 2
                    elif trump_caller_team == self.team_2:
                        self.team_2_points += 2
                    print("Sweep!")
        print("Here are the points for Team 1: ", self.team_1_points)
        print("Here are the points for Team 2: ", self.team_2_points)
        self.team_1[0] = 0
        self.team_2[0] = 0

    def play(self):
        while not self.game_over:
            self.deal_cards()
            self.play_full_round()
            if self.team_1_points > self.max_points or self.team_2_points > self.max_points:
                self.game_over = True
            self.deck = []
            self.deck = Euchre_Deck()