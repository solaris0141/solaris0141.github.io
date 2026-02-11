from pwn import *
from binascii import unhexlify,hexlify

r = remote('blocked2.wolvctf.io', 1337)
r.recvuntil(b"you have one new encrypted message:\n").decode()
encflag = r.recvline().decode()[:-1]


msg = []

r.recvuntil(b" > ")
r.sendline(encflag[:32].encode())
res = r.recvline().decode()[:-1]
Eiv = unhexlify(res[64:96])
msg.append(xor(Eiv,unhexlify(encflag[32:64])))
print(msg)

for i in range(16):
    r.recvuntil(b" > ")
    r.sendline(hexlify(msg[i]))
    res = r.recvline().decode()[:-1]
    Ept = unhexlify(res[64:96])
    msg.append(xor(Ept,unhexlify(encflag[32*(i+2): 32*(i+3)])))

print("".join([i.decode() for i in msg]))