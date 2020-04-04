import socket
import time


server = "irc.freenode.net"
port = 6667
channel = "#bitcoin"
username = "Gambito123"
msg = " :Hola  !"

#implementamos una clase cliente.
class UserClient:

    def __init__(self, server, port, user,channel,msg):
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

    #Este metodo envia info de log
    def send(self,nick):
        self.conn.send(nick)

    #este sirve para formatear los mensajes
    def prepare(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message).encode("utf-8")
        self.conn.send(command)

    # selecciona el canal
    def select_channel(self):
        chan = "JOIN  {}\r\n".format(self.channel).encode("utf-8")
        self.conn.send(chan)

    #envia el mensaje al canal
    def send_message(self):
        send = "PRIVMSG {} \r\n".format(self.msg)
        print(send)
        self.conn.send("PRIVMSG {} {}\r\n".format(self.channel,self.msg).encode())


if __name__ == "__main__":

    #creamos la instancia
    client = UserClient(server, port, username, channel,msg)
    accepted = False
    #conectamos
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
    
    #enviamos el mensaje y fin del programa 
    print("sending..")
    time.sleep(1)
    client.send_message()






