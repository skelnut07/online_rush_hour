import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1212


def start_client(host=SERVER_IP, port=SERVER_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = "Hello from client!"
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    print(f"Received from server: {response}")

    client_socket.close()


if __name__ == "__main__":
    start_client()
