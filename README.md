# SimpleMessenger
A simple client-server messenger.

# Setup

In order to setup the project you will need to take the following steps:
- Change the IP adress in client_socket.py file to your public adress of the server (change the __HOST variable),
- If your server will be accessed via a router, setup port forwarding to redirect traffic on port 6889 to your server machine.

# Run

Have one machine be the server for the messenger, then you can have multiple other machines connected to it as clients, chatting with each other. To run the server run the server.py file. To run the client run client.py file.

# Note

There exists currently no easy way of creating new users. In order to create a new user you will need to modify login_window.py file, to include this line: print(login, password) in the login() method. You can then save the output in the following format: <login>,<password> to the logins.txt file and restart the server to include changes. Please note that the password is hashed so you will need to remember it.
