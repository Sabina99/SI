import socket
import json

from KM import ECB
from KM import OFB

ip = "127.0.0.1"
port = 5000  # socket server port number
key_to_decrypt_keys = b'veryawesomekeyyy'

# instantiere
client_socket = socket.socket()

# conectat la server
client_socket.connect((ip, port))

message = input("Dati modul de criptare (ecb/ofb): ")

while message != 'stop':
    if message == 'ecb':

        #  am trimis cum vreau sa cripteze
        client_socket.send(message.encode())

        # se primeste cheia criptata
        enc_text = client_socket.recv(1024).decode()
        print('text criptat: ' + enc_text)
        aux = ECB(enc_text, key_to_decrypt_keys)

        #  se decripteaza cheia
        cheie = aux.decrypt(enc_text).encode()
        print('k1=', cheie)

        #  poate incepe comunicarea
        client_socket.send('ok'.encode())

        #  se primeste textul criptat
        text_primit = client_socket.recv(1024).decode()
        print('text primit de la server, criptat: ', text_primit)

        # se decripteaza textul primit
        aux2 = ECB(text_primit, cheie)
        txt_decr = aux2.decrypt(text_primit)
        print('textul decriptat:', txt_decr)

    if message == 'ofb':
        #  trimit modul de criptare de la client la server
        client_socket.send(message.encode())

        # primesc de la server vectorul de initializare si cheia criptata
        enc_text = client_socket.recv(1024).decode()

        print('text criptat: ' + enc_text)

        to_rec_init_vec = client_socket.recv(1024).decode()
        to_rec_init_vec = json.loads(to_rec_init_vec) 

        #  se decripteaza cheia
        aux = OFB(enc_text, key_to_decrypt_keys)
        aux.set_init_vec(to_rec_init_vec)
        cheie = aux.decrypt(enc_text).encode()
        print('k2=', cheie)

        #  poate incepe comunicarea
        client_socket.send('ok'.encode())

        #  se primeste textul criptat
        text_primit = client_socket.recv(1024).decode()
        print('text primit de la server, criptat: ', text_primit)

        # se decripteaza textul
        aux2 = OFB(text_primit, cheie)
        to_rec_init_vec = client_socket.recv(1024).decode()
        init_vec = json.loads(to_rec_init_vec)
        aux2.set_init_vec(init_vec)

        print('text decriptat: ', aux2.decrypt(text_primit))

    message = input(" -> ") 
    
client_socket.close() 
