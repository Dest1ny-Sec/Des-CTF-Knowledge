---
title: 腾讯云安全挑战赛·COS提权与利用 WP
contest: 腾讯云安全挑战赛 2025
year: 2025
difficulty: hard
vuln_type: crypto_oracle
tags: [Java-CrackMe, AES-ECB, XOR-deobfuscate, COS-bucket-policy, Tencent-Cloud-API, CVM-ResetInstancesPassword, COS-PutBucketACL-Deny, IP-not-equal, ip_restriction]
attack_chain:
- Java CrackMe:AbstractHashMap+密钥LiLiLLLiiiLLiiLLi="Q8Ro9cHYVAdBaRD8"(AES)
- 静态初始化GIiIiLA.add(20+条base64)
- AES-ECB解密每个base64
- 再做XOR deobfuscate:i_start=(11963830^57816743)^(15501129^52968536),xor_key=(95558172^72233696)^(85510964^82109419)
- 解出:secret_id="AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW"
- secret_key="6ijalekmP0w5b4iiatUZVriHtd3iDTp98sbow/EhGGE="
- token="8RWwthXC3rhLqqs60VtkfdrK2QVtRlua1eac99e9bd0f081699323aa8e9fbfa06..."
- region="ap-guangzhou",scheme="https"
- COS API:get_bucket_policy返回Policy,Action=name/cos:PutBucketACL+ip_not_equal
- IP限制:["106.53.243.200","172.16.0.129"]
- qcloud-cos-python-sdk-v5:pip install cos-python-sdk-v5 --break-system-packages
- 绕过思路:从CVM API ResetInstancesPassword改机器密码+SSRF到PutBucketACL
- CommonClient cvm.tencentcloudapi.com,Region=ap-guangzhou,Action=ResetInstancesPassword
- params={"InstanceIds":["ins-xxx"],"Password":"Aa112211.","UserName":"root","ForceStop":true}
key_payload: AES+deobfuscate AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW
one_liner: 腾讯云安全挑战赛COS提权与利用WP,Java CrackMe反编译AES-ECB+XOR deobfuscate解出AK/SK/Token,COS Bucket Policy分析(IPCAM not-equal限制+PutBucketACL),CVM ResetInstancesPassword+SSRF绕过链。
lesson: 云安全比赛常考"反编译获取云凭据+滥用云API提权",Java CrackMe的AES-ECB+XOR组合是典型混淆;COS Bucket Policy的ip_not_equal可被CVM SSRF绕过;ResetInstancesPassword是云提权关键API。
quality: high
---

## 题目列表

1道云安全:COS提权与利用

## 关键考点

### Java CrackMe分析
- AbstractHashMap中存在加解密逻辑
- 密钥:private static String LiLiLLLiiiLLiiLLi = "Q8Ro9cHYVAdBaRD8" (AES)
- 静态初始化:GIiIiLA.add(20+条base64)
- CrackMe存在大量xor加密内容

### AES-ECB解密
```python
KEY = "Q8Ro9cHYVAdBaRD8".encode('utf-8')
def aes_decrypt(encrypted_data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    decoded_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(decoded_data)
    pad_len = decrypted_data[-1]
    return decrypted_data[:-pad_len].decode('utf-8', errors='ignore')
```

### XOR deobfuscate
```python
def calculate_obfuscation_params():
    a = 11963830 ^ 57816743
    b = 15501129 ^ 52968536
    i_start = a ^ b
    c = 95558172 ^ 72233696
    d = 85510964 ^ 82109419
    xor_key = c ^ d
    return i_start, xor_key

def deobfuscate(data_str, i_start, xor_key):
    decode = base64.b64decode(data_str)
    decode_list = list(decode)
    for i in range(i_start, len(decode_list)):
        decode_list[i] = decode_list[i] ^ xor_key
    return bytes(decode_list).decode('utf-8', errors='ignore')
```

### 解出的COS凭据
- secret_id="AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW"
- secret_key="6ijalekmP0w5b4iiatUZVriHtd3iDTp98sbow/EhGGE="
- token="8RWwthXC3rhLqqs60VtkfdrK2QVtRlua1eac99e9bd0f081699323aa8e9fbfa06..."
- region="ap-guangzhou"

### COS Bucket Policy分析
- Action: name/cos:PutBucketACL
- Effect: Deny
- Condition: ip_not_equal ["106.53.243.200", "172.16.0.129"]
- 限制:只有这两个IP能PutBucketACL

### CVM API ResetInstancesPassword
- 思路:从CVM改机器密码,然后SSRF到COS
- CommonClient("cvm", "2017-03-12", cred, "ap-guangzhou")
- params={"InstanceIds":["ins-xxx"],"Password":"Aa112211.","UserName":"root","ForceStop":true}
- ResetInstancesPassword + 目标CVM

### Python SDK
- apt install python3-pip
- python3 -m pip install -U cos-python-sdk-v5 --break-system-packages

## 实战价值
- 云安全比赛常考"反编译获取云凭据+滥用云API提权"
- Java CrackMe的AES-ECB+XOR组合是典型混淆
- COS Bucket Policy的ip_not_equal可被CVM SSRF绕过
- ResetInstancesPassword是云提权关键API
- qcloud-cos-python-sdk-v5是标准工具
