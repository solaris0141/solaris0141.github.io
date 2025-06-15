alphabets = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(sep=" ")
print(alphabets)

ct = "Br olzy Jnyetbdrc'g xun, V avrkkr gb sssp km frja sbv kvflsffoi Jnuc Sathrg. Wkmk gytjzyakz mj jsqvcmtoh rc bkd. Canjc kns puadlctus!".upper()
pt = "On this Valentine's day, I wanted to show my love for professor Paul Eggert. This challenge is dedicated to him. Enjoy the challenge!".upper()
key = ""

for i in range(len(ct)):
    if ct[i] not in alphabets:
        continue
    index = (alphabets.index(ct[i]) - alphabets.index(pt[i])) % 26
    key += alphabets[index]
print(key)
print(len(key))