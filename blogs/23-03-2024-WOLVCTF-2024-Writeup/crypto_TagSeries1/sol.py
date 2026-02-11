from pwn import *

MESSAGE = b"GET FILE: flag.txt"
r = remote("tagseries1.wolvctf.io", 1337)
r.recvline()
r.sendline(b"aaaaaaaaaaaaaaaa")
r.sendline(b"aaaaaaaaaaaaaaaa")
res = r.recvline()[:-1]
print(res)
msg = MESSAGE + b"a"*14 + b"a"*16
r.sendline(msg)
r.sendline(res)
flag = r.recvline().decode()
print(flag)