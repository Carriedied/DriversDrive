import socket
import json

HOST = "10.190.130.243"
PORT = 65432

m = {
  "status": "success",
  "data": [
    {
      "ip": "192.168.1.10",
      "hostname": "PC-01",
      "devices": [
        {
          "name": "NVIDIA GeForce RTX 3060",
          "driver_status": "missing",
          "driver_url": "https://example.com/driver.exe"
        }
      ]
    }
  ]
}

jsonObj = json.dumps(m)


data = jsonObj


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()



ip = socket.gethostbyname(socket.getfqdn())
print(ip)

while True:
    conn, addr = server.accept()

    print("Connected by", addr)
    conn.sendall(bytes(data, encoding="utf-8"))

