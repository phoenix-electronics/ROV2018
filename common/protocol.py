import pickle
import socket
import struct
from select import select
from typing import Union

from common.timer import Timer


def send_obj(sock: socket, obj: object) -> None:
    """Write a length-delimited serialized object to the socket"""
    data = pickle.dumps(obj)
    sock.sendall(struct.pack('!I', len(data)))
    sock.sendall(data)


def recv_obj(sock: socket, timeout: Union[Timer, float]) -> object:
    """Read a length-delimited serialized object from the socket, or raise socket.error if the timeout is exceeded"""
    timer = timeout if isinstance(timeout, Timer) else Timer(timeout)
    len_data = recv_len(sock, 4, timer)
    length, = struct.unpack('!I', len_data)
    obj_data = recv_len(sock, length, timer)
    return pickle.loads(obj_data)


def recv_avail(sock: socket, timeout: float = 0) -> bool:
    """Return whether the socket has data available for reading, either immediately or before a timeout"""
    return len(select([sock], [], [], timeout)[0]) != 0


def recv_len(sock: socket, length: int, timeout: Union[Timer, float]) -> bytes:
    """Read an exact number of bytes from the socket, or raise socket.error if the timeout is exceeded"""
    timer = timeout if isinstance(timeout, Timer) else Timer(timeout)
    buffer = bytearray()
    while len(buffer) < length and not timer.is_expired():
        if recv_avail(sock, timer.get_remaining_time()):
            buffer += sock.recv(length - len(buffer))
    if len(buffer) != length:
        raise socket.error('timed out')
    return buffer
