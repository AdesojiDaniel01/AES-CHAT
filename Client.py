#!/usr/bin/env python3
"""
Simple chat client for the group project (Person 3 — Client)

Responsibilities:
  1) Connect to server
  2) Read stdin
  3) Send lines as chat messages (JSON framed: 4-byte length + UTF-8 JSON)
  4) Display server replies
  5) Handle Ctrl+C (SIGINT) cleanly

Assumptions (per project brief):
  - HOST = "127.0.0.1", PORT = 5000 by default
  - Message shape: {"type": "chat", "txt": "..."}
  - net.py exposes: connect(host, port) -> socket, send_json(sock, obj), recv_json(sock) -> obj

Usage:
  python client.py [--host 127.0.0.1] [--port 5000]

This file intentionally keeps all wire-format details in net.py.
"""
from __future__ import annotations

import argparse
import sys
import threading
import signal
import socket
from contextlib import suppress

# Import helpers provided by Person 1 (Networking)
# These functions are expected to exist in net.py as per the shared assumptions.
import net

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


def pretty_print_from_server(msg: dict) -> None:
    """Render messages from the server in a friendly way.

    Expected echo server behavior:
      - If type == "chat": echo back the text
      - Otherwise: {"type": "error", "text": "unknown"}
    """
    if not isinstance(msg, dict):
        print(f"[server] (non-dict) {msg}")
        return

    mtype = msg.get("type")
    if mtype == "chat":
        print(f"[server] {msg.get('txt', '')}")
    elif mtype == "error":
        # The server spec says: send back {"type": "error", "text": "unknown"}
        # Some implementations might use "txt"; show either if present.
        print(f"[server error] {msg.get('text') or msg.get('txt') or 'unknown error'}")
    else:
        print(f"[server] (unhandled type={mtype!r}) {msg}")


def recv_loop(sock: socket.socket, stop_evt: threading.Event) -> None:
    """Continuously receive JSON messages from the server and display them."""
    try:
        while not stop_evt.is_set():
            try:
                msg = net.recv_json(sock)  # blocks until a framed JSON msg arrives
                if msg is None:
                    # Treat None as closed connection
                    print("[client] server closed the connection")
                    break
                pretty_print_from_server(msg)
            except (ConnectionResetError, BrokenPipeError):
                print("[client] connection reset by peer")
                break
            except OSError as e:
                # Likely due to shutdown during exit
                if not stop_evt.is_set():
                    print(f"[client] recv error: {e}")
                break
            except Exception as e:  # keep client resilient to unexpected payloads
                print(f"[client] failed to parse/display server message: {e}")
                # continue receiving further messages
    finally:
        stop_evt.set()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simple JSON-framed chat client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port (default: 5000)")
    args = parser.parse_args(argv)

    stop_evt = threading.Event()

    try:
        sock = net.connect(args.host, args.port)
    except Exception as e:
        print(f"[client] failed to connect to {args.host}:{args.port}: {e}")
        return 2

    print(f"[client] connected to {args.host}:{args.port}\nType messages and press Enter to send. Ctrl+C to quit.")

    # Receiver thread prints all messages coming from server
    receiver = threading.Thread(target=recv_loop, args=(sock, stop_evt), daemon=True)
    receiver.start()

    # Handle Ctrl+C: set the stop flag and close the socket to unblock threads
    def handle_sigint(signum, frame):
        print("\n[client] Ctrl+C received, shutting down...")
        stop_evt.set()
        with suppress(Exception):
            # Half-close to wake up any pending operations
            sock.shutdown(socket.SHUT_RDWR)
        with suppress(Exception):
            sock.close()

    # Register signal handler (works on Unix; on Windows it still maps Ctrl+C)
    signal.signal(signal.SIGINT, handle_sigint)

    # Send loop: read from stdin and send as chat messages
    try:
        for line in sys.stdin:
            if stop_evt.is_set():
                break
            txt = line.rstrip("\n")
            if not txt:
                # skip empty lines to keep the UX clean; remove if you want to send empties
                continue
            try:
                net.send_json(sock, {"type": "chat", "txt": txt})
            except (BrokenPipeError, ConnectionResetError):
                print("[client] connection closed while sending")
                break
            except OSError as e:
                print(f"[client] send error: {e}")
                break
    except KeyboardInterrupt:
        # Redundant due to signal handler, but keeps UX clean if stdin reading is interrupted
        pass
    finally:
        stop_evt.set()
        with suppress(Exception):
            sock.shutdown(socket.SHUT_RDWR)
        with suppress(Exception):
            sock.close()
        # Give receiver a moment to exit gracefully
        receiver.join(timeout=0.5)
        print("[client] disconnected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
