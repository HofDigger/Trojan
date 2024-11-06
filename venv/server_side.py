import os
import socket
import ssl

def generate_key(client_ip):
    random_key = os.urandom(32)
    with open(r'path:\path\path\path\path{}'.format(client_ip)) as key_file:
        key_file.write(random_key)
    return random_key
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind("127.0.0.1", 8080)
s.listen(1)
print("Server is listening")
while True:
    con, addr = s.accept()
    ssl_socket = ssl.wrap_socket(con, server_side=True, certfile="server.crt", keyfile="server.key")
    ip, port = ssl_socket.getpeername()
    random_key = generate_key(ip)
    ssl_socket.sendall(random_key)

