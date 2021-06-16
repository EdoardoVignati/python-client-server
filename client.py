#!/usr/bin/python3
import socket
import threading
import sys
from signal import signal, SIGINT

exit_event = threading.Event()


def quit(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting gracefully\n")
    exit_event.set()
    exit(0)


def receive(connection_socket, sig):
    while sig:
        try:
            data = connection_socket.recv(32)
            print("\nServer received: {}".format(str(data.decode("utf-8"))))
            if exit_event.is_set():
                return
        except:
            print("You have been disconnected from the server\n")
            return


if __name__ == "__main__":
    signal(SIGINT, quit)
    host = input("Host: ")
    port = int(input("Port: "))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Could not make a connection to the server\n")
        sys.exit(1)

    receive_thread = threading.Thread(target=receive, args=(sock, True))
    receive_thread.start()

    values = [3.14, 42.0, 10.12, 12.94]
    i = 0
    while i < len(values):
        message = str(values[i])
        input("Click to send {} ...\n".format(message))
        sock.sendall(str.encode(message))
        i += 1
    sock.close()
    exit_event.set()
    receive_thread.join()
    sys.exit(0)
