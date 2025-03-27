import socket

LISTENING_PORT = 1212


def start_server(host='127.0.0.1', port=LISTENING_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    data = client_socket.recv(1024).decode()
    print(f"Received from client: {data}")

    response = "Hello from server!"
    client_socket.send(response.encode())

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()
