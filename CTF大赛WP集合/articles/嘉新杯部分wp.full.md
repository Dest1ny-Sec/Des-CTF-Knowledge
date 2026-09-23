---
title: 嘉新杯部分wp
contest: 恒安嘉新杯 / EasyAES + 失窃的工艺
year: 2025
difficulty: medium
vuln_type: crypto_oracle
tags:
- EasyAES
- 4层CBC
- 双重爆破
- SHA-256 key派生
- OTA流量分析
- 晨星安全团队
- Zion_Cat
attack_chain:
- '题1 EasyAES: 4 层 AES-CBC 加密'
- c3 (密文 hex 192 字节) → 3 次 unpad + decrypt 得 c0
- part2 (3 字符 ascii_letters+digits) SHA-256 派生 key1
- 解 c3 → c2 → c1 → c0 (需要 valid_padding 检查)
- part1 (3 字符) SHA-256 派生 key0, 解 c0 → flag (36 字符 + 4 横线)
- 'flag 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
- '题2 失窃的工艺: OTA 流量分析'
- hello 消息找到 session_key + vehicle_type + 密文
- 'session_key: b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90'
- ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==
key_payload: '''4 层 AES-CBC + part1+part2 SHA-256 派生 key + flag UUID 格式'''
one_liner: 嘉新杯 2 题：EasyAES 4 层 CBC 双重爆破 + 失窃的工艺 OTA 流量分析 session_key 解密。
lesson: 多层 AES-CBC 加密需要 valid_padding 检查 + unpad 逐层验证; SHA-256 短 key 派生可爆破 (3 字符 62^3 = 238k); OTA 流量 first message 通常含 session_key。
quality: medium
full_path: 嘉新杯部分wp.full.md
meta_path: 嘉新杯部分wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '嘉新杯部分wp。嘉新杯 2 题：EasyAES 4 层 CBC 双重爆破 + 失窃的工艺 OTA 流量分析 session_key 解密。。关键路径：题1 EasyAES: 4 层 AES-CBC 加密 → c3 (密文 hex 192 字节) → 3 次 unpad + decrypt 得 c0 → part2 (3 字符 ascii_letters+digits) SHA-256 派生 ...'
category: crypto
subcategory: oracle
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/271379.html
reasoning_chain:
- '嘉新杯 2 题, 题 1 EasyAES 4 层 AES-CBC 加密 c3 (192 字节 hex) → 触发点: 多层加密'
- '假设: 3 字符 ascii_letters+digits 派生 key 爆破 part2 → 动作: 62^3 = 238k 遍历 SHA-256 → 观察: valid_padding 验证 unpad'
- '假设: 3 次 unpad + decrypt 得 c0 → 动作: 循环 candidates.append((part2, c0)) → 观察: part1 3 字符再爆破 → 解出 flag (UUID 格式)'
- '题 2 失窃的工艺 OTA 流量分析 → 触发点: hello 消息含 session_key → 假设: OTA 协议 first message 含密钥'
- '动作: tshark 提取 hello 消息 → 观察: session_key=b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90'
- '动作: vehicle_type + AES-GCM 解密密文 ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg== → 完成'
failed_attempts:
- '试图不解 valid_padding 直接 decrypt → 失败: padding error 抛异常'
- '试图爆破 part1 全组合 → 失败: 必须先 valid part2 解 c0 才能解 part1'
key_observations:
- 多层 AES-CBC 加密需要 valid_padding 检查 + unpad 逐层验证 (不能跳过中间)
- SHA-256 短 key 派生可爆破 (3 字符 62^3 = 238k 可接受)
- OTA 流量 first message (hello) 通常含 session_key
- 'flag UUID 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
prerequisites:
- AES-CBC 加解密 + PKCS7 padding
- SHA-256 短 key 派生爆破
- OTA 协议分析 (hello 消息结构)
- tshark 字段提取
---
# 嘉新杯部分wp

> 原文: https://www.ctfiot.com/271379.html
> ID: 271379

恒安嘉新杯

简单的逆向分析

EasyAES

