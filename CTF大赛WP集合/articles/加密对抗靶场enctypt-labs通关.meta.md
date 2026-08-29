---
title: 加密对抗靶场enctypt-labs通关
contest: encrypt-labs / 加密对抗靶场
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [encrypt-labs, AES, DES, RSA, HmacSHA256, 加签验签, 防重放, 弱口令, autodecoder, Yakit热加载]
attack_chain:
  - 第 1 关: 对称加密 (算法定位) → admin/1234
  - 第 2 关: AES key 固定 t3giDeeWT99XilzCslD9EQ== iv=+jVQ1xurlO1dvxYRk9TvRA==
  - 第 3 关: RSA 加密 (只公钥, 只能加密不能解密)
  - 第 4 关: AES+RSA 混合 → 替换 JS 固定 key/iv (复用第 2 关)
  - 第 5 关: DES 规律 key (username=test → key=key66666, iv=9999test)
  - 第 6 关: HmacSHA256 加签 → secret_key=be56e057f20f883e, timestamp 10 位
  - 第 7 关: 防重放 + RSA 加密 timestamp 13 位 + Yakit 热加载
  - 第 8 关: 加签 key 在服务端 → 弱口令 admin/123456
  - autodecoder 一键解密 (前 5 关)
  - 第 6-7 关自写 Flask /encode /decode 接口
key_payload: 'admin/1234 + admin/123456 弱口令 + autodecoder + Yakit热加载'
one_liner: encrypt-labs 8 关通关：对称/AES/RSA/混合/DES/HmacSHA256/防重放/服务端签，最关键是替换 JS 固定 key 和弱口令。
lesson: 加密对抗核心思路: 1) 抓包定位算法位置 2) 提取 key/iv (硬编码/可预测/可替换 JS) 3) autodecoder 一键解密 4) 防重放注意 timestamp + nonce; 5) 实在不行弱口令爆破。
quality: medium
---

# 加密对抗靶场enctypt-labs通关

## 概览
- **来源**: ctfiot 216940
- **靶场**: https://github.com/SwagXz/encrypt-labs
- **难度**: ⭐⭐⭐

## 8 关

### Q1: 对称加密
- 抓包定位算法 → 直接还原明文
- 还原: `{"username":"admin","password":"1234"}`

### Q2: AES 服务端 key 固定
```json
{"aes_key":"t3giDeeWT99XilzCslD9EQ==","aes_iv":"+jVQ1xurlO1dvxYRk9TvRA=="}
```

### Q3: RSA 加密
- 只公钥无私钥 → 只能加密不能解密
- 靶场只测登录无越权 → 没问题

### Q4: AES+RSA 混合
- key+iv 每次随机 → 替换 JS 固定 key/iv (复用 Q2)
- password 爆破

### Q5: DES 规律 key
- username=test → key=key66666, iv=9999test
- username=admin → key=admin66666, iv=9999admin

### Q6: HmacSHA256 加签
```python
secret_key = "be56e057f20f883e"
data_to_sign = f"{username}{password}{nonce}{timestamp}"
new_signature = hmac.new(secret_key.encode('utf-8'),
                          data_to_sign.encode('utf-8'),
                          hashlib.sha256).hexdigest()
```
- 自写 Flask `/encode` `/decode` 接口

### Q7: 防重放 + RSA timestamp
- 13 位毫秒 timestamp
- generateRequestData 用 RSA 加密 timestamp
- Yakit 热加载:
```yak
rsa = func(random) {
    public_key = `-----BEGIN PUBLIC KEY-----...`
    return codec.EncodeBase64(codec.RSAEncryptWithPKCS1v15(public_key, f'${random}'~))
}
req = result => {
    r1 = time.Now().Unix()
    return rsa(r1*1000)
}
```

### Q8: 加签 key 在服务端 (安全无解)
- 签名靠服务端生成, 客户端只能调
- 弱口令: `admin/123456`
- GG 弱口令 yyds

## 工具
- **autodecoder**: 前 5 关一键解密
- **Yakit 热加载**: 第 6-7 关动态修改 timestamp
- **Flask 自写接口**: 第 6 关 HmacSHA256 加签

## 教学
- 加密对抗核心: 抓包 + 算法定位 + 提取 key/iv + 替换 JS
- 防重放: timestamp + nonce 唯一性 + 服务端超时校验
- 弱口令是最终杀手锏
