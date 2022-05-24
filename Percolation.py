from random import randint, sample, seed
from colorama import Fore, Style
from os import system, name
from time import sleep, time


class Find:
    """
    Find Class is a search algorithm protocol for connecting items in a network by keeping track of the root of an item.
    
    The parent Find Class requires a single parameter: the size property. The total number of members or items in a
    network is NxN, where N is the one-dimensional size property, is represented by the space property.

    In order to maintain and keep track of the connections in the network, the class uses a roots lists. The index of
    the list represents members in the network, and the list's values represent the roots of members. A root determines
    what other members in the network the item is connected to. Two members in the network are connected when they share
    the same root item. The root can be directly connected to a member, or the root can be connected along a path (see
    below for more details). Index 0 represents the first item in the network and space - 1 represents the last.

    In order to manage the list, the find class has a search protocol to access the root from the root list, and a
    method to connect to items in the network. These methods are the find() and union() method respectfully. It also has
    two methods, connect() and connected() that utilize find and union to check and manage the network and its roots.
    The class has four child classes: QuickUnion, WeightedQuickUnion, PathCompression, and QuickFind. The basis methods
    used in the search protocol are from the QuickUnion algorithm, which is the basis child class of two other classes,
    WeightedQuickUnion and PathCompression. It acts as kind of default class and should be used when creating a basic
    Find object (i.e. a Find Object itself should not be instantiated). QuickFind uses a slightly different protocol
    where the find method can access roots directly and is computationally heavier (see below for more details).
    
    As stated above, the default algorithm for the protocol is quick union, which is a recursive search algorithm.
    The default union method uses a quick union update of the root list, which sets the root of one item to the other.
    The default search method uses a find roots method, which is a recursive search to find a root. A root is found when
    a number has itself as the root. All indexed numbers (from 0 to space - 1) have a root in the root list, which is
    initially defined as itself. When items in the network are connected, one root value will be changed to a different
    number by updating a singe value in the roots list, while the other connected number maintains itself as the root in
    the list indicating that it is root node of a series of connected numbers otherwise known as tree branches or paths.
    This is tree branch or path concept is simple: all numbers in the network point to another number, or to itself.
    The value in the root list that the indexed item points to is considered to be its direct connection on the branch.
    A number belongs to a tree branch when you follow the path of the item until you reach a root that points to itself.
    When starting with any item indexed item (network member), if the root of that number is not itself, that number is
    connected to the number it points to in the roots list. The root of the tree is found by following the sequential
    pointers until the number points to itself. All numbers in the network that either share the same root, or point to
    a root along a path to a single root, are considered to be connected. Full connection in the network occurs when all
    numbers point to a single root in the root list directly or along a path on the tree branch.
    
    All child classes, with the exception of QuickFind, use this concept to demonstrate connection in a network.
    QuickFind uses direct connection only- any number in the network is connected to a root with a direct connection in
    the roots list. Full connection in a network occurs when all numbers have just one base root in the root list.

    ...
    
    Attributes
    ----------
    size: int
        the base measure of the network in one-dimension where the total number of members of the network is size X size
    space: int
        the total number of members in a network, size X size, representing a two-dimensional matrix in one-dimension
    roots: list of int
        list of roots of the members in a network which are the indexed numbers with each root represented by an integer
        
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
    numbers()
        Returns list of int. Shows a list of all the members in the network from one to the space attribute.
    """

    def __init__(self, size):
        """
        Takes an integer as an argument to create a search protocol for network connection and models the network as an
        indexed list where each indexed number is a item in a network. The outward facing list runs from one to
        N-squared, where N is the size property. Index zero represents the first item in the network, and the index at
        N-squared minus one is the final item in the network. Size property must be greater than zero as the network
        must have at least one member. Space property is set as size-squared and is the total number of items. Size and
        Space should not be changed once the network has been set, as the protocol relies on a fixed two-dimensional,
        N x N geometry of rows and columns represented in one-dimension by a list of roots that show how each item in
        the network is connected.
        
        Parameters
        ----------
        size: int
            the basis number for the total number of members in a network, size X size
        """
        self.size = size
        self.space = size ** 2
        self.roots = [num + 1 for num in range(self._space)]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value <= 0:
            raise ValueError("The size of the network must be greater than zero.")
        self._size = value

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, value):
        self._space = value

    def connected(self, a, b):
        """Checks if two items in the network have the same root. Calls the find_root method. Returns boolean."""
        root = self.find_root
        return root(a) == root(b)

    def connect(self, a, b):
        """Connects two items in the network if the roots are different. Calls the union method. Returns none."""
        root = self.find_root
        p = root(a)
        q = root(b)
        if p != q:
            self.union(p, q)

    # Default is QuickUnion algorithm. Sets the root of the first item passed to the second item to show connection
    def union(self, p, q):
        """Updates the roots list to show the connection between two items. Returns none."""
        self.roots[p - 1] = q

    # Default is QuickUnion algorithm. Recursively checks the root until the root equals the number itself.
    def find_root(self, n):
        """Returns the root of an item in the network. Returns an integer."""
        while self.roots[n - 1] != n:
            n = self.roots[n - 1]
        return n

    def numbers(self):
        """Returns a list of all the items in the network. Returns a list of integers."""
        return [num + 1 for num in range(self._space)]


