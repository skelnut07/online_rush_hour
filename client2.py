import socket
import json
from load_board import load_board_

SERVER_IP = "127.0.0.1"
SERVER_PORT = 64131


def start_client(host=SERVER_IP, port=SERVER_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("""Welcome!
    pick your car by writing down the letter it is shown as,
    pick direction to move with u,d,r,l
    """)

    while True:
        msg = client_socket.recv(2048)
        if msg.decode() == "W":
            break
        elif msg.decode() == "cm":
            response = input("which car do you want to move ")
            client_socket.send(response.encode())
        elif msg.decode() == "cd":
            response = input("what direction do you want to move it ")
            client_socket.send(response.encode())
        elif msg.decode()[:5] == "ERROR Something didn't work":
            print(msg)
            client_socket.send("Error received".encode())
        else:
            msg = msg.decode('utf-8')
            print('\n'.join(map(str, load_board_(json.loads(msg)))))
            client_socket.send("received board".encode())
    print("YOU WIN")
    client_socket.send("OVER".encode())
    client_socket.close()


if __name__ == "__main__":
    start_client()

# client_socket.send(msg.encode())
# msg = client_socket.recv(1024).decode()
# print(msg)
