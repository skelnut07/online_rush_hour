from car import Car
from helper import load_json
from board import Board
import socket
import json
import threading
from encryption import encrypt_message, decrypt_message

SERVER_IP = "127.0.0.1"
LISTENING_PORT = 50000

# Replace these with actual file paths to your JSON config files
DIFFICULTY_PATHS = {
    "easy": "C:\\Users\\ilans\\OneDrive\\Desktop\\me\\school\\final_project_cyber\\online_rush_hour\\easy_config.json",
    "medium": "C:\\Users\\ilans\\OneDrive\\Desktop\\me\\school\\final_project_cyber\\online_rush_hour\\medium_config.json",
    "hard": "C:\\Users\\ilans\\OneDrive\\Desktop\\me\\school\\final_project_cyber\\online_rush_hour\\hard_config.json"
}


class Game:
    """
    Game logic for a single player session
    """

    def __init__(self, board):
        """
        Initializes a Game object with a given board.
        :param board: Board object containing cars and grid layout
        """
        self.board = board

    def __recv_decrypted(self, client_socket):
        """
        Receives encrypted data from the client, decrypts it, and returns the decoded message.
        :param client_socket: socket object of the connected client
        :return: Decrypted string message from client
        """
        try:
            data = client_socket.recv(2048)
            if not data:
                raise ConnectionResetError("Client disconnected.")
            return decrypt_message(data)
        except Exception as e:
            print(f"Receive error: {e}")
            raise

    def __send_encrypted(self, client_socket, msg):
        """
        Encrypts and sends a message to the client.
        :param client_socket: socket object of the connected client
        :param msg: string message to be encrypted and sent
        """
        try:
            client_socket.send(encrypt_message(msg))
        except Exception as e:
            print(f"Send error: {e}")
            raise

    def __single_turn(self, client_socket):
        """
        Executes a single game turn: receives car selection and move direction from the client,
        validates and applies the move if possible.
        :param client_socket: socket object of the connected client
        """
        car_ = ""
        while car_ not in self.board.cars.keys():
            self.__send_encrypted(client_socket, "cm")
            car_ = self.__recv_decrypted(client_socket)
            print(f"Received car selection: {car_}")

            if car_ not in self.board.cars.keys():
                self.__send_encrypted(client_socket, "ERROR: Invalid car selection, please try again.")

        side = self.board.cars[car_].get_info()[2]
        where_ = ''
        while not ((side == 0 and where_ in ['u', 'd']) or (side == 1 and where_ in ['r', 'l'])):
            self.__send_encrypted(client_socket, "cd")
            where_ = self.__recv_decrypted(client_socket)
            print(f"Received direction: {where_}")

        if not self.board.move_car(car_, where_):
            print("Move failed.")

    def load_car_dict(self):
        """
        Returns a dictionary containing the current car configuration on the board.
        :return: dict mapping car name to [length, location, direction]
        """
        return {car.get_name(): car.get_info() for car in self.board.cars.values()}

    def play(self, client_socket):
        """
        Main gameplay loop for a single client. Sends board updates and receives moves until the game is won.
        :param client_socket: socket object of the connected client
        """
        try:
            while not self.board.cell_content(self.board.target_location()):
                print(self.board)
                msg = json.dumps(self.load_car_dict())
                self.__send_encrypted(client_socket, msg)
                self.__recv_decrypted(client_socket)  # Acknowledge
                self.__single_turn(client_socket)

            print("YOU WIN")
            self.__send_encrypted(client_socket, "W")
            self.__recv_decrypted(client_socket)  # Final acknowledgment
        except Exception as e:
            print(f"Connection error occurred during game: {e}")
        finally:
            client_socket.close()
            print("Client disconnected, socket closed.")


def handle_client(client_socket, client_address, difficulty_paths):
    """
    Handles a newly connected client: receives difficulty, loads board, and starts the game.
    :param client_socket: socket object representing the client
    :param client_address: tuple with client IP and port
    :param difficulty_paths: dictionary mapping difficulty names to JSON file paths
    """
    print(f"Connection established with {client_address}")
    try:
        client_socket.send(encrypt_message("Choose difficulty: easy, medium, hard"))
        difficulty = decrypt_message(client_socket.recv(1024)).strip().lower()

        while difficulty not in difficulty_paths:
            client_socket.send(encrypt_message("Invalid difficulty. Choose: easy, medium, hard"))
            difficulty = decrypt_message(client_socket.recv(1024)).strip().lower()

        config_path = difficulty_paths[difficulty]
        car_dict = load_json(config_path)

        boardy = Board()
        for carkey in car_dict:
            boardy.add_car(Car(carkey, *car_dict[carkey]))

        game = Game(boardy)
        game.play(client_socket)
        print(f"Game session with {client_address} ended.")

    except Exception as e:
        print(f"Connection error with {client_address}: {e}")
    finally:
        client_socket.close()
        print("Client disconnected, socket closed.")


def main():
    """
    Entry point for the server. Binds the socket, listens for clients, and spawns a thread for each new connection.
    """
    host = SERVER_IP
    port = LISTENING_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, DIFFICULTY_PATHS)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
