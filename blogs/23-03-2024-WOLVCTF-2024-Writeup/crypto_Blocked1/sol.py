from pwn import *
from binascii import hexlify, unhexlify


r = remote("blocked1.wolvctf.io", 1337)

print(r.recvuntil(b"you are logged in as: ").decode())
username = r.recvline().decode()[:-1]
assert len(username) == 12
print(r.recvuntil(b"> ").decode())
r.sendline(b"2")
token = r.recvline().decode()
print(token)
print(r.recvuntil(b"> ").decode())
iv = token[:32]
ct1 = token[32:64]
ct2 = token[64:96]
f = xor(unhexlify(ct1), str(username).encode() + b'\0\0\0\0')
ct1 = hexlify(xor(f, b'doubledelete\0\0\0\0')).decode()
newtoken = iv + ct1 + ct2
print(newtoken)
r.sendline(b'1')
print(r.recvuntil(b"> ").decode())
r.sendline(newtoken.encode())
print(r.recvline().decode())