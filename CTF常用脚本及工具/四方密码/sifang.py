#coding:utf-8
import collections
import re

matrix = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'
pla = 'abcdefghijklmnoprstuvwxyz'
key1 = '[SECURITY]'
key2 = '[INFORMATION]'
key1 = ''.join(collections.OrderedDict.fromkeys(key1))
key2 = ''.join(collections.OrderedDict.fromkeys(key2))

matrix1 = re.sub('[\[\]]','',key1) + re.sub(key1,'',matrix)
matrix2 = re.sub('[\[\]]','',key2) + re.sub(key2,'',matrix)

matrix_list1 = []
matrix_list2 = []
pla_list = []
for i in range(0,len(matrix1),5):
    matrix_list1.append(list(matrix1[i:i+5]))
#print matrix_list1

for i in range(0,len(matrix2),5):
    matrix_list2.append(list(matrix2[i:i+5]))
#print matrix_list2

for i in range(0,len(pla),5):
    pla_list.append(list(pla[i:i+5]))
#print pla_list

#查询两个密文字母位置
def find_index1(x):
    for i in range(len(matrix_list1)):
        for j in range(len(matrix_list1[i])):
            if matrix_list1[i][j] == x:
                return i,j
def find_index2(y):
    for k in range(len(matrix_list2)):
        for l in range(len(matrix_list2[k])):
            if matrix_list2[k][l] == y:
                return k,l

def gen_pla(letter):

    #两个子母中第一个字母位置
    first = find_index1(letter[0])

    #两个子母中第二个字母位置
    second = find_index2(letter[1])

    pla = ''
    pla += pla_list[first[0]][second[1]]
    pla += pla_list[second[0]][first[1]]

    return pla

def main():
    cip = 'ZHNJINHOOPCFCUKTLJ'
    pla = ''
    for i in range(0,len(cip),2):
        pla += gen_pla(cip[i:i+2])
    print(pla)

if __name__ == '__main__':
    main()
