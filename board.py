from car import Car
from copy import deepcopy

# SOME INSTRUCTIONS:
# ALL Board fields must be private!!
# if you want to make more functions for yourself, they must be private!
# The board must be 7x7 with the fourth row having an extra spot, coordinate (3,7)
# Move method: If the player tries to make an illegal move, you need to return False and print
#                 out what they did wrong
# Add Car method: No need to print out what went wrong, the user doesnt get to decide whether cars are added or not
# Remember, you can use all of the car's public methods and fields. Anything private you can't use!!

BOARDSIZE = 7


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        self.board = self.__starter_board()
        self.cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        return '\n'.join(map(str, self.board))

    def __checkCord(self, cord):
        for i in cord:
            if i not in self.board_coordinates():
                return False
        return True

    def __starter_board(self):
        board = []

        for num in range(BOARDSIZE):
            smaller_list = ["_" for num in range(7)]
            board.append(smaller_list)

        board[3].append("_")
        return board

    def board_coordinates(self):
        """ This function returns the coordinates of cells in this board in a set
        :return: A set of coordinates
        """
        # In this board, returns a list containing the cells in the square
        #  from (0,0) to (6,6) and the target cell (3,7)
        cords = set()
        for col in range(BOARDSIZE):
            for lin in range(BOARDSIZE):
                cords.add((col, lin))
        cords.add(self.target_location())
        return cords

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        #  [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        cars_moves = []
        for car_name in self.cars.keys():
            cars_moves.append((car_name, list(self.cars[car_name].possible_moves().keys())[0],
                               list(self.cars[car_name].possible_moves().values())[0]))
            cars_moves.append((car_name, list(self.cars[car_name].possible_moves().keys())[1],
                               list(self.cars[car_name].possible_moves().values())[1]))
        return cars_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return int(BOARDSIZE / 2), BOARDSIZE

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        if self.board[coordinate[0]][coordinate[1]] == "_":
            return None
        else:
            return self.board[coordinate[0]][coordinate[1]]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # implement your code and erase the "pass"
        cords = car.car_coordinates()
        name = car.get_name()
        work = 0
        is_cord = 0
        board_cords = self.board_coordinates()
        for i in cords:
            if i in board_cords:
                is_cord += 1
        if is_cord == len(cords):
            for cord in cords:
                if self.cell_content(cord) is None:
                    work += 1
            if work == len(cords):
                for i in range(len(cords)):
                    self.board[(cords[i][0])][(cords[i][1])] = name
                self.cars[name] = car
                return True
        print("This spot in the board has already been taken")
        return False

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        if name not in self.cars:
            print("Car does not exist")
            return False
        car = self.cars[name]
        exact_location = car.car_coordinates()
        if movekey == 'u':
            if exact_location[0][0] == 0 or self.cell_content((exact_location[0][0] - 1, exact_location[0][1])):
                return False
        elif movekey == 'l':
            if exact_location[0][1] == 0 or self.cell_content((exact_location[0][0], exact_location[0][1] - 1)):
                return False
        elif movekey == 'd':
            if exact_location[-1][0] == BOARDSIZE - 1 or self.cell_content(
                    (exact_location[-1][0] + 1, exact_location[-1][1])):
                return False
        elif movekey == 'r':
            if car.car_coordinates()[-1] == (self.target_location()[0], self.target_location()[1] - 1):
                pass
            elif exact_location[-1][1] == BOARDSIZE - 1 or self.cell_content(
                    (exact_location[-1][0], exact_location[-1][1] + 1)):
                return False
        else:
            return False
        if car.move(movekey):
            exact_location = car.car_coordinates()
            if movekey == 'd':
                self.board[(exact_location[0][0]) - 1][(exact_location[0][1])] = '_'
                self.board[(exact_location[-1][0])][(exact_location[-1][1])] = name
            elif movekey == 'r':
                self.board[(exact_location[0][0])][(exact_location[0][1]) - 1] = '_'
                self.board[(exact_location[-1][0])][(exact_location[-1][1])] = name
            elif movekey == 'u':
                self.board[(exact_location[-1][0]) + 1][(exact_location[-1][1])] = '_'
                self.board[(exact_location[0][0])][(exact_location[0][1])] = name
            else:
                self.board[(exact_location[-1][0])][(exact_location[-1][1]) + 1] = '_'
                self.board[(exact_location[0][0])][(exact_location[0][1])] = name
            return True
        return False

# Board1 = Board()
# car1 = Car("I", 3, (3, 3), 1)
# car2 = Car("P", 3, (0, 2), 1)
# car3 = Car("S", 2, (1, 5), 0)
# car4 = Car("K", 32, (5, 0), 1)
# Board1.add_car(car2)
# Board1.add_car(car1)
# print(Board1, '\n')
# Board1.move_car("I", 'r')
# print(Board1, '\n')
# Board1.move_car("I", 'r')
# print(Board1, '\n')
# Board1.add_car(car3)
# print(Board1, '\n')
# Board1.move_car("P", 'r')
# print(Board1, '\n')
# Board1.move_car("S", 'u')
# print(Board1, '\n')
#
# Board1.add_car(car4)
# print(Board1, '\n')
