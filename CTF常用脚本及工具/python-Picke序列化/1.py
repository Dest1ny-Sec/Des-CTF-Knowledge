import pickle  

fp = open("123.txt","rb+")
fw = open('pickle.txt', 'w')
a=pickle.load(fp)
pickle=str(a)
fw.write( pickle )
fw.close()
fp.close()