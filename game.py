from car import Car
from helper import load_json
from board import Board


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code here (and then delete the next line - 'pass')
        car_ = input("which car do you want to move ")
        where_ = input("what direction do you want to move it ")
        if self.board.move_car(car_, where_):
            pass
        else:
            print("Something didn't work")

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.board.cell_content(self.board.target_location()):
            print(self.board)
            self.__single_turn()
        print(self.board)
        print("You WIN")


if __name__ == "__main__":
    """update file location next line"""
    car_dict = load_json("C:\\Users\\פיזיקה\\PycharmProjects\\online_rush_hour\\car_config.json")
    print(car_dict)
    boardy = Board()
    game = Game(boardy)

    for carkey in car_dict:
        boardy.add_car(Car(carkey, car_dict[carkey][0], car_dict[carkey][1], car_dict[carkey][2]))

    # Your code here
    # All access to files, constructors, and such must be in this
    #  section, or in functions called from this section.
    play_game = Game(boardy)
    play_game.play()

"""
More Instructions:
    Make error printouts be a part of the game. For example, If the user tries to move a car off
        the board, then print out a message to the user telling them they can't do that. 
"""