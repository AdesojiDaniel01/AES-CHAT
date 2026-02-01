# Handles I/O functionality. 

import json
import struct
import socket

MAX_MSG = 1024 * 1024  # 1MB cap.




def connect(host, port):
    """Make a TCP client connection and return the socket."""
    s = socket.create_connection((host, port))
    return s

def bind_and_listen(host, port):
    """Create a server socket bound to host/port. Start listening."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(100)
    return server

def send_json(sock, obj):
    """Turn obj into json prefix with 4-byte length."""
    try:
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    except TypeError:
        raise ValueError("invalid_message")
    
    # Reject oversized messages.
    if len(payload) > MAX_MSG:
        raise ValueError("message_too_large")
    
    # Send length header followed by payload.
    header = struct.pack(">I", len(payload))
    sock.sendall(header + payload)


def recv_json(sock):
    """Read length header, then sent bytes, decode into a dict."""
    # Read 4-byte length header.
    try:
        header = _recv_all(sock, 4)
    except ConnectionError:
        # Client disconnected before sending data.
        return None
    
    length = int.from_bytes(header, "big")
    if length < 0 or length > MAX_MSG:
        raise ValueError("invalid_length")
    
    payload = _recv_all(sock, length)

    # Decode JSON string into object.
    try:
        obj = json.loads(payload.decode("utf-8"))
    
    except json.JSONDecodeError:
        raise ValueError("invalid_json")
    
    # Ensure object is a dictionary.
    if not isinstance(obj, dict):
        raise ValueError("invalid_message")
    
    return obj
    

def _recv_all(sock, n):
    """Read  n bytes from sock or raise error if disconnected."""
    # Continue reading until required number of bytes is received.
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Disconnected")
        buf.extend(chunk)
    return bytes(buf)
