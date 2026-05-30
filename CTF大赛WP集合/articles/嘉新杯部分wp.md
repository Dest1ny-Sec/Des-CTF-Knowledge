# 嘉新杯部分wp

> 原文: https://www.ctfiot.com/271379.html
> ID: 271379

恒安嘉新杯

简单的逆向分析

EasyAES

fromCrypto.CipherimportAESfromhashlibimportsha256importstringimportitertoolsdefvalid_padding(s): iflen(s) ==0: returnFalse n = s[-1] ifn <1orn >32: returnFalse iflen(s) < n: returnFalse returnall(s[-i] == nforiinrange(1, n +1))defunpad(s): returns[:-s[-1]]defdecrypt_with_key(enc, key): iv = enc[:16] cipher = AES.new(key, AES.MODE_CBC, iv) dec = cipher.decrypt(enc[16:]) returndecdefmain(): c3_hex ="62343dfc3e978a1d580b54f345e1ed719c85ab15781acfe8ba3bcef1560c9cf54f187bc204c302a5ed4ebb5b5454151ba9b8b73841e17dc391c30a637ef8cfa14a25d01765231ef93a6faede2d66bad5d124201a2d278522bfd416de294677046d47f2827580cdcb9c0d3b18e4c0c68c8948aaefe4e684c7386b426db7898b5c2090047ff433bb6a75b38beaf81b7ad9404d2f09c642179697e9d3721eefc0eb12ba8c780a8d07672f70b00b9cadef74" c3 =bytes.fromhex(c3_hex) chars = string.ascii_letters + string.digits candidates = [] print("Brute forcing part2...") total =len(chars) **3 count =0 forpart2_tupleinitertools.product(chars, repeat=3): count +=1 ifcount %10000==0: print(f"Progress:{count}/{total}") part2 =''.join(part2_tuple) key1 = sha256(part2.encode()).digest() try: dec3 = decrypt_with_key(c3, key1) except: continue ifnotvalid_padding(dec3): continue c2 = unpad(dec3) iflen(c2) <16: continue try: dec2 = decrypt_with_key(c2, key1) except: continue ifnotvalid_padding(dec2): continue c1 = unpad(dec2) iflen(c1) <16: continue try: dec1 = decrypt_with_key(c1, key1) except: continue ifnotvalid_padding(dec1): continue c0 = unpad(dec1) iflen(c0) <16: continue candidates.append((part2, c0)) print(f"Found candidate part2:{part2}") print(f"Number of candidates:{len(candidates)}") print("Brute forcing part1 for each candidate...") forpart2, c0incandidates: forpart1_tupleinitertools.product(chars, repeat=3): part1 =''.join(part1_tuple) key0 = sha256(part1.encode()).digest() try: dec0 = decrypt_with_key(c0, key0) except: continue ifnotvalid_padding(dec0): continue flag_padded = unpad(dec0) try: flag_str = flag_padded.decode('utf-8') except: continue iflen(flag_str) ==36andflag_str.count('-') ==4: ifflag_str[8] =='-'andflag_str[13] =='-'andflag_str[18] =='-'andflag_str[23] =='-': print(f"Flag found:{flag_str}") print(f"Part1:{part1}, Part2:{part2}") return print("Done.")if__name__ =='__main__':main()

失窃的工艺

OTA流量分析

然后通过那个hello里面可以找到一个密钥和密文

{"message":"handshake ok","ok":true,"session_key":"b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90","vehicle_type":"normal"}ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==

晨星安全团队—-Zion_Cat


```
fromCrypto.CipherimportAESfromhashlibimportsha256importstringimportitertoolsdefvalid_padding(s): iflen(s) ==0: returnFalse n = s[-1] ifn <1orn >32: returnFalse iflen(s) < n: returnFalse returnall(s[-i] == nforiinrange(1, n +1))defunpad(s): returns[:-s[-1]]defdecrypt_with_key(enc, key): iv = enc[:16] cipher = AES.new(key, AES.MODE_CBC, iv) dec = cipher.decrypt(enc[16:]) returndecdefmain(): c3_hex ="62343dfc3e978a1d580b54f345e1ed719c85ab15781acfe8ba3bcef1560c9cf54f187bc204c302a5ed4ebb5b5454151ba9b8b73841e17dc391c30a637ef8cfa14a25d01765231ef93a6faede2d66bad5d124201a2d278522bfd416de294677046d47f2827580cdcb9c0d3b18e4c0c68c8948aaefe4e684c7386b426db7898b5c2090047ff433bb6a75b38beaf81b7ad9404d2f09c642179697e9d3721eefc0eb12ba8c780a8d07672f70b00b9cadef74" c3 =bytes.fromhex(c3_hex) chars = string.ascii_letters + string.digits candidates = [] print("Brute forcing part2...") total =len(chars) **3 count =0 forpart2_tupleinitertools.product(chars, repeat=3): count +=1 ifcount %10000==0: print(f"Progress:{count}/{total}") part2 =''.join(part2_tuple) key1 = sha256(part2.encode()).digest() try: dec3 = decrypt_with_key(c3, key1) except: continue ifnotvalid_padding(dec3): continue c2 = unpad(dec3) iflen(c2) <16: continue try: dec2 = decrypt_with_key(c2, key1) except: continue ifnotvalid_padding(dec2): continue c1 = unpad(dec2) iflen(c1) <16: continue try: dec1 = decrypt_with_key(c1, key1) except: continue ifnotvalid_padding(dec1): continue c0 = unpad(dec1) iflen(c0) <16: continue candidates.append((part2, c0)) print(f"Found candidate part2:{part2}") print(f"Number of candidates:{len(candidates)}") print("Brute forcing part1 for each candidate...") forpart2, c0incandidates: forpart1_tupleinitertools.product(chars, repeat=3): part1 =''.join(part1_tuple) key0 = sha256(part1.encode()).digest() try: dec0 = decrypt_with_key(c0, key0) except: continue ifnotvalid_padding(dec0): continue flag_padded = unpad(dec0) try: flag_str = flag_padded.decode('utf-8') except: continue iflen(flag_str) ==36andflag_str.count('-') ==4: ifflag_str[8] =='-'andflag_str[13] =='-'andflag_str[18] =='-'andflag_str[23] =='-': print(f"Flag found:{flag_str}") print(f"Part1:{part1}, Part2:{part2}") return print("Done.")if__name__ =='__main__':main()
```



```
{"message":"handshake ok","ok":true,"session_key":"b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90","vehicle_type":"normal"}ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273875-wxsync-2025-09-d77e4f5aa2eb8352d04bdb98b2580c11.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273877-wxsync-2025-09-87a48c74ba08a9efe68c22ad520b62e4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273879-wxsync-2025-09-d5d80ba71358a2d86bb51921be21a134.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273881-wxsync-2025-09-ab9bacc9db0c22e0c17723a071b36b08.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273883-wxsync-2025-09-32676a443b6569c69d9ccbcc1a72892f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273885-wxsync-2025-09-a16ae8fc7b4a1a4703852680129a3e4c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273887-wxsync-2025-09-51ed5506ed4648f567278216c1a43341.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273891-wxsync-2025-09-77b7f1de8cfa5b26c3dd4ed68e35d595.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273894-wxsync-2025-09-a2698cedc3fd7a0dc5d29b6859a973a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758273896-wxsync-2025-09-d95913104f7fb8b2783a5a0027749fca.png)