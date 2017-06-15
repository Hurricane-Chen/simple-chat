import socket
import time

HOST = '127.0.0.1'    # The remote host
PORT = 50000              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    while True:
        s.sendall("今儿真高兴！".encode("utf-8"))
        time.sleep(2.5)
    data = s.recv(512)
print('Received', repr(data))