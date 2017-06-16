#!/usr/bin/python3

import socket
import threading
import time


class Server:
    def __init__(self, listen_addr, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((listen_addr, port))
        self.sock.listen(15)
        self.buffer = {}
        self.buffer_lock = threading.Lock()

    def __del__(self):
        self.sock.close()

    def handler(self, new_sock, addr):
        print("New connection . . .", addr)
        login_info = new_sock.recv(36)
        login_info = login_info.decode("utf-8")
        talk_to = new_sock.recv(36)
        talk_info = talk_to.decode("utf-8")
        print(login_info, " ", talk_info)
        if not login_info.startswith("Login:") or not talk_info.startswith("Talk:"):
            print("incorrect login format")
            new_sock.close()
            return
        username = login_info[6:-1]
        talker = talk_info[5:-1]
        self.buffer[username] = []
        print("user: %s login, talk to: %s" % (username, talker))
        rec_thread = threading.Thread(target=self.sender, args=(new_sock, talker))
        rec_thread.start()
        while True:
            data = new_sock.recv(1024)
            info = data.decode("utf-8")
            if info == "!exit" or not data:
                break
            self.buffer_lock.acquire()
            self.buffer[username].insert(0, info)
            self.buffer_lock.release()
            time.sleep(0.5)
        new_sock.close()
        print("Connection from ", addr, "closed")

    def sender(self, new_sock, talker):
        while not new_sock._close:
            # send data from buffer
            time.sleep(1)
            if talker not in self.buffer:
                continue
            elif len(self.buffer[talker]) == 0:
                continue
            else:
                info = self.buffer[talker].pop()
                new_sock.send(info.encode("utf-8"))

    def run(self):
        while True:
            new_sock, addr = self.sock.accept()
            threading.Thread(target=self.handler, args=(new_sock, addr)).start()

if __name__ == "__main__":
    import configparser

    # Read configure
    config = configparser.ConfigParser()
    config.read("chat.conf")
    addr = config["server"]["address"]
    port = config["server"]["port"]

    print("Initializing server . . . address: %s port: %s" % (addr, port))

    serve = Server(addr, int(port))
    serve.run()
