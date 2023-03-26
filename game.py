class Mancala_Board:
    # Constructor to initialize the mancala board with name mancala
    def __init__(self, mancala):
        if mancala != None:
            self.mancala = mancala[:]
        else:
            # score for player 1 is at index 6 and that of player 2 is at index 13 rest all contains the seed values
            self.mancala = [0 for i in range(14)]
            # 0 to 5 index all are set to 4 for the player 1
            for i in range(0, 6):
                self.mancala[i] = 4
            # setting the index 7 to 12 to 4 for player 2
            for i in range(7, 13):
                self.mancala[i] = 4

    # Function to perform a player move, takes the index of the pit as input and returns repeat_turn (T/F)
    def player_move(self, i):
        j = i
        # repeat_turn is used as a flag variable to check if the last seed ended into the scoring pit
        repeat_turn = False
        # copying the value of the selected pit in add variable
        add = self.mancala[j]
        # setting the new value of that pit as 0
        self.mancala[j] = 0
        # i>6 signifies it is player 2 or the bot player chance
        if i > 6:
            stones = add

            while stones > 0:
                # below 2 lines circulate the value of i in the range of 0-14-0
                i += 1
                i = i % 14
                if i == 6:
                    continue
                else:
                    self.mancala[i % 14] += 1
                stones -= 1

            # condition of capturing the opponent's seed
            # if a player's last seed ends up in his own side, the seed is 1 in number and the pit opposite to
            # player 2 pit has some stones then all the seeds of both the pits will be transferred to player 2
            if i > 6 and self.mancala[i] == 1 and i != 13 and self.mancala[5 - (i - 7)] != 0:
                self.mancala[13] += 1 + self.mancala[5 - (i - 7)]
                self.mancala[i] = 0
                self.mancala[5 - (i - 7)] = 0

            # if the last seed ended in the store of player 2 (13 index pit) then the player 2 will get another turn
            if i == 13:
                repeat_turn = True

        # else it the palyer1 or the human player chance
        else:
            stones = add
            while stones > 0:
                i += 1
                i = i % 14
                if i == 13:
                    continue
                else:
                    self.mancala[i % 14] += 1
                stones -= 1

            # capture condition for player 1
            if i < 6 and self.mancala[i] == 1 and i != 6 and self.mancala[-i + 12] != 0:
                self.mancala[6] += 1 + self.mancala[-i + 12]
                self.mancala[i] = 0
                self.mancala[-i + 12] = 0

            # condition for repeat turn
            if i == 6:
                repeat_turn = True
        return repeat_turn

    # Function to check if the game has ended
    # The game will end if a player has finished all his seeds
    def isEnd(self):
        # seeds of player are 0
        if sum(self.mancala[0:6]) == 0:
            self.mancala[13] += sum(self.mancala[7:13])
            for i in range(14):
                if i != 13 and i != 6:
                    self.mancala[i] = 0
            return True
        # seeds of ai bot are all 0
        elif sum(self.mancala[7:13]) == 0:
            self.mancala[6] += sum(self.mancala[0:6])
            for i in range(14):
                if i != 13 and i != 6:
                    self.mancala[i] = 0
            return True
        return False

    # Function to print the mancala board after every turn of a player
    def print_mancala(self):
        # player 2 board
        for i in range(12, 6, -1):
            print('  ', self.mancala[i], '   ', end='')
        print('  ')
        # scores of both the players
        print(self.mancala[13], '                                           ', self.mancala[6])
        # player 1 board
        for i in range(0, 6, 1):
            print('  ', self.mancala[i], '   ', end='')
        print('  ')
        # module.draw_board(self.mancala)

    # husVal function returns the heuristic value for a particular move
    # Score difference is used as the heuristic value
    def husVal(self):
        if self.isEnd():
            # more negative the value of the heuristic more will be the winning probability
            if self.mancala[13] > self.mancala[6]:
                return 100
            elif self.mancala[13] == self.mancala[6]:
                return 0
            else:
                return -100
        else:
            return self.mancala[13] - self.mancala[6]


# End of the mancala game class

# MinorMax is true for the turn of bot and False for the turn of human player
def alphabeta(mancala, depth, alpha, beta, MinorMax):
    if depth == 0 or mancala.isEnd():
        return mancala.husVal(), -1
    # AI-Bot Turn, max turn
    if MinorMax:
        v = -1000000
        player_move = -1
        for i in range(7, 13, 1):
            # skip the pit with 0 seeds
            if mancala.mancala[i] == 0:
                continue

            # here 'a' is the object used for the Mancala_Board class
            a = Mancala_Board(mancala.mancala[:])
            # if turn is False means turn will switch else it won't
            turn = a.player_move(i)
            newv, _ = alphabeta(a, depth - 1, alpha, beta, turn)
            if v < newv:
                player_move = i
                v = newv
            alpha = max(alpha, v)
            if alpha >= beta:
                break

        return v, player_move

    # human player or min turn
    else:
        v = 1000000
        player_move = -1
        for i in range(0, 6, 1):
            if mancala.mancala[i] == 0:
                continue
            a = Mancala_Board(mancala.mancala[:])
            turn = a.player_move(i)
            newv, _ = alphabeta(a, depth - 1, alpha, beta, not turn)
            if v > newv:
                player_move = i
                v = newv
            beta = min(beta, v)
            if alpha >= beta:
                break

    return v, player_move
