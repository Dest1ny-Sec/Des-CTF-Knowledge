# -*- coding: utf-8 -*-
# 使用前注意修改判别flag条件，第35行*********

dic = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7,
       17: 23, 19: 11, 21: 5, 23: 17, 25: 25}  # 模逆

# 加密


def encrypt(clear_content, key_a, key_b):
    result = ""
    for i in clear_content:
        if (ord(i) >= 65 and ord(i) <= 90):
            result += chr(((key_a*(ord(i)-65)+key_b) % 26)+65)
        elif (ord(i) >= 97 and ord(i) <= 122):
            result += chr(((key_a*(ord(i)-97)+key_b) % 26)+97)
        else:
            result += i
    return result

# 穷举


def blasting(cipher):
    lis = []
    flag = []
    result = ""
    a = 1
    for i in dic.keys():
        for j in range(0, 26):
            for s in cipher:
                if (ord(s) >= 65 and ord(s) <= 90):
                    result += chr(((dic.get(i) * (ord(s)-65) -
                                  (dic.get(i) * j) % 26) % 26)+65)
                elif (ord(s) >= 97 and ord(s) <= 122):
                    result += chr(((dic.get(i) * (ord(s)-97) -
                                  (dic.get(i) * j) % 26) % 26)+97)
                else:
                    result += s
            print('明文' + str(a) + ' : ' + result)
            a += 1
            if result[0:3].lower() in ['key', 'ctf', 'fla']:
                flag.append(result)
            result = ""
    return flag


if __name__ == '__main__':
    prompt = """选择：(e)加密  （c）破解
    请输入您的选择："""
    choice = 'e'
    if choice == 'e':
        ming = input("请输入明文：")
        key = input("请输入加密密钥：a和b，以空格间隔").split(" ")
        print("密文为：%s" % (encrypt(ming, int(key[0]), int(key[1]))))
    elif choice == 'c':
        cipher = input("请输入密文：")
        plain = blasting(cipher)
        print("程序判定flag为：")
        print(plain)
