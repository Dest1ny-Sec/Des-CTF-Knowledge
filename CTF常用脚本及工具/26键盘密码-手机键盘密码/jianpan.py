# -*- coding:utf-8 -*-
# Author : Konmu
# [NCTF2019]Keyboard

chiper='ooo yyy ii w uuu ee uuuu yyy uuuu y w uuu i i rr w i i rr rrr uuuu rrr uuuu t ii uuuu i w u rrr ee www ee yyy eee www w tt ee'
chiper=chiper.split(' ')

keys=['q','w','e','r','t','y','u','i','o']
values=[1,2,3,4,5,6,7,8,9]
dicts=dict(zip(keys,values))

jiugongge=['   ','abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']
new_dicts=dict(zip(values,jiugongge))

for i in range(len(chiper)):
    temp=dicts.get(chiper[i][0])
    print(''.join(new_dicts[temp][len(chiper[i])-1]),end='')