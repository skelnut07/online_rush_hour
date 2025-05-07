from car import Car
from helper import load_json
from board import Board
import socket
import json
import threading

SERVER_IP = "192.168.1.168"
LISTENING_PORT = 50000
CONFIG_PATH = "C:\\Users\\ilans\\OneDrive\\Desktop\\me\\school\\final_project_cyber\\online_rush_hour\\car_config.json"

class Game:
    """
    Game logic for a single player session
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type Board
        """
        self.board = board

    def __single_turn(self, client_socket):
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
            print("Something didn't work")

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
                client_socket.send(msg.encode('utf-8'))
                client_socket.recv(1024)  # Receive acknowledgment
                self.__single_turn(client_socket)
            print("YOU WIN")
            client_socket.send("W".encode())
            client_socket.recv(1024)  # Receive final acknowledgment
            print(self.board)
        except (ConnectionResetError, BrokenPipeError, socket.error) as e:
            print(f"Connection error occurred: {e}")
        finally:
            client_socket.close()
            print("Client disconnected, socket closed.")


def handle_client(client_socket, client_address, car_dict):
    print(f"Connection established with {client_address}")
    boardy = Board()
    for carkey in car_dict:
        boardy.add_car(Car(carkey, car_dict[carkey][0], car_dict[carkey][1], car_dict[carkey][2]))

    game = Game(boardy)
    game.play(client_socket)
    print(f"Game session with {client_address} ended.")


if __name__ == "__main__":
    car_dict = load_json(CONFIG_PATH)

    host = SERVER_IP
    port = LISTENING_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client,args=(client_socket, client_address, car_dict))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()
