#!/usr/bin/python3
import socket
import threading

connections = []
total_connections = 0


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
                data = self.client_socket.recv(32)
                if not data:
                    raise Exception("Client sent empty packet. Exiting.")
            except Exception:
                print("Client " + str(self.client_address) + " has disconnected")
                self.client_signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.client_id) + ": " + str(data.decode("utf-8")))
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


if __name__ == "__main__":
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    new_connections_thread = threading.Thread(target=new_connection, args=(sock,))
    new_connections_thread.start()