class QuickUnion(Find):
    """
    Default child class of parent class Find. Other QuickUnion-related protocols are built on this basic algorithmic
    data structure. This child class should be called when creating a basic Find Object, and not a Find Object itself.

    Attributes and Methods
    ----------------------
    See the Find parent class
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
        Returns None. Connects two items in the network if they do not have the same root and performs path compression.
    pass_compression(a, b)
        Returns None. Updates all the roots of items in a path to the root of initial item to flatten the tree size.
    """

    def connect(self, a, b):
        """Connects two items if the roots are different and compresses the tree sizes. Returns none."""
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
        """Returns the root of an item in the network. Returns an integer."""
        return self.roots[n - 1]

    def union(self, p, q):
        """Updates any item that has the same root as the first item to the root of the second. Returns none."""
        for num in range(self.space):
            if self.roots[num] == p:
                self.roots[num] = q


class Board:
    """
    Board Class is an object that represents a space of interconnected positions in a directional N x N matrix. It is an
    abstraction of an initially empty network where positions get opened and filled as new members join the network
    and connect with one another.

    A Board is a directional, N x N matrix that has a top and bottom row, and a left and right column representing the 
    edges or boundaries of the abstract space. The abstraction represents a network of any kind where the members can
    stand in relation to each other in a matrix, or row by column grid. At first, all positions in the network are not
    considered to be a part of the network. Any row or column of the matrix can be selected to join the network. When
    a row and column position within the boundaries is selected, the selected position joins and becomes a part of the
    network. A position on the board that is in the network is open, and a position not in the network is closed. A
    closed or unoccupied position is represented by 0, and an open or occupied position is represented by 1. Any
    adjacent open positions are considered to be connected to each other in the network. The finder object in the board
    class keeps track of all the connections of all the open positions on the board, or items in the network. A board is
    fully occupied or connected when all positions are open. In addition, any position in the first row that is open is
    also known asa a full position. Any position connected to a position in the first row is also a full position. The
    reason for this is because the board is directional: the flow of full positions is downward. The board is said to
    percolate when there is a complete and full path from the top row to the bottom row.

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
    open_positions: int
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
    number_of_open_positions()
        Returns int. Returns the total number of open sites on the game board
    is_full(n)
        Returns bool. Checks if the position is full. A full position is defined as a position on the board that is
        connected to an open position in the top row of the board. Full positions can only flow down once a position in
        the first row has been opened, and any subsequent connected positions are also considered full.
    percolates()
        Returns bool. Checks if the board has percolated. Percolation is defined as a path of full positions starting
        from top to the bottom. Makes two sets of roots for the top and bottom rows. If the two sets have a common
        element, then percolation has occurred.
    show_board()
        Returns none. Prints a two-dimensional state of the current board with open and closed positions
    show_numbers_and_roots_list()
        Returns none. Prints a list of the members in the network and a list of the roots
    show_roots()
        Returns none. Prints each number on the board pointing to the root of the number
    """
    def __init__(self, size, find='QuickFind'):
        """
        Takes an integer and string as arguments to initialize a Board object that is a two-dimensional matrix
        represented by a one-dimensional list. The integer parameter is the size attribute that is the one-dimensional
        value that makes up the size X size space attribute, representing the total number of positions on the board or
        the maximum number of members in the network. The string argument is used to create a Find object that also
        represents the same network. After the find parameter is validated, a Find object is created where the size,
        and by proxy the space, attribute are validated. A board object is a list of positions that can be open,
        closed, or full depending on the relationship of the position in the overall network. Initially the positions
        are all closed. The final attribute is an integer, open positions, which tracks the total number of open
        positions on the board at any given time, and increases each time the method open gate returns True.
        """
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
        self.open_positions = 0

    # Validation of properties are done in the Find Class- these properties should not be changed after initialization
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
        """Setter function guarantees a valid string for the Find Object was passed to the Board Class object."""
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
            self.open_positions += 1
            self.__connect(a, b, position)
            return True
        return False

    def __position(self, a, b):
        """Returns a flattened, one-dimensional location of a two dimensional point on the board."""
        # if (a < 1 or b < 1) or (a > self._size or b > self._size):
        #     raise ValueError('Invalid arguments were passed to the function.')
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

    # def __positions(self, position):
    #     """Returns the row and column on the 2-D board from the 1-D board position."""
    #     col = int(position % self.size)
    #     if col == 0:
    #         col = self.size
    #     row = int((position - col + self.size) / self.size)
    #
    #     return row, col

    def number_of_open_positions(self):
        """Returns the number of open positions or sites on the game board. Returns integer."""
        return self.open_positions

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
        root = self.finder.find_root
        top_row = {root(i + 1) for i in range(self.size)}
        bottom_row = {root(i + 1) for i in range(self.space - self.size, self.space)}
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
        """Prints a quick 2-D representation of the 1-D game board. Returns None."""
        for position, mark in enumerate(self.board):
            print(str(mark) + '   ', end='')
            if position % self.size == self.size - 1:
                print('\n')

    def show_numbers_and_roots_list(self):
        """Prints a list of board positions and a list of each position's root. Returns None."""
        print(self.finder.numbers())
        print(self.finder.roots)

    def show_roots(self):
        """Prints each number on the board pointing to the root of that number. Returns None."""
        for i in range(self.space):
            print(f"{i + 1} -> {self.finder.roots[i]}")

    # def show_board_position_and_roots(self):
    #     for i in range(self.space):
    #         a, b = self.__positions(i + 1)
    #         print(f"({a}, {b}) -> {self.finder.roots[i]}")


