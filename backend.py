import socket
import threading
import sys
import time

# Dummy backend that simulates a real server
# This server just echoes back the bytes sent to it by the client
def handle(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        time.sleep(4) # Simulate some processing time
        print(f"Message from Client received: {data.decode()}")
        conn.sendall(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", int(sys.argv[1])))
s.listen()


print(f"Backend listening on port {sys.argv[1]}")

while True:
    # Accepts a client and handles it in a new thread
    cs, addr = s.accept()

    handler_thread = threading.Thread(target=handle, args=(cs,))
    handler_thread.start()