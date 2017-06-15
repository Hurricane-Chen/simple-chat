import socket
import threading
import time


class Server:
    def __init__(self, listen_addr, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((listen_addr, port))
        self.sock.listen(5)

    def __del__(self):
        self.sock.close()

    def tcplink(self, new_sock, addr):
        print("New connection . . .", addr)
        new_sock.send(b"Roger. ")
        while True:
            data = new_sock.recv(512)
            print(data.decode("utf-8"))
            time.sleep(0.5)
            if data == "exit" or not data:
                break
            new_sock.send(b"Receive your message.")
        new_sock.close()
        print("Connection from ", addr, "closed")

    def run(self):
        while True:
            new_sock, addr = self.sock.accept()
            t = threading.Thread(target=self.tcplink, args=(new_sock, addr))
            t.start()

if __name__ == "__main__":
    serve = Server("127.0.0.1", 50000)
    serve.run()
