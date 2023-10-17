"""
POC
"""
from toku.crypto.cipher.api import Cipher
from toku.crypto.cipher.aes import AesCipher

cipher: Cipher = AesCipher(bytes("ak58fj287fivk287", "utf-8"))
ciphertext: str = cipher.encrypt("poc")
plaintext: str = cipher.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
