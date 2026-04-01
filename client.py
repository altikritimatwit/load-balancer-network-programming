import socket

HOST = '127.0.0.1'
PORT = 8080 # Load Balancer port

def send_message():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    message = input("Enter message to send to backend: ")
    s.sendall(message.encode())
    response = s.recv(1024)
    print(f"Backend sent: {response.decode()}")
    s.close()

# Sequentially sends messages to Load Balancer
# Demonstrates round-robin
print("--- Sequential Client ---")
i = 1
while True:
    print(f"Sending message #{i}")
    send_message()
    i += 1