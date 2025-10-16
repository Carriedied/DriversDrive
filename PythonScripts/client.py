import socket

HOST = "10.190.130.243"
PORT = 65432



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    data = client.recv(1024)
    print(data.decode('utf-8'))