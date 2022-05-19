from random import randint, sample, seed
from colorama import Fore, Style
from os import system, name
from time import sleep, time


class Find:
    """
    Find Class is a search algorithm protocol for connecting items in a network by keeping track of the root of an item.
    
    The parent Find Class requires a single parameter: the size property. The total number of members or items in a
    network is NxN, where N is the one-dimensional size property, is represented by the space property.

    In order to maintain and keep track of the connections in the network, the class uses parallel lists:
    one representing the members in the network, and the other representing the roots of the items. A root determines
    what other members in the network the item is connected to. Two members in the network are connected when they share
    the same root item. The root can be directly connected, or connected along a path (see below for more details).

    The class has four child classes: QuickUnion, WeightedQuickUnion, PathCompression, and QuickFind. The methods used
    in the search protocol are QuickUnion, which is the basis child class of two other classes, WeightedQuickUnion and
    PathCompression, and acts as kind of default class and should be used when creating a basic Find object.
    
    The default union method uses a quick union update of the root list, which sets the root of one item to the other.
    The default search method uses a find roots method, which is a recursive search to find a root. A root is found when
    a number has itself as the root. All indexed numbers in the numbers list has a root in the root list, which is
    initially defined as itself. As items in the network are connected, the root will be changed to a different number
    in the root list, or the root in the list remains as itself indicating that it is root node of a series of connected
    numbers. This is based on a tree or path concept: all numbers in the network point to another number, or to itself.
    The number in the root list that the item in the numbers list points to is considered to be its direct connection.
    A number belongs to a tree when you follow the path of the item until you reach a root that points to itself.
    When starting with any item in the numbers list, if the root of that number is not itself, then that number is
    connected to number it points to in the roots list. The root of the tree is found by following the sequential
    pointers until the number points to itself. All numbers in the network that either share the same root, or point to
    a root along a path to a single root, are considered to be connected. Full connection in the network occurs when all
    numbers point to a single root in the root list directly or along a path.
    
    All child classes, with the exception of QuickFind, use this concept to demonstrate connection in a network.
    QuickFind uses direct connection only: any number in the tree is connected to a root with a direct connection of one
    base root. Thus, full connection in a network occurs when all numbers have just one root in the root list.

    ...
    
    Attributes
    ----------
    size: int
        one-dimensional parameter where the size squared represents the total number of members in a network
    space: int
        the total number of members in a network, size X size, representing a two-dimensional matrix in one-dimension
    # numbers: list of int
    #     list of members in a network with each member represented by an integer
    roots: list of int
        list of roots of members in a network with each root represented by an integer
        
    Methods
    -------
    connected(a, b)
        Returns Boolean. Shows if two items have the same root in the network and are already connected.
    connect(a, b)
        Returns None. Connects two items in the network if they do not have the same root.
    union(p, q)
        Returns None. Updates the roots of two items to connect them in a network.
    find(n)
        Returns int. Finds the root of an item in a network and returns it.   
    """

    def __init__(self, size):
        """
        Takes an integer as argument to create a search protocol for network connection. Size property must be greater
        than zero. Space property is set as size squared.
        
        Parameters
        ----------
        size: int
            the basis number for the total number of members in a network, size X size
        """
        self.size = size
        self.space = size ** 2
        # self.numbers = [num + 1 for num in range(self._space)]
        self.roots = [num + 1 for num in range(self._space)]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value <= 0:
            raise ValueError("The size must be greater than zero.")
        self._size = value

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, value):
        self._space = value

    def connected(self, a, b):
        """Checks if two items from numbers list have the same roots. Calls the find_root method. Returns boolean."""
        root = self.find_root
        return root(a) == root(b)

    def connect(self, a, b):
        """Connects two items from numbers list if the roots are different. Calls the union method. Returns none."""
        root = self.find_root
        p = root(a)
        q = root(b)
        if p != q:
            self.union(p, q)

    # Default is QuickUnion algorithm. Sets the root of the first item passed to the second item to show connection
    def union(self, p, q):
        """Updates the roots list to show the connection between two items from roots list. Returns none."""
        self.roots[p - 1] = q

    # Default is QuickUnion algorithm. Recursively checks the root until the root equals the number itself.
    def find_root(self, n):
        """Returns the root of an item from the root list. Takes an item from the numbers list."""
        while self.roots[n - 1] != n:
            n = self.roots[n - 1]
        return n


