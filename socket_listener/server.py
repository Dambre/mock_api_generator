import asyncore
import ast
import json

from logger import getLogger
from listener.urls import validate_post_data as validate

logger = getLogger(__name__, 'logs/socket_listener.log')

HOST = 'localhost'
PORT = 9998


class MessagesHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(4096).strip().decode('utf-8')
        logger.debug('{} from {}'.format(data, self.addr))
        if data:
            try:
                length, data = data.split('#')
            except ValueError:
                return

            try:
                data = ast.literal_eval(data)
                message = '{}\n'.format(
                    json.dumps(validate(data))
                )

            except (SyntaxError, ValueError):
                message = {
                    "success": False,
                    "error": "Invalid data provided"
                }

            length = len(str(message))
            message = '{}#{}'.format(length, message)
            self.send(message.encode())


class MessagesServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = MessagesHandler(sock)


def run_server(host=HOST, port=PORT):
    server = MessagesServer(host, port)
    asyncore.loop()


if __name__ == '__main__':
    run_server()
