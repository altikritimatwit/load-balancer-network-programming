import socket

HOST = '127.0.0.1'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(b'Hello from Mina')
print(s.recv(1024))

s.close()