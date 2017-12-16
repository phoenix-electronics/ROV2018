import pickle
import socket
import struct
from select import select
from typing import Union

from common.timer import Timer


def send_obj(sock: socket, obj: object) -> None:
    data = pickle.dumps(obj)
    sock.sendall(struct.pack('!I', len(data)))
    sock.sendall(data)


def recv_obj(sock: socket, timeout: Union[Timer, float]) -> object:
    timer = timeout if isinstance(timeout, Timer) else Timer(timeout)
    len_data = recv_len(sock, 4, timer)
    length, = struct.unpack('!I', len_data)
    obj_data = recv_len(sock, length, timer)
    return pickle.loads(obj_data)


def recv_len(sock: socket, length: int, timeout: Union[Timer, float]) -> bytes:
    timer = timeout if isinstance(timeout, Timer) else Timer(timeout)
    buffer = bytearray()
    while len(buffer) < length and not timer.is_expired():
        select([sock], [], [], timer.get_remaining_time())
        buffer += sock.recv(length - len(buffer))
    if len(buffer) != length:
        raise socket.error('timed out')
    return buffer
