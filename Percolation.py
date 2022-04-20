from random import randint, sample, seed
from colorama import Fore, Style
from os import system, name
from time import sleep, time


class Find:
    def __init__(self, size):
        self.size = size
        self.numbers = [num + 1 for num in range(self.size
                                                 ** 2)]
        self.roots = [num + 1 for num in range(self.size ** 2)]
        
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        if value <= 0:
            raise ValueError("The size must be greater than zero")
        self._size = value  

    def connected(self, a, b):
        p = self.find_root(a)
        q = self.find_root(b)
        if p != q:
            self.union(p, q)
            return True
        return False
    
    # Default is QuickUnion algorithm
    def union(self, p, q):
        self.roots[p - 1] = q

    def find_root(self, n):
        while self.roots[n - 1] != n:
            n = self.roots[n - 1]
        return n


class QuickUnion(Find):
    def __init__(self, size):
        super().__init__(size)
        # print(f"QuickUnion(size={size})")

    def union(self, p, q):
        super().union(p, q)


class QuickFind(Find):
    def __init__(self, size):
        super().__init__(size)
        # print(f"QuickFind(size={size})")

    def union(self, p, q):
        for num in self.numbers:
            if self.roots[num - 1] == p:
                self.roots[num - 1] = q


class Board:
    open_sites = 0

    def __init__(self, size, find='QuickFind'):
        self.size = int(size)
        self.space = self.size ** 2
        self.board = [0 for _ in range(self.space)]

        if find == 'QuickUnion':
            self.finder = QuickUnion(self.size)
        else:
            self.finder = QuickFind(self.size)

    def is_open(self, n):
        """Checks if the position is open. Returns bolean"""
        return self.board[n - 1] == 1

    
    def open_gate(self, a, b):
        """Opens the gate if the current position is not open, updates the number or open positions, and calls the connect method to join 
        the current position to the adjacent squares. Returns boolean
        """
        position = self.__position(a, b)
        if not self.is_open(position):
            self.board[position - 1] = 1
            self.open_sites += 1
            self.__connect(a, b, position)
            return True
        return False

    def __position(self, a, b):
        """Returns a flattened, one-dimensional location of a two dimensional point on the board."""
        return (a - 1) * self.size + b

    def __connect(self, a, b, position):
        """Connects the currently played position to the adjacent four squares using a Find method."""
        above = position - self.size
        below = position + self.size
        left = position - 1
        right = position + 1

        if a != 1:
            if self.is_open(above):
                self.finder.connected(position, above)

        if a != self.size:
            if self.is_open(below):
                self.finder.connected(position, below)

        if b != 1:
            if self.is_open(left):
                self.finder.connected(position, left)

        if b != self.size:
            if self.is_open(right):
                self.finder.connected(position, right)

    def number_of_open_sites(self):
        """Returns the number of open positions on the game board."""
        return self.open_sites

    def is_full(self, n):
        """Checks if position is full by comparing the root of the position to all roots in the first row. Returns boolean."""
        if self.is_open(n):
            for i in range(self.size):
                if self.finder.find_root(n) == self.finder.find_root(i + 1):
                    return True
        return False

    def percolates(self):
        """Checks to see if percolation has occurred. Returns boolean."""
        for n in range(self.space - self.size, self.space):
            if self.is_full(n + 1):
                return True
        return False

    def show_board(self):
        """Prints a quick 2-D representation of the 1-D game board."""
        for position, mark in enumerate(self.board):
            print(str(mark) + '   ', end='')
            if position % self.size == self.size - 1:
                print('\n')

    def show_roots(self):
        """Prints a list of board positions and a list of each position's root."""
        print(self.finder.numbers)
        print(self.finder.roots)

class MonteCarlo:
    def __init__(self, size, iterations):
        self.size = size
        self.iterations = iterations

    def test_1(self):
        percolation_list = []
        space = self.size ** 2
        start = time()
        for i in range(self.iterations):
#             seed(i)
#             marks = sample(range(1,  space + 1), space)
#             print(marks)
            board = Board(self.size, 'QuickUnion')
            while not board.percolates():
#             for position in marks:
#                 b = int(position % self.size)
#                 if b == 0:
#                     b = self.size
#                 a = int( (position - b + self.size) /self.size)
# #                 print(a, b)
                a = randint(1, board.size)
                b = randint(1, board.size)
                board.open_gate(a, b)
