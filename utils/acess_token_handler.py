from cryptography.fernet import Fernet
import base64

class AccessToken:
    def __init__(self):
        self.key = Fernet.generate_key()  # 🔐 You should store this key securely
        self.cipher = Fernet(self.key)

    def encrypt(self,access_token):
        encrypted_token = self.cipher.encrypt(access_token.encode('utf-8'))
        
        print(">>>>>>>>>>>>",encrypted_token)
        return encrypted_token

    def decrypt(self,access_token):
        # Decode from Base64 (if double encoded), then decrypt
        try:

            decrypted = self.cipher.decrypt(access_token).decode('utf-8')
            print("LLLLLLLL>>>>>>>>>>>>",)
            return decrypted
        except Exception as e:
            print("LLLLLLLL",e)
            return False
    




