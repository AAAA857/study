import os
import random



def Verification_code(number):
    res = ""
    li = []
    for i in range(number):
        # 生成 0-9 随机整数数字
        N = str(random.randint(0,9))
        S = chr(random.randrange(start=97,stop=130))
        li.append(N)
        li.append(S)
        k = random.choice(li)
        res += k
    return  res

print(Verification_code(4))