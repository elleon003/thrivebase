from cryptography.fernet import Fernet
import os
import base64
from typing import Optional

class TokenEncryption:
    def __init__(self):
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable is required")
        
        # Ensure the key is properly padded for base64 encoding
        key_bytes = key.encode()
        padding = len(key_bytes) % 4
        if padding:
            key_bytes += b'=' * (4 - padding)
        
        try:
            # Convert the base64 key to bytes for Fernet
            self.fernet = Fernet(base64.urlsafe_b64encode(key_bytes[:32]))
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {str(e)}")
    
    def encrypt_token(self, token: str) -> str:
        """
        Encrypt a token string
        """
        if not token:
            return None
        return self.fernet.encrypt(token.encode()).decode()
    
    def decrypt_token(self, encrypted_token: str) -> Optional[str]:
        """
        Decrypt an encrypted token string
        """
        if not encrypted_token:
            return None
        try:
            return self.fernet.decrypt(encrypted_token.encode()).decode()
        except Exception:
            return None

# Global instance
token_encryption = TokenEncryption()
