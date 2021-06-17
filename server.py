#!/usr/bin/python3
import socket
import threading
import pickle
from tkinter import Tk, Text

connections = []
total_connections = 0
text = None


class Client(threading.Thread):
    def __init__(self, client_socket, client_address, client_id, client_name, client_signal):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.client_id = client_id
        self.client_name = client_name
        self.client_signal = client_signal

    def __str__(self):
        return str(self.client_id) + " " + str(self.client_address)

    def run(self):
        while self.client_signal:
            try:
                data = self.client_socket.recv(2048)
                if not data:
                    raise Exception("Client sent empty packet. Exiting.")
            except Exception:
                print("Client " + str(self.client_address) + " has disconnected")
                self.client_signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID {}: {}".format(self.client_id, pickle.loads(data)))
                text.insert("1.0", "ID {}: {}\n".format(self.client_id, pickle.loads(data)))
                for client in connections:
                    client.client_socket.sendall(data)


def new_connection(new_socket):
    while True:
        sock, address = new_socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def server_gui():
    global text
    window = Tk()
    window.title("Server")
    window.geometry('500x300')
    text = Text(window, height=10)
    text.pack()
    window.mainloop()


if __name__ == "__main__":
    host = "localhost"  # input("Host: ")
    port = 5000  # int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    new_connections_thread = threading.Thread(target=new_connection, args=(sock,))
    new_connections_thread.start()

    server_gui()  # If you remove the gui call, the process runs in terminal
