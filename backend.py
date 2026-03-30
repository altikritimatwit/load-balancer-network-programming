import socket
import threading
import sys

# Dummy backend server that would be replaced by real server 
# This server just echoes back the bytes sent to it
def handle(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", int(sys.argv[1])))
s.listen()


print(f"Backend listening on port {sys.argv[1]}")

while True:
    cs, addr = s.accept()

    handler_thread = threading.Thread(target=handle, args=(cs,))
    handler_thread.start()