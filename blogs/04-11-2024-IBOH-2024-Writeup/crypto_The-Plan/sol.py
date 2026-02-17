from pwn import *
from Crypto.Util.number import bytes_to_long, GCD, long_to_bytes
import sys
sys.set_int_max_str_digits(10000)
io = remote("127.0.0.1",5002)
print(io.recvuntil(b'>> ').decode())
io.sendline(b'1')
print(io.recvuntil(b': ').decode())
payload = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' #just need to be bigger than 192 bytes (1024*3/2)
io.sendline(payload)
io.recvuntil(b'Public keys: ')
pub = eval(io.recvline().strip(b'\n').decode())
print(pub)
io.recvuntil(b'Encrypted Log: ')
enc_payload = io.recvline().strip(b'\n').decode()
print(enc_payload)
io.recvuntil(b'Session Key: ')
enc_payload_session = io.recvline().strip(b'\n').decode()
print(enc_payload_session)

print(io.recvuntil(b'>> ').decode())
io.sendline(b'2')
io.recvuntil(b'Encrypted Log Value: ')
io.sendline(enc_payload.encode())
io.recvuntil(b'Decrypted Log: ')
dec_payload = bytes.fromhex(io.recvline().strip(b'\n').decode())
print(dec_payload)
s = bytes_to_long(payload)
sp = bytes_to_long(dec_payload)
p = GCD(s - sp, pub[0]) 
q = pub[0]//(p**2)

print(io.recvuntil(b'>> ').decode())
io.sendline(b'3')
io.recvuntil(b'Public keys: ')
io.recvline().strip(b'\n').decode()
io.recvuntil(b'Encrypted Log: ')
enc_flag = io.recvline().strip(b'\n').decode()
print(enc_flag)
io.recvuntil(b'Session Key: ')
enc_flag_session = io.recvline().strip(b'\n').decode()
print(enc_flag_session)

def decrypt_log(g: int, p: int, enc_log: int):
    a = (pow(enc_log,p-1,p**2) - 1)//p
    b = (pow(g,p-1,p**2) - 1)//p
    res = (a*pow(b,-1,p))%p
    return res

res = decrypt_log(pub[1], p, bytes_to_long(bytes.fromhex(enc_flag)))
k = int(enc_flag_session) - p - q
flag = long_to_bytes(res + k*p)
print(flag.decode())