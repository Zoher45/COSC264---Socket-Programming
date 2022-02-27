# COSC264---Socket-Programming

This socket programming is implemented using the TCP protocol. First, run the server and then the client. The file is requested by the client, which is located on the server-side. If the request is successful the requested file should appear in the client directory.

Running the server-side
1) First open terminal and direct to the server.py file 
2) To run the server, a port number must be provided (ranging from 1025 to 64000)
3) Run the following command - python server.py 5000
4) The Server will then be waiting for a request from the client-side

Running the client-side
1) First open terminal and direct to the client.py file 
2) To run the client IP, port number and file parameters must be passed respectively
3) Run the following command - python client.py localhost 5000 'Test File.txt'
