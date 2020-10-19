import socket
import threading
from tkinter import *

def Enter_pressed(event):
    input_get = input_field.get()

    s.sendall(bytes(input_get,'UTF-8'))
    input_user.set('')
    return input_get


def toBoard(msg):
    
    messages.config(state="normal")
    messages.insert(INSERT, '%s\n' % msg)
    messages.config(state="disabled")

def Get_Message():
    while True:
        data = s.recv(1024).decode()
        toBoard(data)
    


HOST = '127.0.0.1'
PORT = 8080

window = Tk()

messages = Text(window,state="disabled")
messages.pack()

input_user = StringVar()
input_field = Entry(window, text=input_user,bd=5,font=("Calibri 12"))

input_field.pack(side=BOTTOM, fill=X,padx=5,pady=10)

frame = Frame(window)
input_field.bind("<Return>", Enter_pressed)
frame.pack()


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    toBoard("Connected to Server")
    t2 = threading.Thread(target=Get_Message,args=[])
    t2.start()
    window.mainloop()




