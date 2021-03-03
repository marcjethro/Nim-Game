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
                        evaluated_options = self.options()
                        move = self.best_move(evaluated_options)
                        self.x_a_stack(*move)
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

    def look_for_options(self) -> dict:
        dict_of_options = {}
        for i in range(3, self.size + 1):
            if self.board[i] == i:
                continue
            for j in range(1, i - self.board[i] + 1):
                dict_of_options[f"{i}{j}"] = None
        return dict_of_options

    @staticmethod
    def minimum_value_of_options(options: dict) -> int:
        lowest = 101
        for i in options:
            if options[i] < lowest:
                lowest = options[i]
        return lowest

    @staticmethod
    def maximum_value_of_options(options: dict) -> int:
        highest = -101
        for i in options:
            if options[i] > highest:
                highest = options[i]
        return highest

    @staticmethod
    def best_move(options: dict) -> tuple:
        highest = -101
        best_move = ""
        for i in options:
            if options[i] > highest:
                best_move = i
                highest = options[i]
        return tuple(int(x) for x in best_move)

    def options(self, ai=True):
        simulation = Game(size=self.size, misere=self.misere)
        simulation.board = self.board.copy()
        options = simulation.look_for_options()
        for option in options:
            simulation.board = self.board.copy()
            simulation.x_a_stack(*tuple(int(x) for x in option))
            if simulation.win():
                if (self.misere and ai) or (not self.misere and not ai):
                    options[option] = -100
                else:
                    options[option] = 100
            else:
                if ai:
                    options[option] = Game.minimum_value_of_options(simulation.options(False))
                else:
                    options[option] = Game.maximum_value_of_options(simulation.options(True))
        simulation.board = self.board.copy()
        return options


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
