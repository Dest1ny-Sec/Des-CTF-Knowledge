import hashlib

plaintext = 'TASC?O3RJMV?WDJKX?ZM' # 需要还原的密文

for i in range(26):
	temp1 = plaintext.replace('?',str(chr(65+i)),1) # 替换不超过1次
	for j in range(26):
		temp2 = temp1.replace('?',chr(65+j),1) # 替换第2个问号
		for n in range(26):
			temp3 = temp2.replace('?',chr(65+n),1) # 替换第3个问号
			s = hashlib.md5(temp3.encode('utf8')).hexdigest().upper()#注意大小写
			if s[:4] == 'E903':    #检查元素
				print (s)       #输出密文
