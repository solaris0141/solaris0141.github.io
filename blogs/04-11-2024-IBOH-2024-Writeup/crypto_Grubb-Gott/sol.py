import itertools

def reverse_Ciao(ciphertext, n):
    nsize = len(n)
    output = ""

    for i in range(len(ciphertext)):
        if ciphertext[i] == ' ':
            output += ' '
            continue
        
        code = ord(ciphertext[i]) - ord('a')

        n[0] -= 1
        for j in range(nsize - 1):
            if n[j] < 0:
                n[j] = 25
                n[j + 1] -= 1
            else:
                break
        
        for j in range(nsize):
            code = (code + n[j]) % 26
        
        if code % 2 == 0:
            code -= 1
        else:
            code += 1
        
        for j in range(nsize - 1, -1, -1):
            code = (code - n[j]) % 26
            if code < 0:
                code = 26 + code
        
        output += chr(code + ord('a'))

    return output

ciphertext = "sijrknpjtmjjfdmhhlb"
possible_values = [0, 1]
all_rotor_combinations = itertools.product(possible_values, repeat=6)
for rotors in all_rotor_combinations:
    rotor = list(rotors)
    secret = reverse_Ciao(ciphertext, rotor)
    print("Decrypted secret:", secret, rotors)