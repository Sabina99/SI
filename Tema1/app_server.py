import socket
import select
from KM import OFB
from KM import ECB

ip = "127.0.0.1"
port = 5000
k3 = b'veryawesomekeyyy'
k2 = 'ana are merepere'
k1 = 'ana are peremere'

# instantire
server_socket = socket.socket()
server_socket.bind((ip, port))

server_socket.listen(2)

# accept conexiunea
conn, address = server_socket.accept()
print("Conexiune formata :)")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    if str(data) == 'ecb':
        aux = ECB(k1, k3)
        to_send = aux.encrypt(k1)

        # trimit cheia criptat catre client
        conn.send(to_send.encode())
        mesaj = conn.recv(1024).decode()

        # textul criptat a fost primit si pot coninua
        if str(mesaj) == 'ok':
            text_de_trimis = '9876543219876543'
            aux2 = ECB(text_de_trimis, k1.encode())
            crypto = aux2.encrypt(text_de_trimis)
            conn.send(crypto.encode())

    if str(data) == 'ofb':
        aux = OFB(k2, k3)
        to_send_key = aux.encrypt(k2)
        to_send_init_vec = aux.init_vec

        # trimit info catre client
        conn.send(to_send_key.encode())
        conn.send(str(to_send_init_vec).encode())

        mesaj = conn.recv(1024).decode()

        #  poate incepe comunicarea
        if str(mesaj) == 'ok':
            text_de_trimis = '1234567891234567'
            aux2 = OFB(text_de_trimis, k2.encode())
            init_vec = aux2.init_vec
            crypto = aux2.encrypt(text_de_trimis)
            conn.send(crypto.encode())
            conn.send(str(init_vec).encode())

# am inchis conxiunea
conn.close()