class QuickUnion(Find):
    """
    Default child class of parent class Find. Other QuickUnion-related protocols are built on this basic algorithmic
    data structure.
    
    Attributes and Methods
    ----------------------
    See the parent class 
    """

    # Equivalent to the base Find Class and used as a basis of other models based on QuickUnion
    def __init__(self, size):
        super().__init__(size)


class WeightedQuickUnion(QuickUnion):
    """
    Child class of QuickUnion class. Based on QuickUnion except uses a weighted tree decision strategy to call
    the union method.
    
    Attributes
    ----------
    tree size: list of int
        list of tree size of members in a network represented by an integer
        
    Methods
    -------
    union(p, q)
        Returns None. Updates the root of one item to the other based on which tree size is smaller, and connects them.
    """

    def __init__(self, size):
        super().__init__(size)
        self.tree_size = [1 for _ in range(self._space)]

    def union(self, p, q):
        """Updates the roots list based on tree size to show the connection between two items. Returns none."""
        if self.tree_size[p - 1] < self.tree_size[q - 1]:
            super().union(p, q)
            self.tree_size[q - 1] += self.tree_size[p - 1]
        else:
            super().union(q, p)
            self.tree_size[p - 1] += self.tree_size[q - 1]


class PathCompression(WeightedQuickUnion):
    """
    Child class of WeightedQuickUnion class. Based on WeightedQuickUnion except uses path compression to flatten
    the size of trees when the roots are not equal.
    
    Attributes
    ----------
    tree size: list of int
        list of tree size of members in a network represented by an integer
        
    Methods
    -------
    connect(a, b)
        Returns None. Connects two items in the network if they do not have the same root, and perform path compression.
    pass_compression(a, b)
        Returns None. Updates the all the roots of items in a path to the root of initial item to flatten the trees.
    """

    def connect(self, a, b):
        """Connects two items if the roots are different. Calls path compression before union call. Returns none."""
        root = self.find_root
        p = root(a)
        q = root(b)

        if p != q:
            compress = self.path_compression
            compress(a, p)
            compress(b, q)
            self.union(p, q)

    def path_compression(self, initial_num, root):
        """Flattens the tree size by setting all items along the path to the root to the root. Returns none."""
        while self.roots[initial_num - 1] != root:
            node = initial_num
            initial_num = self.roots[initial_num - 1]
            self.roots[node - 1] = root


class QuickFind(Find):
    """
    Child class of base Find class. Uses a single root element for a tree where all connected members have the same
    root. Updates all items in a tree when the union method is called.
    
    Attributes
    ----------
    See the parent class
        
    Methods
    -------
    union(p, q)
        Returns None. Updates the all the items that have a root of the first item to the second item.
    """

    def __init__(self, size):
        super().__init__(size)

    def find_root(self, n):
        """Returns the root of an item from the root list. Takes an item from the numbers list."""
        return self.roots[n - 1]

    def union(self, p, q):
        """Connects two items in the list by updating the root of any item of the first to the second."""
        for num in range(self.space):
            if self.roots[num] == p:
                self.roots[num] = q


