from client_socket_server import client

# Set to same as the socket listener server
HOST = 'localhost'
PORT = 3005


if __name__ == '__main__':
    try:
        client.run_client(HOST, PORT)
    except ConnectionRefusedError:
        print('First start the socket '\
            'listener server\nor\nset correct HOST and PORT.')
