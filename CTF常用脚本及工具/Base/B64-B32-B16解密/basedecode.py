import base64

file1 = open("./flag_encode.txt",'r')
file2 = open("flag.txt",'w')
base = file1.read()
while(1):
    try:
        base = base64.b32decode(base).decode()
    except:
        try:
            base = base64.b64decode(base).decode()
        except:
            try:
                base = base64.b16decode(base).decode()
            except:
                print("解码完成")
                file2.write(base)
                break