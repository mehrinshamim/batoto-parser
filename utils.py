import hashlib
from Crypto.Cipher import AES
from typing import Tuple

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
    """
    OpenSSL EVP_BytesToKey style (MD5 loop) to derive key and iv.
    """
    generated = b""
    prev = b""
    while len(generated) < (key_len + iv_len):
        md = hashlib.md5()
        md.update(prev + password + salt)
        prev = md.digest()
        generated += prev
    key = generated[:key_len]
    iv = generated[key_len:key_len+iv_len]
    return key, iv

def decrypt_batoto(encrypted_b64: str, password: str, decode_base64_fn) -> str:
    """
    Decrypt batoWord with password. decode_base64_fn should return bytes.
    """
    cipher_data = decode_base64_fn(encrypted_b64)
    if not cipher_data.startswith(b"Salted__"):
        raise ValueError("Missing Salted__ header in encrypted data")
    salt = cipher_data[8:16]
    encrypted = cipher_data[16:]
    key, iv = evp_bytes_to_key(password.encode("utf-8"), salt, 32, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    # remove PKCS#7 padding
    pad_len = decrypted[-1]
    if pad_len < 1 or pad_len > 16:
        # fallback: return raw
        return decrypted.decode("utf-8", errors="ignore")
    return decrypted[:-pad_len].decode("utf-8", errors="ignore")

def generate_uid(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()