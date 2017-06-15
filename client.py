#!/usr/bin/python3

import socket
import time
import threading


class Client:
    def __init__(self, host, port, username, talker):
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.username = username
        self.talker = talker
        self.login()

    def login(self):
        login_info = "Login:%s" % self.username
        talk_info = "Talk:%s" % self.talker
        self.sock.send(login_info.encode("utf-8"))
        time.sleep(2)
        self.sock.send(talk_info.encode("utf-8"))

    def write(self):
        while True:
            msg = input("Talk to %s:" % self.talker)
            data = msg.encode("utf-8")
            if msg == "!exit":
                self.sock.sendall(data)
                self.sock.close()
                return
            self.sock.sendall(data)

    def receive(self):
        while True:
            time.sleep(1)
            data = self.sock.recv(512)
            if not data:
                continue
            print("from %s: %s" % (self.talker, data.decode("utf-8")))

    def run(self):
        w = threading.Thread(target=self.write, args=())
        r = threading.Thread(target=self.receive, args=())
        w.start()
        r.start()

if __name__ == "__main__":
    username = input("Enter your username: ")
    talker = input("Chat to: ")
    client = Client("127.0.0.1", 50000, username, talker)
    client.run()
