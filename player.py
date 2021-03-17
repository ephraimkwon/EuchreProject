class Player(object):
    def __init__(self, name = "name"):
        self.name = name
        self.hand = []
        self.win_game = False
        self.won_trick = False
        self.team = 0
        self.is_dealer = False
        self.seat_num = 0
        self.original_seat_num = 0
    def __repr__(self):
        return self.name
    def show_hand(self):
        print(self.name + "'s Hand")
        count = 0
        for card in self.hand:
            count += 1
            print(str(count)+  ": " , card)