class Visualizer:
    """
    A Visualizer Object creates a formatted string version of a Board object's current state and displays it. The
    visualizer's create board method will format and display a two-dimensional matrix, showing the difference between
    open, closed, and full positions. There are three modes for the visualizer: Square, Circle, and Matrix mode. Each
    mode represents the members of a network using a different marker (a square, a circle, or 0's and 1's). Grey shows a
    closed position, black an open position, and blue (or green in Matrix mode) a full position.

    ...

    Attributes
    ----------
    board: a board object
        a Board Object with the Board Object's list attribute that is a list of zeros and ones only
    marker: str
        a string representing the type of marker to be used to display the members in the network

    Methods
    -------
    print_board(str)
        Returns none. Prints each character in the string without the new line character
    create_board()
        Returns str. Takes a Board Object list and formats it as a printable string of the current state of the network
    """
    def __init__(self, board, marker):
        self.board = board
        self.marker = marker

    @staticmethod
    def print_board(formatted_board):
        """Prints the formatted board string. Returns None."""
        for mark in formatted_board:
            print(mark, end='')

    def create_board(self):
        """Returns a formatted string of a board list of zeros and ones. Returns string."""
        new_board = ['[[']
        for position, number in enumerate(self.board.board):
            if position == 0:
                pass
            elif position % self.board.size == 0:
                new_board.append('\n [')

            if self.marker == 'Matrix':
                mark = '0.'
            elif self.marker == 'Circle':
                mark = '\u25CF'
            else:  # Default marker is a square- this default will also be set if other string argument is passed
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


