data = open("photo.dat","rb")
strs = data.read()
flag = open("flag.jpg","ab+")
for i in strs:
	flag.write(bytes([i ^ 0x33]))