from pwn import *
from sympy import *
from Crypto.Util.number import *
while True:
    r = remote("chall.lac.tf",31171)
    #r.interactive()
    exec(r.recvline().decode())
    exec(r.recvline().decode())
    exec(r.recvline().decode())
    print(r.recvuntil("> ").decode())

    try:
        x = randint(0,N//4)
        print(x)
        r.sendline(str((x**2)).encode())
        y = int(r.recvline().decode())
    except:
        continue
    
    print(f"{N = }")
    print(f"{e = }")
    print(f"{ct = }")
    print(f"{y = }")
    a = gcd(y+x,N)
    b = gcd(y-x,N)
    c = ((y+x)*(y-x)) % N
    print(f'{a=}')
    print(f'{b=}')
    print(f'{c=}')
    if c == 0:
        if a != N and b != N:
            break
    r.close()
    
if a == 1:
    p = b
    q = N//b
elif b == 1:
    p = a
    q = N//b
else:
    p = a
    q = b
phi = (p-1)*(q-1)
d = pow(int(e),-1,int(phi))
print(f"{d=}\n")
print(long_to_bytes(pow(int(ct),d,int(N))))