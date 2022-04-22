import random
import shelve


class Game:
    def __init__(self, size=5, ai=False, human_player=1, misere=False):
        self.ai = ai
        if size < 3:
            raise ValueError("Size is too small")
        self.size = size
        self.board = {}
        for j in range(3, size + 1):
            self.board[j] = 0
        self.player = 1
        self.human_player = human_player
        self.misere = misere

    def play(self):
        while True:
            print(self.show_game())
            print(f"Player {self.player}'s turn!")
            try:
                if self.ai:
                    if self.player == self.human_player:
                        self.player_input()
                    else:
                        self.x_a_stack(*self.best_move())
                else:
                    self.player_input()
            except Exception as v:
                print(v)
                continue
            if self.win():
                print(self.show_game())
                print(f'Player {1 if self.player == 2 else 2} wins!' if self.misere
                      else f'Player {self.player} wins!')
                self.board = {}
                for j in range(3, self.size + 1):
                    self.board[j] = 0
                self.player = 1
                break
            self.player = 1 if self.player == 2 else 2

    def player_input(self):
        input_stack = int(input("Which stack? "))
        input_how_many = int(input("X how many? "))
        self.x_a_stack(input_stack, input_how_many)

    def x_a_stack(self, stack, how_many):
        if stack not in self.board:
            raise ValueError(f"Stack {stack} does not exist!")
        elif how_many + self.board[stack] > stack or how_many == 0:
            raise ValueError(f"You can't X {how_many} lines in stack {stack}")
        self.board[stack] += how_many

    def win(self):
        return all(self.board[x] == x for x in self.board)

    def show_game(self):
        show_list = []
        for x in self.board:
            string = []
            for i in range(0, self.board[x]):
                string.append("X")
            while len(string) < x:
                string.append("0")
            show_list.append("".join(string))
        return " ".join(sorted(show_list, key=len, reverse=True))

    @staticmethod
    def sorted_tuple(raw_state):
        new_state = list(filter(lambda left: True if left != 0 else False, raw_state))
        return tuple(sorted(new_state))

    def convert_board_to_state(self, board):
        state = tuple(key - value for key, value in board.items())
        return self.sorted_tuple(state)

    def look_for_options(self) -> list:
        list_of_options = []
        for i in range(3, self.size + 1):
            if self.board[i] == i:
                continue
            for j in range(1, i - self.board[i] + 1):
                list_of_options.append((i, j))
        return list_of_options

    def best_move(self) -> tuple:
        mode = "misere" if self.misere else "normal"
        with shelve.open("memory") as memory:
            memory_table = memory[mode]
        if not memory_table[self.convert_board_to_state(self.board)]:
            while True:
                random_stack = random.choice(list(self.board.keys()))
                if self.board[random_stack] == random_stack:
                    continue
                return random_stack, 1
        biggest_take = 0
        for option in self.look_for_options():
            board_copy = self.board.copy()
            board_copy[option[0]] += option[1]
            new_state = self.convert_board_to_state(board_copy)
            if memory_table[new_state]:
                continue
            if option[1] > biggest_take:
                best_option = option
                biggest_take = option[1]
        return best_option


if __name__ == '__main__':
    option_game_size = 3
    option_ai = False
    option_human_player = 1
    option_misere = False

    while True:
        while True:
            try:
                print("")
                option_game_size = int(input("Enter game size from 3 to 6:"))
                if 3 <= option_game_size <= 6:
                    break
                else:
                    print("Number must be between 3 and 6")
                    continue
            except ValueError:
                print("Enter a number!")
                continue

        while True:
            print("")
            option_ai = input("Play with ai? (y/n)")
            if option_ai == "y":
                option_ai = True
                while True:
                    try:
                        print("")
                        option_human_player = int(input("Play as player 1 or 2? (1/2)"))
                        if option_human_player in {1, 2}:
                            break
                        else:
                            print("Enter either 1 or 2!")
                            continue
                    except ValueError:
                        print("Enter either 1 or 2!")
                        continue
                break
            elif option_ai == "n":
                option_ai = False
                break
            else:
                print("Enter either 'y' or 'n'")

        while True:
            print("")
            option_misere = input("Play a misere game? (Last to move loses) (y/n)")
            if option_misere == "y":
                option_misere = True
                break
            elif option_misere == "n":
                option_misere = False
                break
            else:
                print("Enter either 'y' or 'n'")

        print("")
        start = Game(option_game_size, ai=option_ai, human_player=option_human_player, misere=option_misere)
        start.play()
        while True:
            print("")
            play_again = input("Play again? (y/n)")
            if play_again == "y":
                break
            elif play_again == "n":
                exit()
            else:
                print("Enter either 'y' or 'n'")