class Board:
    """
    
    ...
    
    Attributes
    ----------    
    find: str
        a valid string representing the type of find object to be called when constructing the finder attribute 
    finder: find object
        the find object used to keep track of the roots of the members and perform all search and connect functions
    size: int
        the basic dimension of a board, size X size, where size X size is represented as the space of the board
    space: int
        the total number of spaces on the board representing the total members in a network 
    board: list of int
        list of spaces on a board which are open (1) or closed (0). An open site represents an active member of network
    open_sites: int
        the total number of open sites on the board, a location which is occupied by an active member of the network
        
    Methods
    -------
    is_open(n)
        Returns bool. Looks at the board list and returns True if the position on the board is 1 (open)
    open_gate(a, b)
        Returns bool. Takes a row (a) and column (b) and calls the position method. Checks if the current position on
        the board is open or not open. If not, updates position on the board list to an open site, updates the total
        number of open sites, and calls the connect method to connect the current position to any space on board
        above, below, left, or right of the current position
    position(a, b)
        Returns int. Private method. Transforms the 2-D position in a matrix to a 1-D position on the flat board
    connect(a, b, position)
        Returns none. Private method. Connects the current open position to the four adjacent positions in a 2-D matrix.
        Finds the 1-D representation of the positions above, below, left, and right of the current position. Checks if
        each of these positions are an edge case on the board. If not, uses the finder object to connect the current
        item to the adjacent item if the adjacent item is also an open site.
    number_of_open_sites()
        Returns int. Returns the total number of open sites on the game board
    is_full(n)
        Returns bool. Checks if the position is full. A full position is defined as a position on the board that is
        connected to an open position in the top row of the board. Full positions can only flow down once a position in
        the first row has been opened, and any subsequent connected positions are also considered full.
    percolates()
        Returns bool. Checks if the board has percolated. Percolation is defined as a path of full positions starting
        from top to the bottom. Makes two sets of roots for the top and bottom rows. If the two sets have a common
        element, then percolation has occurred.
    """
    def __init__(self, size, find='QuickFind'):
        self.size = int(size)  # size validation is done in the Find Class- this will also validate the space property
        self.find = find

        if self._find == 'QuickFind':
            self.finder = QuickFind(self.size)
        elif self._find == 'WeightedQuickUnion':
            self.finder = WeightedQuickUnion(self.size)
        elif self._find == 'PathCompression':
            self.finder = PathCompression(self.size)
        else:
            self.finder = QuickUnion(self.size)

        self.space = self.size ** 2  # space is the total number of elements on the board
        self.board = [0 for _ in range(self.space)]
        self.open_sites = 0

    # Validation of properties are done ih the Find Class- decorators indicate values should not be changed manually
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, value):
        self._space = value

    @property
    def find(self):
        return self._find

    @find.setter
    def find(self, value):
        """Setter function guarantees valid Find Object was passed to the Board Class object."""
        if value not in ('QuickUnion', 'WeightedQuickUnion', 'QuickFind', 'PathCompression'):
            raise ValueError("Find kernel must be one of 'QuickUnion', 'WeightedQuickUnion', 'PathCompression' "
                             "or 'QuickFind'")
        else:
            self._find = value

    def is_open(self, n):
        """Checks if the position is open. Returns boolean"""
        return self.board[n - 1] == 1

    def open_gate(self, a, b):
        """Updates board and number of open sites. Connects position to any open adjacent positions. Returns boolean."""
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
        """Connects the currently played position to the adjacent four squares using a finder object from Find class."""
        above = position - self.size
        below = position + self.size
        left = position - 1
        right = position + 1
        connector = self.finder.connect
        if a != 1:
            if self.is_open(above):
                connector(position, above)

        if a != self.size:
            if self.is_open(below):
                connector(position, below)

        if b != 1:
            if self.is_open(left):
                connector(position, left)

        if b != self.size:
            if self.is_open(right):
                connector(position, right)

    def number_of_open_sites(self):
        """Returns the number of open positions or sites on the game board."""
        return self.open_sites

    def is_full(self, n):
        """Checks if the current position is full. Returns boolean."""
        if self.is_open(n):
            root_of_position = self.finder.find_root(n)
            top_row_root = self.finder.find_root
            for i in range(self.size):
                if root_of_position == top_row_root(i + 1):
                    return True
        return False

    def percolates(self):
        """Checks if percolation has occurred. Returns boolean."""
        # top_row = set()
        # bottom_row = set()
        root = self.finder.find_root
        top_row = {root(i + 1) for i in range(self.size)}
        bottom_row = {root(i + 1) for i in range(self.space - self.size, self.space)}
        # for i in range(self.size):
        #     top_row.add(self.finder.find_root(i + 1))
        # for i in range(self.space - self.size, self.space):
        #     bottom_row.add(self.finder.find_root(i + 1))

        common_roots = top_row.intersection(bottom_row)

        if common_roots:  # if common_roots contains any element, it will evaluate to True
            return True

        return False
    # Alternative percolation algo -> not as efficient as the one above
    #         for n in range(self.space - self.size, self.space):
    #             if self.is_full(n + 1):
    #                 return True
    #         return False

    def show_board(self):
        """Prints a quick 2-D representation of the 1-D game board."""
        for position, mark in enumerate(self.board):
            print(str(mark) + '   ', end='')
            if position % self.size == self.size - 1:
                print('\n')

    def show_numbers_and_roots_list(self):
        """Prints a list of board positions and a list of each position's root."""
        # print(self.finder.numbers)
        print([num + 1 for num in range(self.space)])
        print(self.finder.roots)

    def show_roots(self):
        """Prints each number pointing to the root of that number."""
        for i in range(self.space):
            print(f"{i + 1} -> {self.finder.roots[i]}")
            # print(f"{self.finder.numbers[i]} -> {self.finder.roots[i]}")


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
        """Returns a board as a string with all played positions indicated by a darker colour,
        and all filled positions by a colour.
        """
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
            else:  # Default marker is a square
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
        self.board = Board(size, find)  # find argument validated in the Board Class
        self.visualizer = Visualizer(self.board, self.marker)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        """Setter function guarantees valid speed was passed to the Game Class object."""
        if value not in ('Fast', 'Slow', 'Express', 'Inf'):
            raise ValueError("Invalid string argument was passed to constructor.")
        else:
            self._speed = value

    def play_game(self):
        """Takes a N x N matrix board and randomizes open spaces on the game board. Game will quit once percolation
        has occurred or once all squares have been played. If auto is False, the game will be played taking input
        from the user.
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

            formatted_board = self.visualizer.p_board()
            if self.auto:
                Game.clear()
            print('\n')
            print(f"The new numbers are {a} and {b}.")
            self.visualizer.print_board(formatted_board)
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

            # extra protection to make sure the game quits and for debugging/testing
            if self.board.number_of_open_sites() == self.board.space:
                done = True

    # define our clear function from GeeksForGeeks
    @staticmethod
    def clear():
        """Clears the screen for before printing the new board"""
        if name == 'posix':
            _ = system('clear')

    def enter_position(self):
        """Returns a board position in the NxN matrix from input by the user"""
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
        print(f"{function.__name__}: Elapsed time of {(end - start)} s")

    return wrapper


class MonteCarlo:
    def __init__(self, size, iterations):
        self.size = size
        self.iterations = iterations

    # Test Method 1 performs much slower than Method 2 because it uses two randomized points with points repeating
    @elapsed_time
    def test_1(self, find):
        percolation_list = []
        for i in range(self.iterations):
            board = Board(self.size, find)
            while not board.percolates():
                a = randint(1, board.size)
                b = randint(1, board.size)
                board.open_gate(a, b)
            percolation_list.append(round(board.open_sites / board.space, 4))

        average = sum(percolation_list) / len(percolation_list) * 100
        print(f"Percolation Threshold Average: {(round(average, 4))}%")
        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")

    def positions(self, position):
        """Returns the row and column on the 2D board from the 1D position."""
        col = int(position % self.size)
        if col == 0:
            col = self.size
        row = int((position - col + self.size) / self.size)

        return row, col

    # Test Method 2 is quite a bit faster than Test Method 1-> Renamed to monte_carlo_percolation_test
    @elapsed_time
    def monte_carlo_percolation_test(self, find, randomized=True, seed_value=None):
        """Test Function that takes a 2-Dimensional board of size N over I iterations of the board as defined in the
        class Object and performs repeated tests over randomized sets of inputs of open gates in order to find
        the percolation threshold averaged out over I.
        """
        if randomized and seed_value is not None:
            raise ValueError("When randomized is set to True, seed_value cannot be set to any value and must be None)."
                             "\nTo have reproducible results, set randomized to False and enter a seed_value.")
        elif not randomized and seed_value is None:
            raise ValueError("When randomized is set to False, seed_value must be set to an integer greater than zero.")
        percolation_list = []
        space = self.size ** 2

        for i in range(self.iterations):
            if not randomized:
                seed(i * seed_value)
            else:  # Else statement here to avoid Pycharm error warning-> does not affect the randomized tests
                seed_value = 0
            marks = sample(range(1, space + 1), space)
            board = Board(self.size, find)
            for position in marks:
                a, b = self.positions(position)
                board.open_gate(a, b)
                if board.percolates():
                    print(a, b)
                    break
            percolation_list.append(round(board.open_sites / board.space, 4))
            # board.show_roots()
        #             v = Visualizer(board, "Circle")
        #             v.print_board(v.p_board())

        average = sum(percolation_list) / len(percolation_list) * 100
        print(f"Percolation Threshold Average: {(round(average, 4))}%")
        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")

    @elapsed_time
    def monte_carlo_full_connection_test(self, find, seed_value):
        space = self.size ** 2

        for i in range(self.iterations):
            board = Board(self.size, find)
            seed((i + 1) * seed_value)
            marks = sample(range(1, space + 1), space)

            for position in marks:
                b = int(position % self.size)
                if b == 0:
                    b = self.size
                a = int((position - b + self.size) / self.size)
                board.open_gate(a, b)

            board.show_roots()
            board.show_numbers_and_roots_list()

            # print(board.show_board())
        # end = time()
        #         print(board.show_board())
        #         print(board.show_roots())
        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")


def main():
    #     mc = MonteCarlo(16, 100)
    # mc.monte_carlo_percolation_test('QuickFind')
    # print()
    # mc.test_1('QuickFind')
    # print()
    mc = MonteCarlo(175, 1)
    mc.monte_carlo_percolation_test('QuickUnion', randomized=False, seed_value=42)
    print()
    mc.monte_carlo_percolation_test('WeightedQuickUnion', randomized=False, seed_value=42)
    print()
    # mc.monte_carlo_percolation_test('QuickFind', randomized=False, seed_value=42)
    # print()
    mc.monte_carlo_percolation_test('PathCompression', randomized=False, seed_value=42)
    print()

    # mc = MonteCarlo(141, 1)
    # mc.monte_carlo_percolation_test('QuickUnion')
    # print()
    # mc.monte_carlo_percolation_test('WeightedQuickUnion')
    # print()
    # mc.monte_carlo_percolation_test('QuickFind')
    # print()
    # mc.monte_carlo_percolation_test('PathCompression')
    # print()

#     mc = MonteCarlo(3000, 1)

#     mc.monte_carlo_full_connection_test('PathCompression', seed_value=89)
#     print()
#     mc.monte_carlo_full_connection_test('WeightedQuickUnion', seed_value=89)
#     print()


#     mc.monte_carlo_full_connection_test('QuickUnion', seed_value=42)
#     print()
#     mc.monte_carlo_full_connection_test('PathCompression', seed_value=42)
#     print()
#     mc.monte_carlo_full_connection_test('WeightedQuickUnion', seed_value=42)
#     print()
#     mc.monte_carlo_full_connection_test('PathCompression', seed_value=4)
#     print()
#     mc.monte_carlo_full_connection_test('WeightedQuickUnion', seed_value=4)
#     print()
#     mc.monte_carlo_full_connection_test('QuickFind', seed_value=42)
#     print()


# @elapsed_time
# def monte_carlo_test_1(size, trials):
#     mc = MonteCarlo(size, trials)
#     mc.test_1()
#
# @elapsed_time
# def monte_carlo_test_2(size, trials, randomized, seed_value):
#     mc = MonteCarlo(size, trials)
#     mc.test_2(randomized, seed_value)

# monte_carlo_test_1(12, 300)
# monte_carlo_test_2(12, 5, False, 99)


if __name__ == "__main__":
    main()
