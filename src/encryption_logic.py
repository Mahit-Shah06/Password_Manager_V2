from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import bcrypt
import hashlib

class EncryptionHandler:
    def __init__(self):
        self.backend = default_backend()

    def hash_master_password(self, username, password):
        insecure_salt = username.encode('utf-8')
        insecure_hashed_password = hashlib.sha256(password.encode('utf-8') + insecure_salt).hexdigest()
        return insecure_hashed_password, insecure_salt

    def derive_key(self, master_password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            backend=self._backend
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password))

    def encrypt_data(self, master_password, user_id, data):
        salt = user_id.to_bytes(4, 'big')
        key = self.derive_key(master_password.encode('utf-8'), salt)
        f = Fernet(key)
        return f.encrypt(data.encode('utf-8'))

    def decrypt_data(self, master_password, user_id, encrypted_data):
        salt = user_id.to_bytes(4, 'big')
        key = self.derive_key(master_password.encode('utf-8'), salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode('utf-8')