import socket 
import threading 

def forward(src, dst):
    try:
        # Bytes forwarded from src to dst until src is closed
        while True: 
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        # Socket errors handled silently
        pass
    finally:
        # Basically tells dst to stop sending data to src
        # SHUT_WR means closed for writing
        try:
            dst.shutdown(socket.SHUT_WR)
        except:
            pass

def handle_connections(client_socket, backend_addr, backend_pool):
    # Ensuring backend is up and running before forwarding
    try:
        backend_socket = socket.create_connection(backend_addr)
    except Exception as e:
        client_socket.close()
        return
    
    # This is where bidirectional forwarding occurs
    # Two threads are spawned, for either direction of the connection
    # direc1 is client -> backend, while direc2 is backend -> client
    direc1 = threading.Thread(target=forward, args=(client_socket, backend_socket))
    direc1.start()
    direc2 = threading.Thread(target=forward, args=(backend_socket, client_socket))
    direc2.start()

    # Both direcs finish, and then we clean up
    direc1.join()
    direc2.join()

    # Connection count is decremented, after connection is closed
    add_key = f"{backend_addr[0]}:{backend_addr[1]}"
    with backend_pool.lock:
        backend_pool.connection_count[add_key] -= 1
    
    backend_socket.close()
    client_socket.close()