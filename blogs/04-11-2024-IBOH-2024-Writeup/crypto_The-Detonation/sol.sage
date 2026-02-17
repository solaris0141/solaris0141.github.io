from Pwn4Sage.pwn import * 

first = []
second = []

io = remote("127.0.0.1", 5001)
print(io.recvuntil(b"is: ").decode())
first.append(int(io.recvline().decode()[:-1]))
for i in range(20):
    io.recvuntil(b"> ")
    io.sendline(b"12345")
    
print(io.recvline().decode())
print(io.recvline().decode())
first.append(int(io.recvline().decode()[:-1]))
first.append(int(io.recvline().decode()[:-1]))
first.append(int(io.recvline().decode()[:-1]))
io.close()

io = remote("127.0.0.1", 5001)
print(io.recvuntil(b"is: ").decode())
second.append(int(io.recvline().decode()[:-1]))
for i in range(20):
    io.recvuntil(b"> ")
    io.sendline(b"12345")
    
print(io.recvline().decode())
print(io.recvline().decode())
second.append(int(io.recvline().decode()[:-1]))
second.append(int(io.recvline().decode()[:-1]))
second.append(int(io.recvline().decode()[:-1]))
io.close()

ans1 = ((first[2] - first[1])^2) - (first[1] - first[0])*(first[3]-first[2])
ans2 = ((second[2] - second[1])^2) - (second[1] - second[0])*(second[3]-second[2])

N = gcd(ans1,ans2)
assert N != 1
n = N.factor()[-1][0]
print(int(n))
f = Zmod(n)
m = f((first[3] - first[2])*pow(first[2]-first[1],-1,n))
c = f(first[1] - first[0]*m)

def gen(s):
    res = f((f(s)*m)+c)
        
    return int(res)

print("Sending with LCG results")
io = remote("127.0.0.1", 5001)
print(io.recvuntil(b"is: ").decode())
seed = io.recvline().decode()[:-1]
nextnum = seed

for i in range(20):
    io.recvuntil(b"> ")
    nextnum = gen(nextnum)
    io.sendline(str(nextnum).encode())

print(io.recvline().decode())
