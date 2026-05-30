fw = open("pickle.txt","r")
text=fw.read( )
i=0
a=0

while i<len(text)+1:
    if(text[i]==']'):
       print('\n')
       a=0
    elif(text[i]=='('):
        if(text[i+2]==','):
            b=text[i+1]
            d=text[i+1]
            b=int(b)-int(a)
            c=1
            while c<b:
                print(" ", end="")
                c += 1
            print(text[i+5], end="")
            a=int(d)
        else:
            b=text[i+1]+text[i+2]
            d=text[i+1]+text[i+2]
            b=int(b)-int(a)
            c=1
            while c<b:
                print(" ", end="")
                c += 1
            print(text[i+6], end="")
            a=int(d)
    i +=1