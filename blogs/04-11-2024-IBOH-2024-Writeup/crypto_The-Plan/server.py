#!/usr/local/bin/python
import random
from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime
from log import chatlog
import sys

def main():
    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    N = (p**2)*q

    while True:
        g = random.randint(2,p-1)
        
        if pow(g,p-1,p**2) != 1:
            break
    h = pow(g,N,N)

    def encrypt_log(N: int, g: int, h: int, log: bytes):
        val = bytes_to_long(log)
        #assert val < p #prevents log corruption
        enc_sessionkey = (val//p)+p+q
        r = random.randint(1,N-1)
        sol = (pow(g,val,N)*pow(h,r,N))%N                                                                       
        return hex(sol)[2:], enc_sessionkey

    def decrypt_log(g: int, p: int, enc_log: int):
        a = (pow(enc_log,p-1,p**2) - 1)//p
        b = (pow(g,p-1,p**2) - 1)//p
        res = (a*pow(b,-1,p))%p
        return hex(res)[2:]

    choice_encrypt = True
    choice_decrypt = True

    while True:
        try:
            print("\nSecret Encryption Service (Legacy)")
            print("(1) Encrypt")
            print("(2) Decrypt")
            print("(3) View Encrypted Log")
            print("(4) Update Encrypted Log")
            
            selection = input(">> ")
            if selection == '1':
                if choice_encrypt:
                    newlog = input("Enter log to be encrypted: ")
                    enc_log, enc_sessionkey = encrypt_log(N,g,h,newlog.encode())
                    print(f"Public keys: {(N,g)}")
                    print(f"Encrypted Log: {enc_log}")
                    print(f"Session Key: {enc_sessionkey}")
                    choice_encrypt = False
                else:
                    print("You already encrypted before")
                    
            elif selection == '2':
                if choice_decrypt:
                    encrypted_log = bytes_to_long(bytes.fromhex(input("Encrypted Log Value: ")))
                    dec_log = decrypt_log(g, p, encrypted_log)
                    print(f"Decrypted Log: {dec_log}")
                    choice_decrypt = False
                else:
                    print("You already decrypted before")
                    
            elif selection == '3':
                ENC_LOG, ENC_SESSIONKEY = encrypt_log(N,g,h,chatlog)
                print(f"Public keys: {(N,g)}")
                print(f"Encrypted Log: {ENC_LOG}")
                print(f"Session Key: {ENC_SESSIONKEY}")
                
            elif selection == '4':
                print("Something went wrong...")
                quit()
                
        except Exception as e:
            quit()
            
if __name__ == "__main__":
    sys.set_int_max_str_digits(10000)
    main()
else:
    raise Exception("Problem Occured")