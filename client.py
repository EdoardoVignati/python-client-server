#!/usr/bin/python3
import socket
import threading
from signal import signal, SIGINT
import pickle
from tkinter import *

exit_event = threading.Event()
sock = None
text = None
values = [3.14, 42.0, 10.12, 12.94]


def quit(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting gracefully\n")
    exit_event.set()
    sys.exit(0)


def receive(connection_socket, sig):
    while sig:
        try:
            data = connection_socket.recv(2048)
            print("\nServer received: {}".format(pickle.loads(data)))
            if exit_event.is_set():
                return
        except:
            print("You have been disconnected from the server\n")
            return


def send_data_via_btn():
    sock.sendall(pickle.dumps(values))
    text.insert("1.0", str(values) + "\n")


def client_gui():
    global text
    window = Tk()
    window.title("Client")
    window.geometry('500x300')
    btn = Button(window, text="Send data", command=send_data_via_btn)
    btn.pack()
    text = Text(window, height=10)
    text.pack()
    window.mainloop()


if __name__ == "__main__":
    signal(SIGINT, quit)
    host = "localhost"  # input("Host: ")
    port = 5000  # int(input("Port: "))

    max_tries = 10

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Could not make a connection to the server\n")
        sys.exit(1)

    receive_thread = threading.Thread(target=receive, args=(sock, True))
    receive_thread.start()

    client_gui()  # If you remove the gui call, the process runs in terminal
    i = 0
    while i < max_tries:
        input("Press Enter to send {} ...\n".format(values))
        sock.sendall(pickle.dumps(values))
        i += 1
    sock.close()
    exit_event.set()
    receive_thread.join()
    sys.exit(0)
