class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # implement your code and erase the "pass"
        self.__name = name
        self.__length = length
        self.__location = tuple(location)
        self.__direction = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in, listed from the front of the car to the back of the car.

                Important Notes:
                    -The head of the car is self.location. For a vertical car, the head is the TOPmost coordinate. For
                        a horizontal car, the head is the LEFTmost coordinate
                    -The coordinates should be tuples, returned inside a list
        """
        # implement your code and erase the "pass"
        #find and return hte cars coordinates
        coords = []
        location0 = self.__location[0]
        location1 = self.__location[1]
        if self.__direction == 0:
            for num in range(self.__length):
                coords.append((location0, self.__location[1]))
                location0 += 1
        else:
            for num in range(self.__length):
                coords.append((self.__location[0], location1))
                location1 += 1
        return coords

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """

        return {"u": "up", "d": "down"} if self.__direction == 0 else {"r": "right", "l": "left"}

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
                    If this move is not legal, then don't return anything
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        #  be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        list1 = []
        if movekey in self.possible_moves():
            if movekey == "u":
                list1.append((self.__location[0] - 1, self.__location[1]))
            elif movekey == "d":
                list1.append((self.__location[0] + self.__length, self.__location[1]))
            elif movekey == "r":
                list1.append((self.__location[0], self.__location[1] + self.__length))
            elif movekey == "l":
                list1.append((self.__location[0], self.__location[1] - 1))
            else:
                pass
            return list1
        return False

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        new_head_location = list(self.__location)
        if movekey in self.possible_moves():
            if movekey == "u":
                new_head_location[0] -= 1
            elif movekey == "d":
                new_head_location[0] += 1
            elif movekey == "r":
                new_head_location[1] += 1
            else:
                new_head_location[1] -= 1
            self.__location = (new_head_location)
            return True
        #change location

        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"

        return self.__name

    def get_info(self):
        return [self.__length, [self.__location[0], self.__location[1]], self.__direction]
