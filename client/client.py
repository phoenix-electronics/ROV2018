import socket
import sys

from common.protocol import recv_obj, send_obj


class Client:
    MSG_TIMEOUT = 0.1
    RETRY_DELAY = 0.1

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Client.MSG_TIMEOUT)

    def connect_and_listen(self) -> None:
        host = self.host
        port = self.port
        sock = self.sock
        print('  Connecting: {}:{}'.format(host, port))
        try:
            sock.connect((host, port))
            while True:
                msg = recv_obj(sock, Client.MSG_TIMEOUT)
                print(msg)
                send_obj(sock, msg)
        except socket.error as err:
            print('Disconnected: {}'.format(err), file=sys.stderr)
        finally:
            sock.close()
