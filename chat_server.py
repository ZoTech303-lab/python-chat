#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s telah terhubung ke." % client_address)
        client.send(bytes("Masukan Nickname dan klik kirim!", ("utf-8")))
        address[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFFSIZE).decode("utf-8")
    wel = 'Selamat datang %s! jika ingin keluar dari chat, ketik "exit".' % name
    client.send(bytes(wel, "utf-8"))
    msg = "%s telah bergabung ke chat!" % name
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("exit", "utf-8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("exit", "utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s telah keluar dari chat." % name, "utf-8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+msg)


clients = {}
address = {}

HOST = input("Masukan IP address : ")
PORT = input("Masukan Port : ")
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("[+] Menunggu Koneksi....")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()