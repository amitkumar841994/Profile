from cryptography.fernet import Fernet
import base64

class AccessToken:
    def __init__(self, access_token):
        self.access_token = access_token
        self.key = Fernet.generate_key()  # 🔐 You should store this key securely
        self.cipher = Fernet(self.key)

    def encrypt(self):
        encrypted_token = self.cipher.encrypt(self.access_token.encode('utf-8'))
        
        encoded = base64.b64encode(encrypted_token).decode('utf-8')
        print(">>>>>>>>>>>>",encoded)
        return encoded

    def decrypt(self, encoded_token):
        # Decode from Base64 (if double encoded), then decrypt
        encrypted_token = base64.b64decode(encoded_token)
        decrypted = self.cipher.decrypt(encrypted_token).decode('utf-8')
        return decrypted
    

AccessToken("AFasdfgaWECLS").encrypt()


