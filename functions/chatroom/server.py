#!/usr/bin/env python
# coding: utf-8

# In[2]:


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


# In[3]:


clients = {}
addresses = {}
HOST = '<LAN/Local IP address>'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR, 8000)


# In[5]:


#A loop to wait incoming connections

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s: %s has connected." % client_address)
        client.sent(bytes("Now you can type your name. Please Enter after finish.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


# In[6]:


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you want to quit this chatroom, please type {quit} to exit.' % name
    msg = "%s has joined the chat." % name
    client.send(bytes(welcome, "utf8"))
    clients[client] = name
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the room." % name, "utf8"))
            break


# In[7]:


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


# In[ ]:


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connections...")
    accept_thread = Thread(target=accept_incoming_connections)
    accept_thread.start()
    accept_thread.join()
    SERVER.close()



