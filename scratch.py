from game_online import Game

clients = [1,2,3,4]

names = ['a','b','c','d']

game = Game()

game.set_up(names)

player_list = [(),(),(),()]

for i in range(len(player_list)):
    player_list[i] += (clients[i],names[i],game.player_list[i])

player_list.sort(key = lambda x: x[2].seat_num, reverse = False) #orders the list based on the seat number
print(player_list)