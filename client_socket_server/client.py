import socket
from listener.validators.messages import messages
from generator import Generate

# set server address
HOST = 'localhost'
PORT = 4000


def run_client(host=HOST, port=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            message = str(messages_pick_and_generate())
            message = '{}#{}'.format(len(message), message)
            sock.sendall(message.encode())

            print('Sent data:\n{}'.format(message))
            received = sock.recv(4096).strip().decode('utf-8')

            print('Received data:\n{}'.format(received))


def messages_pick_and_generate():
    while True:
        msg_id = input('Enter msgId: ')
        message = messages.get(msg_id, {})
        if message:
            msg = message['request']
            data = Generate().get_data(msg)
            data['msgId'] = msg_id
            return data

        print('Incorrect msgId. Available msgIds:\n')
        for msg_id in messages.keys():
            print(msg_id)
