import socket, threading
import re

HOST = '127.0.0.1'
PORT = 8080

clients = []
clientNum = 1

def send_to_all(msg):  
    for client in clients : 
        client[0].sendall(bytes(msg,'UTF-8'))


def send_to_unique(msg,toID,fromID):
    if toID > len(clients):        
        clients[fromID][0].send(bytes("User Does not exist",'UTF-8'))
    else:
        print("Client"+str(fromID)+": "+msg)
        clients[fromID][0].send(bytes("Client"+str(fromID)+": "+msg,'UTF-8'))
        clients[toID][0].send(bytes("Client"+str(fromID)+": "+msg,'UTF-8'))


class ClientThread(threading.Thread):
    def __init__(self, CAddr, CSock,num):        
        super().__init__()
        self.cnum = num
        self.csocket = CSock
        self.CAddr = CAddr
        print("\nNew Connection Added: ",CAddr)

    def run(self):
        print("Connection from : ",self.CAddr,"\n")
        self.csocket.send(bytes("You are connected as Client"+str(self.cnum) + "\n",'UTF-8'))
        send_to_all("client"+str(self.cnum) + " has entered the chat")
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            if not msg:
                break
            tokens = msg.split()
            if tokens[0][0] == "@":
                user = int(re.search(r'\d+', tokens[0]).group())
                print(self.cnum," ",user)
                send_to_unique(msg,user-1,self.cnum-1)
            else:
                print("Client"+str(self.cnum),": ",msg)
                send_to_all("Client"+str(self.cnum) + ": " + msg)

        print("client",self.CAddr," disconnected\n")



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))

    while True:
        s.listen(1)
        conn, addr = s.accept()
        clients.append([conn,addr])
        newthread = ClientThread(addr,conn,clientNum)
        clientNum+=1
        newthread.start()

