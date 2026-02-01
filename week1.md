Shared assumptions:
Host / Port:
	HOST = "127.0.0.1", PORT = 5000
	Message shape: {"type": "chat", "txt": "string, in utf-8 format"}
	Framing: 4-byte length + UTF-8 json. 
	**net.py should hold all the logic for string handling. 


Person 1 — Networking

	Fills out: net.py

	Implement:
		connect, bind_and_listen, send_json, recv_json work 
		*No cryptography, just need to be able to first send basic messages.

	Potentially add a small test in tests. Have it send and recv round trip.

Person 2 — Server

	Fills out: server.py

	Build accept loop.
		1) Can accept client connection with bind_and_listen(HOST, PORT)
		2) Read messages handle_client(sock,addr).
			If type=="chat" then echo. 
			Otherwise, send back { "type": "error", "text", "unknown" } 

		-prints connect / disconnect.
		2) Later, needs threading added so can accept multiple clients.
	
	Use net.py helpers for send/recv. 
		I created stubs for what the assumed structure for these methods will be.

	print messages back to the client (echo)

Person 3 — Client

	Fills out: client.py

		1) Connect to server.
		2) read stdin
		3) send lines as chat messages
		4) Display server replies
		5) Handle ctrl+c cleanly. Aka, picks up on ctrl+c command and exits cleanly.

Person 4 — Crypto

	Fills out Crypto: Diffie–Hellman key exchange
	dh_keypair -- returns (priv, pub)
	dh_shared -- returns shared bytes
	kdf -- returns (enc_key, mac_key)

	Implement DH so both sides can compute the same shared key later.



Workflow for this week:

1) everyone makes their own venv

2) Everyone makes their own branch, and commits that branch.
	-for simplicity, let's have everyone initially create their own branch for all work you do. 
	
	
 
3) Once your section is finished, push it to your branch. 
	-when you commit and push to integrate with everyone else's stuff
	 create a pull request to get it merged into develop. 
	-DO NOT push to main. Push the pull request to develop. 

4) I'll go through and check out the pull requests to see if they are ready to be merged into develop. 

	-as we are all on different time lines, if you need someone else's code, you can use git to pull another branch's code into
	your own current branch. Merge the two before pushing back and trying to create pull request to add back into develop. 



