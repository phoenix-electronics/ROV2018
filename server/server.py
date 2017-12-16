import socket
import sys

from common.protocol import recv_obj, send_obj


class Server:
    ACK_TIMEOUT = 0.2
    CLOSE_DELAY = 0.1

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_server(self) -> None:
        host = self.host
        port = self.port
        sock = self.sock
        sock.bind((host, port))
        sock.listen(1)
        print('Server started: {}:{}'.format(host, port))
        while True:
            self.handle_connection()

    def handle_connection(self) -> None:
        sock = self.sock
        try:
            conn, addr = sock.accept()
            print('     Connected: {}'.format(addr[0]))
            msg = "Test message"
            send_obj(conn, msg)
            resp = recv_obj(conn, Server.ACK_TIMEOUT)
            print(resp)
            print('  Disconnected.')
        except socket.error as err:
            print('  Disconnected: {}'.format(err), file=sys.stderr)
