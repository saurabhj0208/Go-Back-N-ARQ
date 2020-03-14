PROJECT:-
Go-Back-N ARQ scheme

TEAM MEMBERS:-
Abhilasha Saini
Saurabh Joshi

PYTHON VERSION REQUIRED:-
python 2.7


Before executing the following steps, make sure input file(here dummy.txt) is in same directory as the client.py 

STEPS - FOR SERVER SIDE:-
1. Open command prompt and go the directory of 'server.py' file.
2. Execute the following command:

	python server.py <port> <filename> <probability>

	here, <port> = port number at which server is running.
		  <filename> = output file to be created or written into. 
		  <probability> = probability with which client is sending the packet.

	Output file will be created in the same directory as server.py

STEPS - FOR CLIENT SIDE:-
1. Open command prompt and go the directory of 'client.py' file.
2. Execute the following command:
	
	python client.py <host> <port> <filename> <N> <MSS>

	here, <host> = IP address of server can be given as host. If running on same computer, use "localhost" in place of <host>
		  <filename> = input file to be sent
		  <N> = Window size
		  <MSS> = Maximum segment size

Example:-
	In server terminal = python server.py 7735 output.txt 0.05
	In client terminal = python client.py localhost 7735 input.txt 64 500