class Percolate:
    def __init__(self, size=3, auto=True, find='QuickFind', speed='Fast', marker='Square'):
        self.auto, self.speed, self.marker = self.validate_parameters(auto, speed, marker)
        self.board = Board(size, find)  # find and size arguments are validated in the Board Class
        self.visualizer = Visualizer(self.board, self.marker)

    @staticmethod
    def validate_parameters(auto_value, speed_value, marker_value):
        """Validates auto, speed, and marker parameters for Watch Class object."""
        if type(auto_value) != bool:
            raise TypeError("Invalid argument was passed to auto parameter.")
        if speed_value not in ('Fast', 'Slow', 'Express', 'Inf'):
            raise ValueError("Invalid argument was passed to speed parameter.")
        if marker_value not in ('Square', 'Circle', 'Matrix'):
            raise ValueError("Invalid argument was passed to marker parameter.")

        return auto_value, speed_value, marker_value

    def percolate(self):
        """
        Takes a N x N matrix Board Object and randomizes open positions on the board until percolation has occurred. It
        will print the percolation threshold which is the point at which the board percolated. It gives a ratio of the
        total number of open positions to the total number of positions on the board. If the auto parameter is False,
        the positions will be taken from input by the user by row and column.
        """
        if self.auto:
            Percolate.clear()

        # done = False
        while True:
            if self.auto is True:  # this if/else guarantees valid board position is passed to the board object
                a = randint(1, self.board.size)
                b = randint(1, self.board.size)
            else:
                a, b = self.enter_position()  # calls method to get valid input from the user

            if not self.board.open_gate(a, b):  # checks if position has already been played- if so, moves to next input
                if self.auto is False:          # message below is only displayed in play mode with user input
                    print(f"\n\nThe numbers {a} and {b} have already been played.")
                sleep(0.05)
                continue

            formatted_board = self.visualizer.create_board()  # gets a string representation of the current board state
            if self.auto:
                Percolate.clear()  # for display purposes in auto mode to prevent screen flashing
            print('\n')
            print(f"The new numbers are {a} and {b}.")
            self.visualizer.print_board(formatted_board)  # displays the current board state for desired time
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
                threshold = round(self.board.number_of_open_positions() / self.board.space, 4)
                print(f"The Game is over and percolation occurred at {round(threshold * 100, 2)}%")
                break

            # extra protection to make sure the game quits and for debugging/testing- unnecessary if everything is ok
            # if self.board.number_of_open_positions() == self.board.space:
            #     done = True

    # define our clear function from GeeksForGeeks
    @staticmethod
    def clear():
        """Clears the screen for before displaying the new board."""
        if name == 'posix':
            _ = system('clear')

    def enter_position(self):
        """Gets a board position, row and column, in the N x N matrix from input by the user. Returns two integers."""
        a = b = 0
        while True:
            try:
                a = int(input("A: "))
                if not 0 < a <= self.board.size:
                    print(f"Enter a number between one and the size of your board ({self.board.size}).")
                    continue

                b = int(input("B: "))
                if not 0 < b <= self.board.size:
                    print(f"Enter a number between one and the size of your board ({self.board.size}).")
                    continue
            except ValueError:
                print(f"Enter an integer between one and the size of your board (from 1 to {self.board.size}).")
                continue
            break

        return a, b

    @classmethod
    def instantiate_game(cls):
        """Returns a Game Object from input by the user."""
        auto = True
        while True:
            answer = input("\nWould you like to play or watch auto-play? Enter 'Yes' to play or 'No' to watch: ")
            response = ['yes', 'y', 'no', 'n']
            answer = answer.lower()
            if answer not in response:
                print("\nPlease enter 'Yes' or 'No' only.")
                continue
            if 'y' in answer:
                auto = False
            break

        size = 3
        while True:
            try:
                size = int(input("\nEnter a size N, for your N x N game board: "))
                if size <= 0:
                    print("\nThe size must be greater than zero.")
                    continue
                if size > 50:
                    print("\nThe size must be less than fifty.")
                    continue
            except ValueError:
                print("\nEnter a whole number greater than zero.")
                continue
            break

        find = 'QuickUnion'
        while True:
            answer = input("\nChoose your find kernel: 'QuickUnion', 'QuickFind', 'WeightedQuickUnion' or "
                           "'PathCompression', or press 'Enter' for 'QuickUnion': ")
            if len(answer) == 0:
                break
            response = ['quickunion', 'quickfind', 'weightedquickunion', 'pathcompression']
            answer = answer.lower().replace(' ', '')
            if answer not in response:
                print("\nPlease choose a valid find kernel only.")
                continue
            if answer == 'quickfind':
                find = 'QuickFind'
            elif answer == 'weightedquickunion':
                find = 'WeightedQuickUnion'
            elif answer == 'pathcompression':
                find = 'PathCompression'
            break

        speed = 'Fast'
        if auto:
            while True:
                answer = input("\nChoose your game speed: 'Fast', 'Slow', 'Express', or 'Inf'. 'Fast' is the default.\n"
                               "It's recommend to pick the speed based on your board size. Press 'Enter' for default: ")
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

        return Percolate(size, auto, find, speed, marker)


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

    def positions(self, position):
        """Returns the row and column on the 2-D board from the 1-D board position."""
        col = int(position % self.size)
        if col == 0:
            col = self.size
        row = int((position - col + self.size) / self.size)

        return row, col

    # Test Method 1 performs much slower than Method 2 because it uses two randomized points with points repeating
    @elapsed_time
    def percolation_test_1(self, find):
        percolation_list = []
        for i in range(self.iterations):
            board = Board(self.size, find)
            while not board.percolates():
                a = randint(1, board.size)
                b = randint(1, board.size)
                board.open_gate(a, b)
            percolation_list.append(round(board.open_positions / board.space, 4))

        average = sum(percolation_list) / len(percolation_list) * 100
        print(f"Percolation Threshold Average: {(round(average, 4))}%")
        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")

    # Test Method 2 is quite a bit faster than Test Method 1-> Renamed to monte_carlo_percolation_test
    @elapsed_time
    def monte_carlo_percolation_test(self, find, randomized=True, seed_value=None):
        """
        Test Function that takes a 2-Dimensional board of size NxN over I iterations of the board as defined in the
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
                seed(i + seed_value)
            else:  # else statement to avoid error warning that seed_value is None-> does not affect randomized tests
                seed_value = 0
            marks = sample(range(1, space + 1), space)  # a list of random or seeded random values on the 1-D board
            board = Board(self.size, find)
            for position in marks:
                a, b = self.positions(position)  # takes the 1-D position and transforms it to a row and column position
                board.open_gate(a, b)
                if board.percolates():
                    # print(f"The test ended after {board.open_positions} plays.")
                    break
            percolation_list.append(round(board.open_positions / board.space, 4))
            # board.show_roots()
            # v = Visualizer(board, "Circle")
            # v.print_board(v.create_board())

        average = sum(percolation_list) / len(percolation_list) * 100
        print(f"Percolation Threshold Average: {(round(average, 4))}%")
        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")

    @elapsed_time
    def monte_carlo_full_connection_test(self, find, seed_value=None):
        space = self.size ** 2

        for i in range(self.iterations):
            board = Board(self.size, find)

            if seed_value is not None:
                seed((i + 1) + seed_value)

            positions = sample(range(1, space + 1), space)  # generates a random set of all positions in the network

            for position in positions:
                a, b = self.positions(position)  # get the 2-D position, row and column, on the NxN board
                board.open_gate(a, b)

            board.show_roots()
            board.show_board_position_and_roots()

        print(f"Board Size: {self.size}")
        print(f"Iterations: {self.iterations}")
        print(f"Algorithm: {find}")


def main():
    # Game.instantiate_game().play_game()
    # exit()
    #     mc = MonteCarlo(16, 100)
    # mc.monte_carlo_percolation_test('QuickFind')
    # print()
    # mc.test_1('QuickFind')
    # print()
    # mc = MonteCarlo(250, 1)
    # mc.monte_carlo_percolation_test('QuickUnion', randomized=False, seed_value=42)
    # print()
    # mc.monte_carlo_percolation_test('WeightedQuickUnion', randomized=False, seed_value=42)
    # print()
    # mc.monte_carlo_percolation_test('QuickFind', randomized=False, seed_value=42)
    # print()
    # mc.monte_carlo_percolation_test('PathCompression', randomized=False, seed_value=42)
    # print()

    # mc = MonteCarlo(25, 100)
    # mc.monte_carlo_percolation_test('WeightedQuickUnion', randomized=False, seed_value=2)
    # print()
    # mc.monte_carlo_percolation_test('QuickUnion', randomized=False, seed_value=2)
    # print()
    #
    # mc.monte_carlo_percolation_test('QuickFind')
    # print()
    # mc.monte_carlo_percolation_test('PathCompression')
    # print()
    # exit()

    mc = MonteCarlo(3, 1)
    #
    # mc.monte_carlo_full_connection_test('PathCompression', seed_value=89)
    # print()
    # mc.monte_carlo_full_connection_test('WeightedQuickUnion', seed_value=89)
    # print()

    mc.monte_carlo_full_connection_test('QuickUnion', seed_value=42)
    print()
    mc.monte_carlo_full_connection_test('PathCompression', seed_value=42)
    print()
    mc.monte_carlo_full_connection_test('WeightedQuickUnion', seed_value=42)
    print()
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
