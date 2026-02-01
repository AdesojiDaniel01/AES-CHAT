1) Server / Client talking
Get a simple echo working over TCP. one sends a line, the other sends it back.
net.py = connect, listen, send/recv helpers
server.py = accept clients, echo messages back
client.py = connect, read stdin, print replies

2) Add encryption (single key)
Hardcode a test key. Encrypt on send. Decrypt on receive.
sever.py = call encrypt before send, decrypt after recv
client.py = call encrypt before send, decrypt after recv

3) Share the key properly
Add a simple key exchange (Diffie–Hellman) so both sides get a fresh shared key.
crypto.py = diffie-hellmen key exchange
server & client = add handshake before chat loop. Store shared key.

4) Protect against tampering
Add a message tag so changed data gets rejected.
crypto.py: HMAC function
server / client: add tag when sending, check tag when recieving. 

5) Tighten the basics
Add timeouts, size limits, and clear error messages. Handle disconnects cleanly.
net.py: add frame size check / socket timeouts
server.py: catch disconnects / ctrl+c
client.py: handle disconnects cleantly


6) Small GUI 
A tiny window to connect, send, and show messages.
gui.py: tkinter window to send / recv.