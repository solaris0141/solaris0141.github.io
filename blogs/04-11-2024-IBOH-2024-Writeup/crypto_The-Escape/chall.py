import hashlib
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.number import *
import random
from secret import FLAG, n, private_key

class Signature:
    def __init__(self, n):
        self.n = n
        self.generator = random.randint(2,self.n-1)
    
    def genPublic(self, priv: int):
        return pow(self.generator,priv,self.n)

    def sign(self, message: str, priv: int, nonce):
        sig = []
        for k in nonce:
            r = pow(self.generator,k,self.n)
            e = int(hashlib.sha256((message + str(r)).encode()).hexdigest(), 16)
            s = (k - priv * e) % (self.n - 1)
            sig.append((r,s))
        return sig
        
    def verify(self, message: str, sig, pub: int):
        e = int(hashlib.sha256((message + str(sig[0])).encode()).hexdigest(), 16)
        v = ((pow(self.generator,sig[1], self.n))*(pow(pub,e,self.n))) % (self.n)
        return v==sig[0]


def getNonce():
    a = random.randbytes(18)
    b = random.randbytes(8) + a[8:] 
    return bytes_to_long(a),bytes_to_long(b)


Signer = Signature(n)
public_key = Signer.genPublic(private_key)
nonce_1 = getNonce()
nonce_2 = getNonce()
KEY = long_to_bytes(private_key)[:16]
iv = long_to_bytes((nonce_1[1]*nonce_2[1])-(nonce_2[0]*nonce_1[1])+(nonce_2[0]*nonce_1[0])-(nonce_1[0]*nonce_2[1]))[:16]
cipher = AES.new(KEY, AES.MODE_CBC, iv)
enc_flag = cipher.encrypt(pad(FLAG, 16)).hex()

signatures_1 = Signer.sign(enc_flag, private_key, nonce_1)
signatures_2 = Signer.sign(enc_flag, private_key, nonce_2)

# VERIFIED!!!
assert Signer.verify(enc_flag, signatures_1[0], public_key)
assert Signer.verify(enc_flag, signatures_1[1], public_key)
assert Signer.verify(enc_flag, signatures_2[0], public_key)
assert Signer.verify(enc_flag, signatures_2[1], public_key)

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"Encrypted flag = {enc_flag}\n\n")
    for i in signatures_1:
        f.write(f"{i}\n")
    for i in signatures_2:
        f.write(f"{i}\n")
