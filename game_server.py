from car import Car
from helper import load_json
from board import Board
import socket
import json

LISTENING_PORT = 64131


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

    def __single_turn(self, client_socket):
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
        car_ = ""
        while car_ not in self.board.cars.keys():
            print("which car do you want to move? Choose one of the available cars.")
            client_socket.send("cm".encode())
            car_ = client_socket.recv(1024).decode()
            print(f"Received from client: {car_}")

            if car_ not in self.board.cars.keys():
                error_message = "ERROR: Invalid car selection, please try again."
                client_socket.send(error_message.encode())

        side = self.board.cars[car_].get_info()[2]
        where_ = ''
        while not ((side == 0 and where_ in ['u', 'd']) or (side == 1 and where_ in ['r', 'l'])):
            print(f"Invalid direction for car {car_}. Try again.")
            client_socket.send("cd".encode())
            where_ = client_socket.recv(1024).decode()
            print(f"Received from client: {where_}")

        if not self.board.move_car(car_, where_):
            error_message = "ERROR: Invalid move attempt. Try again."
            print(error_message)
            client_socket.send(error_message.encode())

    def load_car_dict(self):
        car_dict_ = {}
        for car in self.board.cars:
            car_dict_[self.board.cars[car].get_name()] = self.board.cars[car].get_info()
        return car_dict_

    def play(self, client_socket):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        try:
            while not self.board.cell_content(self.board.target_location()):
                print(self.board.cell_content(self.board.target_location()))
                print(self.board)
                msg = json.dumps(self.load_car_dict())
                print(msg)
                client_socket.send(msg.encode('utf-8'))
                print(msg)
                msg = client_socket.recv(1024).decode()
                print(msg)
                self.__single_turn(client_socket)

            print("YOU WIN")
            client_socket.send("W".encode())
            msg = client_socket.recv(1024).decode()
            print(msg)
            print(self.board)

        except (ConnectionAbortedError, socket.error) as e:
            print(f"Connection error: {e}")
        finally:
            client_socket.close()
        # while not self.board.cell_content(self.board.target_location()):
        #     print(self.board.cell_content(self.board.target_location()))
        #     print(self.board)
        #     msg = json.dumps(self.load_car_dict())
        #     print(msg)
        #     client_socket.send(msg.encode('utf-8'))
        #     print(msg)
        #     msg = client_socket.recv(1024).decode()
        #     print(msg)
        #     self.__single_turn(client_socket)
        #
        #
        # print("YOU WIN")
        # client_socket.send("W".encode())
        # """WHAT NEEDS TO BE SENT: self.board.cars"""
        # msg = client_socket.recv(1024).decode()
        # print(msg)
        # print(self.board)


if __name__ == "__main__":
    """update file location next line"""
    car_dict = load_json("C:\\Users\\פיזיקה\\PycharmProjects\\online_rush_hour\\car_config.json")
    print(car_dict)
    boardy = Board()
    game = Game(boardy)

    for carkey in car_dict:
        boardy.add_car(Car(carkey, car_dict[carkey][0], car_dict[carkey][1], car_dict[carkey][2]))

    """launching server, connecting to client"""
    host = "127.0.0.1"
    port = LISTENING_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    play_game = Game(boardy)
    play_game.play(client_socket)

    client_socket.close()
    server_socket.close()
