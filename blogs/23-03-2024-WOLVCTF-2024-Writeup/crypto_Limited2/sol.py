import random

correct = [192, 123, 40, 205, 152, 229, 188, 64, 42, 166, 126, 125, 13, 187, 91]

possible = []
for i in range(1703894400, 1704153600):
    random.seed(i)
    if "w" == chr(correct[0] ^ random.getrandbits(8)):
        i2 = i+random.randint(1,60)
        random.seed(i2+1)
        if "c" == chr(correct[1] ^ random.getrandbits(8)):
            i3 = i2+random.randint(1,60)
            random.seed(i3+2)
            if "t" == chr(correct[2] ^ random.getrandbits(8)):
                i4 = i3+random.randint(1,60)
                random.seed(i4+3)
                if "f" == chr(correct[3] ^ random.getrandbits(8)):
                        possible.append(i)
                        
flag = ""
for time_cycle in possible:
    flag = ""
    for i in range(len(correct)):
        random.seed(i+time_cycle)
        res = correct[i] ^ random.getrandbits(8)
        flag += chr(res)
        time_cycle += random.randint(1,60)
        
print(flag)