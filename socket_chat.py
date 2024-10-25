import socket
from threading import Thread
print("""
    1-) Sunucuya Bağlan
    2-) Sunucu Aç
    """)

secenek = int(input(" => "))

def server(IP,PORT):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen()
    accept_list = []
    print(f"Server Ip : {IP} Port : {PORT} is Listening ")

    def revAndSending(i):
        while True:
            try:
                gelen = i.recv(1024).decode("utf-8")
            except ConnectionResetError:
                print("Bağlantı Kapatıldı")
                
            with open("Chat_record.txt","a+",encoding="utf-8") as chat:
                chat.write(gelen+"\n")
            print(gelen)
            for a in accept_list:
                a.send(gelen.encode("utf-8"))

    while True:
        conn , addr = server.accept()
        accept_list.append(conn)
        th = Thread(target=revAndSending,args=(conn,))
        th.start()
        th.join()

def client(IP,PORT):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP,PORT))
    user = input("Kullanıcı Adı :")

    def sendMessage():
        while True:
            msg = input("==>")
            if msg=="close":
                client.close()
            client.send((f"{user}==>"+msg).encode("utf-8"))

    def recvMessage():
        while True:
            msg = client.recv(1024).decode("utf-8")
            if msg:
                print(msg)

    th = Thread(target=sendMessage)
    th2 = Thread(target=recvMessage)
    th.start()
    th2.start()

if secenek == 1:
    IP  = input("İP Adresi Girin :")
    PORT = 4466
    client(IP,PORT)

elif secenek == 2:
    IP  = socket.gethostbyname(socket.gethostname())
    PORT = 4466
    server(IP,PORT)
else :
    print("Yanlış Seçim!")



