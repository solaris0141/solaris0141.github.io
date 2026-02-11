import random

correct = [189, 24, 103, 164, 36, 233, 227, 172, 244, 213, 61, 62, 84, 124, 242, 100, 22, 94, 108, 230, 24, 190, 23, 228, 24]

for i in range(256):
    random.seed(i)
    if 119 == correct[0] ^ random.getrandbits(8):
        random.seed(i+1)
        if 99 == correct[1] ^ random.getrandbits(8):
            random.seed(i+2)
            if 116 == correct[2] ^ random.getrandbits(8):
                random.seed(i+3)
                if 102 == correct[3] ^ random.getrandbits(8):
                    time_cycle = i
                    
print(time_cycle)

flag = ""
for i in range(len(correct)):
    random.seed(i+time_cycle)
    flag += chr(correct[i] ^ random.getrandbits(8))
print(flag)