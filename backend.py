import socket
import threading
import sys

def handle(conn):
    with conn:
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            conn.sendall(chunk)

def run(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()
        print(f"Backend listening on port {port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

port = int(sys.argv[1])
run(port)