fromCrypto.CipherimportAESfromhashlibimportsha256importstringimportitertoolsdefvalid_padding(s): iflen(s) ==0: returnFalse n = s[-1] ifn <1orn >32: returnFalse iflen(s) < n: returnFalse returnall(s[-i] == nforiinrange(1, n +1))defunpad(s): returns[:-s[-1]]defdecrypt_with_key(enc, key): iv = enc[:16] cipher = AES.new(key, AES.MODE_CBC, iv) dec = cipher.decrypt(enc[16:]) returndecdefmain(): c3_hex ="62343dfc3e978a1d580b54f345e1ed719c85ab15781acfe8ba3bcef1560c9cf54f187bc204c302a5ed4ebb5b5454151ba9b8b73841e17dc391c30a637ef8cfa14a25d01765231ef93a6faede2d66bad5d124201a2d278522bfd416de294677046d47f2827580cdcb9c0d3b18e4c0c68c8948aaefe4e684c7386b426db7898b5c2090047ff433bb6a75b38beaf81b7ad9404d2f09c642179697e9d3721eefc0eb12ba8c780a8d07672f70b00b9cadef74" c3 =bytes.fromhex(c3_hex) chars = string.ascii_letters + string.digits candidates = [] print("Brute forcing part2...") total =len(chars) **3 count =0 forpart2_tupleinitertools.product(chars, repeat=3): count +=1 ifcount %10000==0: print(f"Progress:{count}/{total}") part2 =''.join(part2_tuple) key1 = sha256(part2.encode()).digest() try: dec3 = decrypt_with_key(c3, key1) 
except: continue ifnotvalid_padding(dec3): continue c2 = unpad(dec3) iflen(c2) <16: continue try: dec2 = decrypt_with_key(c2, key1) 
except: continue ifnotvalid_padding(dec2): continue c1 = unpad(dec2) iflen(c1) <16: continue try: dec1 = decrypt_with_key(c1, key1) 
except: continue ifnotvalid_padding(dec1): continue c0 = unpad(dec1) iflen(c0) <16: continue candidates.append((part2, c0)) print(f"Found candidate part2:{part2}") print(f"Number of candidates:{len(candidates)}") print("Brute forcing part1 for each candidate...") forpart2, c0incandidates: forpart1_tupleinitertools.product(chars, repeat=3): part1 =''.join(part1_tuple) key0 = sha256(part1.encode()).digest() try: dec0 = decrypt_with_key(c0, key0) 
except: continue ifnotvalid_padding(dec0): continue flag_padded = unpad(dec0) try: flag_str = flag_padded.decode('utf-8') 
except: continue iflen(flag_str) ==36andflag_str.count('-') ==4: ifflag_str[8] =='-'andflag_str[13] =='-'andflag_str[18] =='-'andflag_str[23] =='-': print(f"Flag found:{flag_str}") print(f"Part1:{part1}, Part2:{part2}") return print("Done.")if__name__ =='__main__':
main()

失窃的工艺

OTA流量分析

然后通过那个hello里面可以找到一个密钥和密文

{"message":"handshake ok","ok":
true,"session_key":"b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90","vehicle_type":"normal"}ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==

晨星安全团队—-Zion_Cat


```
fromCrypto.CipherimportAESfromhashlibimportsha256importstringimportitertoolsdefvalid_padding(s): iflen(s) ==0: returnFalse n = s[-1] ifn <1orn >32: returnFalse iflen(s) < n: returnFalse returnall(s[-i] == nforiinrange(1, n +1))defunpad(s): returns[:-s[-1]]defdecrypt_with_key(enc, key): iv = enc[:16] cipher = AES.new(key, AES.MODE_CBC, iv) dec = cipher.decrypt(enc[16:]) returndecdefmain(): c3_hex ="62343dfc3e978a1d580b54f345e1ed719c85ab15781acfe8ba3bcef1560c9cf54f187bc204c302a5ed4ebb5b5454151ba9b8b73841e17dc391c30a637ef8cfa14a25d01765231ef93a6faede2d66bad5d124201a2d278522bfd416de294677046d47f2827580cdcb9c0d3b18e4c0c68c8948aaefe4e684c7386b426db7898b5c2090047ff433bb6a75b38beaf81b7ad9404d2f09c642179697e9d3721eefc0eb12ba8c780a8d07672f70b00b9cadef74" c3 =bytes.fromhex(c3_hex) chars = string.ascii_letters + string.digits candidates = [] print("Brute forcing part2...") total =len(chars) **3 count =0 forpart2_tupleinitertools.product(chars, repeat=3): count +=1 ifcount %10000==0: print(f"Progress:{count}/{total}") part2 =''.join(part2_tuple) key1 = sha256(part2.encode()).digest() try: dec3 = decrypt_with_key(c3, key1) 
except: continue ifnotvalid_padding(dec3): continue c2 = unpad(dec3) iflen(c2) <16: continue try: dec2 = decrypt_with_key(c2, key1) 
except: continue ifnotvalid_padding(dec2): continue c1 = unpad(dec2) iflen(c1) <16: continue try: dec1 = decrypt_with_key(c1, key1) 
except: continue ifnotvalid_padding(dec1): continue c0 = unpad(dec1) iflen(c0) <16: continue candidates.append((part2, c0)) print(f"Found candidate part2:{part2}") print(f"Number of candidates:{len(candidates)}") print("Brute forcing part1 for each candidate...") forpart2, c0incandidates: forpart1_tupleinitertools.product(chars, repeat=3): part1 =''.join(part1_tuple) key0 = sha256(part1.encode()).digest() try: dec0 = decrypt_with_key(c0, key0) 
except: continue ifnotvalid_padding(dec0): continue flag_padded = unpad(dec0) try: flag_str = flag_padded.decode('utf-8') 
except: continue iflen(flag_str) ==36andflag_str.count('-') ==4: ifflag_str[8] =='-'andflag_str[13] =='-'andflag_str[18] =='-'andflag_str[23] =='-': print(f"Flag found:{flag_str}") print(f"Part1:{part1}, Part2:{part2}") return print("Done.")if__name__ =='__main__':
main()
{"message":"handshake ok","ok":
true,"session_key":"b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90","vehicle_type":"normal"}ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]