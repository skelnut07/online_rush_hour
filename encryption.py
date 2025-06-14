# encryption.py
from cryptography.fernet import Fernet

# Shared secret key (must be identical on both server and client)
SECRET_KEY = b'vIqEpCGZJZGdP_uzyKcTVmLNFhB2ItKnODwPtBq0yjc='
fernet = Fernet(SECRET_KEY)

def encrypt_message(message: str) -> bytes:
    """receives message to encrypt
    returns encrypted message"""
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    """ receives message to decrypt
    returns decrypted message"""
    return fernet.decrypt(encrypted_message).decode()
