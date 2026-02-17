#!/usr/local/bin/python
from secret import greenwire, blackwire, redwire, flag
import random

class DefuserModule:
    y = blackwire
    x = redwire
    g = greenwire
    
    def __init__(self, activationNumber):
        self.s = activationNumber
    
    def gen(self):
        self.s = (self.s * self.y + self.x) % self.g
        return self.s
    
def genSafetyNums(activationNumber):
    defuser = DefuserModule(activationNumber)
    nums = []
    for i in range(20):
        nums.append(defuser.gen())
    return nums

def main():
    print("Bomb has been activated, you have 45 seconds to enter all the safety numbers to deactivate this")
    keyvalue = random.randint(1, greenwire)
    safetyNums = genSafetyNums(keyvalue)
    
    print(f"The activation key value is: {keyvalue}")
    print("Enter the safety number if you insist on deactivating")
    inputNums = []
    
    for i in range(20):
        try:
            nums = int(input("> "))
            inputNums.append(nums)
        except:
            print("Careless mistake there, bye")
            print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMMMMMMMMMMM (loud explosion noises*)")
            quit()
    
    if safetyNums == inputNums:
        print("Bomb has been defused, here's the status code: ", flag)
    else:
        print("Safety numbers are false, detonating immediately")
        print("Might as well tease you with the some of the actual safety numbers, not like you could do anything about it now")
        print("\n".join([str(i) for i in safetyNums[:3]]))
        print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMMMMMMMMMMM (loud explosion noises*)")
        quit()
        
if __name__ == "__main__":
    main()
else:
    raise Exception("Problem Occured")