# Client - Server architecture in Python

## Features

- Single server, multiple clients
- Send and receive float arrays
- An _ACK_ is sent to the client
- The server can manage the attachment or removal of clients at runtime
- Send data via GUI or via terminal

## How to use

- Open a terminal #1 (cmd, shell, bash,...)
- Start the server via terminal 1 (type: ``python server.py``)
- Open another terminal #2
- Start the client via  terminal #2 (type: ``python client.py``)
- Set some floats (up to 5)
- Send with the button

You can change host and port in client and server scripts if needed.

Automatically server and clients start on _localhost:5000_

## Libraries used

Python native libraries:

- socket
- threading
- pickle (data conversion)
- tkinter (GUI)
- signal

References: https://docs.python.org/3/library/index.html