#                 if board.percolates():
#                     break
            percolation_list.append(round(board.open_sites/board.space, 4))
        end = time()
        return percolation_list, (end-start)
    
    # Test Method 2 is almost twice as fast as Test Method 1
    def test_2(self, randomized=True, seed_value = None):
        if (randomized and seed_value is not None):
            raise ValueError("When randomized is set to True, seed_value cannot be set to any value and must be None). If you want to have reproducable\
                             results, set randomized to False and enter a seed_value.")
        elif (not randomized and seed_value is None):
            raise ValuError("When randomized is set to False, seed_value must be set to an integer greater than zero.")
        percolation_list = []
        space = self.size ** 2
        start = time()
        for i in range(self.iterations):
            seed(i * seed_value)
            marks = sample(range(1,  space + 1), space)
            board = Board(self.size, 'QuickUnion')
            for position in marks:
                b = int(position % self.size)
                if b == 0:
                    b = self.size
                a = int( (position - b + self.size) /self.size)
                board.open_gate(a, b)
                if board.percolates():
                    break
            percolation_list.append(round(board.open_sites/board.space, 4))
        end = time()
        return percolation_list, (end-start)




class Visualizer:
    def __init__(self, board, marker):
        self.board = board
        self.marker = marker

    @staticmethod
    def print_board(formatted_board):
        """Prints the board string"""
        for mark in formatted_board:
            print(mark, end='')

    def p_board(self):
        """Returns a board as a string with all played positions indicated by a darker colour, and all filled positions by a colour"""
        new_board = ['[[']
        for position, number in enumerate(self.board.board):
            if position == 0:
                pass
            else:
                if position % self.board.size == 0:
                    new_board.append('\n [')

            if self.marker == 'Matrix':
                mark = '0.'
            elif self.marker == 'Circle':
                mark = '\u25CF'
            else:
                mark = '\u25A0'

            if self.board.is_full(position + 1):
                if self.marker == 'Matrix':
                    new_board.append(Style.BRIGHT + Fore.GREEN + '1.' + ' ' + Style.RESET_ALL)
                else:
                    new_board.append(Fore.BLUE + mark + ' ' + Style.RESET_ALL)

            elif number == 0:

                new_board.append(Style.BRIGHT + Fore.WHITE + mark + ' ' + Style.RESET_ALL)

            else:
                if self.marker == 'Matrix':
                    new_board.append(Style.BRIGHT + Fore.BLACK + '1.' + ' ' + Style.RESET_ALL)
                else:
                    new_board.append(mark + ' ')

            if (position + 1) % self.board.size == 0:
                new_board.append('\b' + ']')
                if (position + 1) == self.board.size ** 2:
                    new_board.append(']')
            else:
                new_board.append(' ')

        new_board.append('\n')

        return ''.join(new_board)


