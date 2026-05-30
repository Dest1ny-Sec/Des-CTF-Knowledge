import string
enc='PVSF{vVckHejqBOVX9C1c13GFfkHJrjIQeMwf}'
grid='LOVEKFC'+'ABDGHIJMNPQRSTUWXY'
flag=''

for i in enc:
    if i in string.ascii_lowercase:
        index=grid.lower().index(i)
        flag+=string.ascii_lowercase[index]
        continue
    if i in string.ascii_uppercase:
        index=grid.upper().index(i)
        flag+=string.ascii_uppercase[index]
        continue
    flag+=i
print flag