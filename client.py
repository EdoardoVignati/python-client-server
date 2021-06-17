#!/usr/bin/python3
import socket
import threading
from signal import signal, SIGINT
import pickle
from tkinter import *

host = "localhost"  # input("Host: ")
port = 5000  # int(input("Port: "))

exit_event = threading.Event()
sock = None
text = None
values = []


def quit(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting gracefully\n")
    exit_event.set()
    sys.exit(0)


def receive(connection_socket, sig):
    while sig:
        try:
            data = connection_socket.recv(2048)
            ack = "\nServer received: {}".format(pickle.loads(data))
            print(ack)
            text.insert("1.0", ack)
            if exit_event.is_set():
                return
        except:
            print("You have been disconnected from the server\n")
            return


def send_data_via_btn():
    out_list = []
    for v in values:
        cur_val = v.get(1.0, "end-1c")
        if len(cur_val) == 0:
            continue
        try:
            out_list.append(float(cur_val))
        except:
            pass
    sock.sendall(pickle.dumps(out_list))


def client_gui():
    global text
    window = Tk()
    window.title("Client")
    window.geometry('500x300')
    Label(text="Please put up to 5 float").pack()
    values.append(Text(window, height=1, width=20, ))
    values.append(Text(window, height=1, width=20))
    values.append(Text(window, height=1, width=20))
    values.append(Text(window, height=1, width=20))
    values.append(Text(window, height=1, width=20))
    for v in values:
        v.pack()

    btn = Button(window, text="Send data", command=send_data_via_btn)
    btn.pack()

    text = Text(window, height=10)
    text.pack()
    window.mainloop()


if __name__ == "__main__":
    signal(SIGINT, quit)
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
