import socket 
import threading 

def forward(client_socket, backend_socket):
    while True: 
        data = client_socket.recv(4096)

        if not data:
            break
        backend_socket.sendall(data)

def handle_connections(client_socket, backend_addr):
    backend_socket = socket.create_connection(backend_addr)

    direc1 = threading.Thread(target=forward, args=(client_socket, backend_socket))

    direc1.start()
    direc2 = threading.Thread(target=forward, args=(backend_socket ,client_socket ))
    direc2.start()
    direc1.join()
    direc2.join()
    backend_socket.close()
    client_socket.close()