class Game:
    def __init__(self, size=3, auto=True, find='QuickFind', speed='Fast', marker='Square'):
        self.auto = auto
        self.speed = speed
        self.marker = marker
        self.board = Board(size, find)
        self.visualize = Visualizer(self.board, self.marker)

    def play_game(self):
        """Takes a N x N matrix board and randomizes open spaces on the game board. Game will quit once percolation has occurred or 
        once all squares have been played. If auto is False, the game will be played taking input from the user
        """
        if self.auto:
            Game.clear()

        done = False
        while not done:
            if self.auto is True:
                a = randint(1, self.board.size)
                b = randint(1, self.board.size)
            else:
                a, b = self.enter_position()

            if not self.board.open_gate(a, b):
                if self.auto is False:
                    print(f"\n\nThe numbers {a} and {b} have already been played.")
                sleep(0.05)
                continue

            formatted_board = self.visualize.p_board()
            if self.auto:
                Game.clear()
            print('\n')
            print(f"The new numbers are {a} and {b}.")
            self.visualize.print_board(formatted_board)
            if self.auto:
                if self.speed == 'Fast':
                    sleep(0.25)
                elif self.speed == 'Slow':
                    sleep(1)
                elif self.speed == 'Express':
                    sleep(0.05)
                elif self.speed == 'Inf':
                    sleep(0.001)
                else:
                    raise ValueError("Invalid speed type was entered.")

            if self.board.percolates():
                threshold = round(self.board.number_of_open_sites() / self.board.space, 4)
                print(f"The Game is over and percolation occurred at {round(threshold * 100, 2)}%")
                break
            
            # extra protection to make sure the game quits
            if self.board.number_of_open_sites() == self.board.space:
                done = True

                
    # define our clear function from GeeksForGeeks
    @staticmethod
    def clear():
        """Clears the screen for before printing the new board"""
        if name == 'posix':
            _ = system('clear')

                
    def enter_position(self):
        """Returns a board postition in the NxN matrix from input by the user"""
        a = b = 0
        while True:
            try:
                a = int(input("A: "))
                if not 0 < a <= self.board.size:
                    print(f"Enter a number between one and the size of your board.")
                    continue

                b = int(input("B: "))
                if not 0 < b <= self.board.size:
                    print(f"Enter a number between one and the size of your board.")
                    continue

            except ValueError:
                print(f"Enter a whole number between 1 and {self.board.size}.")
                continue
            break
        
        return a, b

    @classmethod
    def instantiate_game(cls):
        """Returns a Game Object from input by the user"""
        size = 3
        while True:
            try:
                size = int(input("\nEnter a size N, for your N x N game board: "))
            except ValueError:
                print("\nEnter a whole number greater than zero.")
                continue
            if size <= 0:
                print("\nThe size must be greater than zero.")
                continue
            if size > 500:
                print("\nThe size must be less than five hundred.")
                continue
            break
        auto = True
        while True:
            answer = input("\nWould you like to play or watch auto-play? Enter 'Yes' to play: ")
            response = ('yes', 'y', 'no', 'n')
            answer = answer.lower()
            if answer not in response:
                print("\nPlease enter 'Yes' or 'No' only.")
                continue
            if 'y' in answer:
                auto = False
            break

        find = 'QuickUnion'
        while True:
            answer = input("\nChoose your find kernel: 'QuickUnion', 'QuickFind' or press 'Enter' for 'QuickUnion' ")
            if len(answer) == 0:
                break
            response = ('quickunion', 'quickfind', 'weightedquickunion')
            answer = answer.lower().replace(' ', '')
            if answer not in response:
                print("\nPlease chose a valid find kernel only.")
                continue
            if answer == 'quickfind':
                find = 'QuickFind'
            elif answer == 'weightedquickunion':
                find = 'WeightedQuickUnion'
            break

        speed = 'Fast'
        if auto:
            while True:
                answer = input("\nChoose your game speed: 'Fast', 'Slow', 'Express', or 'Inf'. 'Fast' is the default.\n"
                               "It's recommend to pick the speed based on your game size. Press 'Enter' for default: ")
                if len(answer) == 0:
                    break
                response = ('fast', 'slow', 'express', 'inf')
                answer = answer.lower()
                if answer not in response:
                    print("\nPlease choose a valid speed only.")
                    continue
                if answer == 'slow':
                    speed = 'Slow'
                elif answer == 'express':
                    speed = 'Express'
                elif answer == 'inf':
                    speed = 'Inf'
                break

        marker = 'Square'
        while True:
            answer = input("\nChoose your marker: 'Square', 'Circle', 'Matrix' or press 'Enter' for 'Square: ")
            if len(answer) == 0:
                break
            response = ('square', 'circle', 'matrix')
            answer = answer.lower()
            if answer not in response:
                print("\nPlease chose a valid marker only.")
                continue
            if answer == 'circle':
                marker = 'Circle'
            elif answer == 'matrix':
                marker = 'Matrix'
            break

        return Game(size, auto, find, speed, marker)

def elapsed_time(function):
    def wrapper(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        end = time()
        print(f"{function.__name__}: Elapsed time of {(end - start) * 1000} ms")
    
    return wrapper
    
@elapsed_time
def monte_carlo_test_1(size, trials):
    mc = MonteCarlo(size, trials)
    mc.test_1()
    
@elapsed_time
def monte_carlo_test_2(size, trials, randomized, seed_value):
    mc = MonteCarlo(size, trials)
    mc.test_2(randomized, seed_value)

if __name__ == "__main__":
#     g = Game(size=3, auto=True, find='QuickFind', speed='Fastest', marker='Square')
#     g.play_game()
#     mc = MonteCarlo(10, 500)
# #     mc_1 = mc.test()
#     mc_2 = mc.test_2(randomized=False, seed_value = 90)
# #     print(mc_1[1])
    
#     print(mc_2[1])
    
#     print(sum(mc_2[0])/len(mc_2[0]))
    
    monte_carlo_test_1(12, 3000)
    monte_carlo_test_2(12, 3000, False, 90)
#     Game.instantiate_game()
#     Game(size=30).play_game()
#     elapsed_time(len([3,3,3,3,3,3]))

    #     play = Game.instantiate_game()
#     play.play_game()