from tkinter import *
import socket
import time
import threading as thread
import queue

q = queue.Queue()


server = "irc.freenode.net"
port = 6667
channel = "#gus-challenge"
username = "Gambito-x"
msg = " :Hola dede bot Py !"


class Window:
    def __init__(self, server, port, channel, username):
        self.ventana = Tk()
        self.server = server
        self.port = port
        self.channel = channel
        self.username = username
        self.config()
        self.widgets()

    def config(self):
        self.ventana.geometry("400x600+400+150")
        self.ventana.title("IRC-Chat")

    def widgets(self):
        # info de conexion
        self.serverDataLabel = Label(
            self.ventana, text="Server").place(x=20, y=5)
        self.serverData = Entry(self.ventana)
        self.serverData.place(x=20, y=25)
        self.serverData.insert(1, self.server)

        self.portDataLabel = Label(
            self.ventana, text="Port").place(x=150, y=5)
        self.portData = Entry(self.ventana)
        self.portData.place(x=150, y=25)
        self.portData.insert(1, self.port)

        self.channelDataLabel = Label(
            self.ventana, text="Channel").place(x=20, y=45)
        self.channelData = Entry(self.ventana)
        self.channelData.place(x=20, y=65)
        self.channelData.insert(1, self.channel)

        self.channelDataLabel = Label(
            self.ventana, text="Username").place(x=150, y=45)
        self.channelData = Entry(self.ventana)
        self.channelData.place(x=150, y=65)
        self.channelData.insert(1, self.username)
        #---------------------------------

        # area de mensajes
        self.writeArea = Entry(self.ventana, width=50)
        self.writeArea.place(x=40, y=560)

        # boton enviar
        self.sendButton = Button(
            self.ventana, text="Enviar", background="#fc6c7a")
        self.sendButton.place(x=350, y=560)

        # area de escritura
        self.textArea = Entry(self.ventana, width=40)
        self.textArea.place(x=20, y=95)

    def displayMsg(self):
        f = open("datos/data.txt", "r")
        a = f.read()
        self.textArea.insert(0, a)
        f.close()

        #--------------------------------------------------------------------
        #--------------------------------------------------------------------


class UserClient:

    def __init__(self, server, port, user, channel, msg):
        self.server = server
        self.port = port
        self.channel = channel
        self.user = user
        self.msg = msg

    # Abrimos el socket
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    # Leemos la respuesta del server
    def get_response(self):
        return self.conn.recv(512).decode("utf-8")

    # Este metodo envia info de log
    def send(self, nick):
        self.conn.send(nick)

    # este sirve para formatear los mensajes
    def prepare(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message).encode("utf-8")
        self.conn.send(command)

    # selecciona el canal
    def select_channel(self):
        chan = "JOIN  {}\r\n".format(self.channel).encode("utf-8")
        self.conn.send(chan)

    # envia el mensaje al canal
    def send_message(self, m=None):
        if m != None:
            self.conn.send("PRIVMSG {} {}\r\n".format(
                self.channel, m).encode())

    def __str__(self):
        dat = "Server: {} \nPort: {}\nUser: {}\nChannel:{}".format(self.server, self.port,
                                                                   self.user, self.channel)
        return dat

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def check():
    v.displayMsg()


def resetData():
    f = open("datos/data.txt", "w")
    f.close()


def bot():
    # creamos la instancia
    client = UserClient(server, port, username, channel, msg)
    accepted = False
    # conectamos
    client.connect()

    # Bucle para establecer la coneccio  y entrada al canal
    while accepted == False:
        resp = client.get_response()
        print(resp.strip())

        if "No Ident response" in resp:
            client.prepare("NICK", username)
            client.prepare("USER", "{} * * :{}".format(username, username))

        if "376" in resp:
            client.select_channel()

        if "/NAMES list" in resp:
            accepted = True

    time.sleep(1)
    client.send_message()
    print(client)

    while True:
        dataStore = open("datos/data.txt", "a")
        resp = client.get_response()
        print(resp.strip())
        if "PING" in resp:
            client.send_message("PONG")
        elif "hola" in resp.lower():
            client.send_message(":Hola soy un bot")

        elif "freenode.net" not in resp:
            dataStore.write(resp + "\n")
            dataStore.close()
            check()


#--------------------------------------------------


def startApp():
    w = thread.Thread(target=bot)
    w.start()


#--------------------------------------------------


resetData()

v = Window(server, port, channel, username)

startApp()
v.ventana.mainloop()

# while(cmd != "/quit"):
#     cmd = input("< {}> ".format(username)).strip()
#     if cmd == "/quit":
#         client.send_cmd("QUIT", "Good bye!")
#     client.send_message_to_channel(cmd)

#     # socket conn.receive blocks the program until a response is received
#     # to prevent blocking program execution, receive should be threaded
#     response_thread = threading.Thread(target=print_response)
#     response_thread.daemon = True
#     response_thread.start()
