import socket
import sys
from time import sleep


class Client:
    CONNECT_TIMEOUT = 1.0
    RECEIVE_TIMEOUT = 1.0
    RECONNECT_DELAY = 1.0

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.connected = False

    def connect_and_listen(self) -> None:
        print('Connecting: {}:{}'.format(self.host, self.port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(Client.CONNECT_TIMEOUT)
            sock.connect((self.host, self.port))
            self.connected = True
            print('Connected')
        except socket.error as err:
            print('Error: {}'.format(err), file=sys.stderr)
        finally:
            sock.close()
            self.connected = False
        print('Disconnected (RECONNECT_DELAY: {}s)'.format(Client.RECONNECT_DELAY))
        sleep(Client.RECONNECT_DELAY)
