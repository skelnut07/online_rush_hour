import socket
import json
from encryption import encrypt_message, decrypt_message

# Shared secret key (use same key in both client and server)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 50000

BOARDSIZE = 7


def get_car_coords(location, direction, length):
    """
    Parameters:
        location (tuple): The starting coordinate of the car's head (row, col).
        direction (int): Orientation of the car (0 for vertical, 1 for horizontal).
        length (int): Number of cells the car occupies.

    Returns:
        list of tuple: A list of all coordinates occupied by the car based on its starting location and direction.
    """
    cords = []
    y = location[0]
    x = location[1]
    if direction == 0:
        for _ in range(length):
            cords.append((y, x))
            y += 1
    else:
        for _ in range(length):
            cords.append((y, x))
            x += 1
    return cords


def board_coordinates():
    """
    Returns:
        set of tuple: All valid coordinates on the 7x7 game board,
                      including the special exit cell at (3, 7).
    """
    cords = set()
    for col in range(BOARDSIZE):
        for lin in range(BOARDSIZE):
            cords.add((col, lin))
    cords.add((BOARDSIZE // 2, BOARDSIZE))
    return cords


def create_starter_board():
    """
    Returns:
        list of list of str: A 2D list representing the game board with "_"
                             for empty spaces and an extra cell at (3, 7).
    """
    board = []
    for _ in range(BOARDSIZE):
        board.append(["_" for _ in range(BOARDSIZE)])
    board[BOARDSIZE // 2].append("_")
    return board


def add_car(board, carkey, car_info, cars):
    """
    Parameters:
        board (list of list): The current board layout.
        carkey (str): The car's identifying letter.
        car_info (list): [length, [row, col], direction]
        cars (dict): Dictionary of current cars on the board.

    Returns:
        tuple: Updated board and cars dictionary after adding the new car
               (if the location is valid and unoccupied).
    """
    cords = get_car_coords(car_info[1], car_info[2], car_info[0])
    board_cords = board_coordinates()
    if all(coord in board_cords for coord in cords) and all(board[y][x] == "_" for y, x in cords):
        for y, x in cords:
            board[y][x] = carkey
        cars[carkey] = car_info
    return board, cars


def load_board_(cars_dict):
    """
    Parameters:
        cars_dict (dict): A dictionary with car keys and their info
                          [length, [row, col], direction].

    Returns:
        list of list: A 2D list representing the game board with all cars placed on it.
    """
    board = create_starter_board()
    current_cars = {}
    for carkey in cars_dict:
        board, current_cars = add_car(board, carkey, cars_dict[carkey], current_cars)
    return board


def start_client(host=SERVER_IP, port=SERVER_PORT):
    """
    Parameters:
        host (str): IP address of the server (default is localhost).
        port (int): Port to connect to (default is 50000).

    This function starts the client, connects to the server,
    handles encrypted communication, manages the game loop
    (difficulty selection, car moves), and displays the board.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("""Welcome!
    Pick your car by writing down the letter it is shown as,
    Pick direction to move with u,d,r,l
    """)

    try:
        # Receive and respond to difficulty prompt
        difficulty_prompt = decrypt_message(client_socket.recv(4096))
        print(difficulty_prompt)
        difficulty = input("Enter difficulty (easy/medium/hard): ").strip().lower()
        client_socket.send(encrypt_message(difficulty))

        # Loop until valid difficulty is accepted by server
        while True:
            response = decrypt_message(client_socket.recv(4096))
            if response.startswith("Invalid difficulty"):
                print(response)
                difficulty = input("Enter difficulty (easy/medium/hard): ").strip().lower()
                client_socket.send(encrypt_message(difficulty))
            else:
                # Proceed to game
                msg = response
                break

        while True:
            if msg == "W":
                print("YOU WIN")
                break
            elif msg == "cm":
                response = input("Which car do you want to move? ")
                client_socket.send(encrypt_message(response))
            elif msg == "cd":
                response = input("What direction do you want to move it (u/d/l/r)? ")
                client_socket.send(encrypt_message(response))
            elif msg.startswith("ERROR"):
                print(msg)
                msg = decrypt_message(client_socket.recv(4096))
                continue
            else:
                car_data = json.loads(msg)
                board = load_board_(car_data)
                for row in board:
                    print(" ".join(row))
                client_socket.send(encrypt_message("received board"))

            # Receive next message
            msg = decrypt_message(client_socket.recv(4096))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()