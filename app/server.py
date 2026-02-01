import threading
from net import bind_and_listen, send_json, recv_json

HOST = "127.0.0.1"
PORT = 5000


def make_json(msg_type, text="", error=None):
    """Box up text into either error or text json. """
    if error is not None:
        return {"type": "error", "error": error}
    return {"type": msg_type, "text": text}

def handle_client(sock, addr):
    """Handle communication with aconnected client."""
    print("Client connected:", addr)
    try:
        while True:
            try:
                msg = recv_json(sock)
                if msg is None:
                    break  # clean disconnect
            except ValueError as e:
                err = str(e)
                if err not in ("invalid_json", "invalid_message", "invalid_length"):
                    err = "invalid_message"
                send_json(sock, make_json("error", error=err))
                continue
            except (ConnectionError, OSError):
                break # Stop on connection drop. 

            t = msg.get("type", "")
            if t == "chat": # Echo message back. 
                text = msg.get("text", "")
                send_json(sock, make_json("chat", text))
            elif t == "ping": # Reply ping request. 
                send_json(sock, {"type": "pong"})
            else: # Unknown message type. 
                print("Unknown msg type:", t, "from", addr)
                send_json(sock, make_json("error", error="unknown_type"))
    finally:
        try:
            sock.close()
        except Exception:
            pass
    print("Client closed:", addr)

def main():
    server = bind_and_listen(HOST, PORT)
    print(f"Listening on {HOST}:{PORT}")

    threads = []
    try:
        while True:
            # Accept new client connections.
            client_socket, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            t.start()
            threads.append(t)
    except KeyboardInterrupt:
        print("shutting down")
    finally:
        # Close the server and wait for threads to finish.
        try:
            server.close()
        except Exception:
            pass
        for t in threads:
            t.join(timeout=0.2)

if __name__ == "__main__":
    main()