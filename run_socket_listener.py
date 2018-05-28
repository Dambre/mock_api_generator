activate_this = '/home/ubuntu/projects/CMFPythonMockServer/env/bin/activate_this.py'
try:
    exec(open(activate_this).read(), dict(__file__=activate_this))
except FileNotFoundError:
    pass


from logger import getLogger
from socket_listener import server


logger = getLogger('run_socket_listener.py', 'logs/socket_listener.log')

HOST = '0.0.0.0'
PORT = 3005


if __name__ == '__main__':
    message = 'Socket server running on {}:{}'.format(HOST, PORT)
    logger.info(message)
    print(message)
    server.run_server(HOST, PORT)
